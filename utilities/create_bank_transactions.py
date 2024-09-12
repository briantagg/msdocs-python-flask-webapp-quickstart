import os
import random
import json
import time
import math
from datetime import date, timedelta

# rounding functions
def roundup_10(x): # rounds up to nearest GBP10
    return x if x % 10 == 0 else x + 10 - x % 10

def roundup_100(x): # rounds up to nearest GBP100
    return x if x % 100 == 0 else x + 100 - x % 100

def create_user_bank_accounts(*account_holders):
    for account_holder in account_holders:
        print(account_holder)

        # create empty json file
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "../website/static/json/", str(account_holder) + "_account.json")
        template_file = open(json_url, "w")
        line = '{"current_account": [], "savings_account": [], "investments_account": []}'
        template_file.write(line)
        template_file.write("\n")
        template_file.close()

        # open created json file to append new data
        data = json.load(open(json_url))

        # create current account entries
        for x in range(500): # 500 transaction entries
            transaction_date = date.today() - timedelta(days=x)
            
            # STATIC PAYMENTS

            # Salary Payments (1st of month)
            if transaction_date.strftime("%d") == '01':
                        id_number_current = int(random.random()*10000000000000000)
                        data['current_account'].append({'ID': id_number_current, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'BACS Payment', 'Amount': "3115.65",})

            # Rent payments (2nd of month)
            if transaction_date.strftime("%d") == '02':
                        id_number_current = int(random.random()*10000000000000000)
                        data['current_account'].append({'ID': id_number_current, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'Royal Housing', 'Amount': "-1240.00",})

            # Direct Debits (13, 14, 17, 20, 21 of month)
            if transaction_date.strftime("%d") in ['13', '14', '17', '20', '21']:
                        id_number_current = int(random.random()*10000000000000000)
                        random_amount_out = random.randint(5000,10000)/100*-1  # between GBP-50.00 and GBP-100.00
                        random_amount_out = "{0:.2f}".format(random_amount_out)
                        data['current_account'].append({'ID': id_number_current, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'Direct Debit', 'Amount': random_amount_out,})

            # Transfers to Savings Account (27th of month)
            if transaction_date.strftime("%d") == '27':
                amount_to_savings = roundup_100(random.randint(100,400))
                amount_from_current = amount_to_savings*-1
                amount_to_savings = "{0:.2f}".format(amount_to_savings)
                amount_from_current= "{0:.2f}".format(amount_from_current)
                id_number_savings = int(random.random()*10000000000000000)

                data['savings_account'].append({'ID': id_number_savings, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'Transfer from Current', 'Amount': amount_to_savings,})
                data['current_account'].append({'ID': id_number_savings, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'Transfer to Savings', 'Amount': amount_from_current,})

            # Transfers to Investments Account (28th of month)
            if transaction_date.strftime("%d") == '28':
                amount_to_investments = roundup_100(random.randint(500,1000))
                amount_from_current = amount_to_investments*-1
                amount_to_investments = "{0:.2f}".format(amount_to_investments)
                amount_from_current= "{0:.2f}".format(amount_from_current)
                id_number_savings = int(random.random()*10000000000000000)

                data['investments_account'].append({'ID': id_number_savings, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'Transfer from Current', 'Amount': amount_to_investments,})
                data['current_account'].append({'ID': id_number_savings, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': 'Transfer to Investments', 'Amount': amount_from_current,})

            # NON-STATIC PAYMENTS

            # transaction has a 1 in 5 chance of happening
            transaction_dice = {1: False, 2: False, 3: False, 4: False, 5: True}
            transaction_dice_roll = random.randint(1,5)
            transaction_today = transaction_dice[transaction_dice_roll]

            # transaction is 'Card Payment' but 1 in 4 is an ATM withdrawel
            if transaction_today == True:
                transaction_types = {1:'Card Payment', 2:'Card Payment', 3: 'Card Payment', 4: 'ATM Withdrawel'}
                transaction_type_selection = random.randint(1,4)
                selected_transaction_type = transaction_types[transaction_type_selection]

                random_amount_out = random.randint(100,10000)/100  # each transaction between GBP-1.00 and GBP-100.00

                if selected_transaction_type == 'ATM Withdrawel':
                    random_amount_out = roundup_10(random_amount_out)

                random_amount_out = random_amount_out*-1 # minus in account
                random_amount_out = "{0:.2f}".format(random_amount_out)
                id_number_current = int(random.random()*10000000000000000)
                data['current_account'].append({'ID': id_number_current, 'Date': transaction_date.strftime("%d-%m-%Y"), 'Type': selected_transaction_type, 'Amount': random_amount_out,})


                # save the appended data back to ["static\json\\" + str(current_user.email) + "_account.json"]
                with open(json_url, 'w') as f:
                    json.dump(data, f, indent=2) # indent=2 for newline after each entry


def main():
      #create_user_bank_accounts('brian@temp.com', 'anna@abc.com')
      create_user_bank_accounts('aanderson@abc.com')
      #pass


if __name__ == '__main__':
      main()

