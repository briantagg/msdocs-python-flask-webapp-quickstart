from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import os
import random
import time

actions = Blueprint('actions', __name__)

# Accout Actions --------------------------------------------------------

@actions.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')

    return render_template("notes.html", user=current_user)


@actions.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})


@actions.route("/transfer", methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        # don't allow empty amount or the 'from' and 'to' account to be the same
        if request.form['amount'] == '' or request.form['from_account'] == request.form['to_account']:
            return render_template('transfer.html')
        else:
            amount = request.form['amount']
            from_account=request.form['from_account']
            to_account=request.form['to_account']

        # build the json filename
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static/json/" + str(current_user.email) + "_account.json")
        data = json.load(open(json_url))

        # work out total for current account
        current_account_total = 0
        for p in data['current_account']:
            current_account_total += float(p['Amount'])

        # work out total for savings account
        savings_account_total = 0
        for p in data['savings_account']:
            savings_account_total += float(p['Amount'])

        # work out total for investments account
        investments_account_total = 0
        for p in data['investments_account']:
            investments_account_total += float(p['Amount'])

        # create 16-digit random reference number
        transaction_id = int(random.random()*10000000000000000)

        data['current_account'].reverse()
        data['savings_account'].reverse() # flip  lists descending for append
        data['investments_account'].reverse()

        # format numbers as currencies (12,345.00)
        plus_amount = "{0:.2f}".format(float(amount))
        minus_amount = "{0:.2f}".format(float(amount)*-1)
        amount_currency_formatted = "{0:,.2f}".format(float(amount))

        if from_account == 'current': # deplete current account and increase the to_account
            if float(amount) < current_account_total: # don't let the current account go overdrawn
                if to_account == 'savings':
                    data['savings_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer from Current', 'Amount': plus_amount,})
                    data['current_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer to Savings', 'Amount': minus_amount,}) # deplete (minus)
                    flash('£' + str(amount_currency_formatted) + ' transferred from Current Account to Savings Account', 'success')
                elif to_account == 'investments':
                    data['investments_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer from Current', 'Amount': plus_amount,})
                    data['current_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer to Investments', 'Amount': minus_amount,}) # deplete (minus)
                    flash('£' + str(amount_currency_formatted) + ' transferred from Current Account to Investments Account', 'success')
            else:
                flash('There were insufficient funds to transfer £' + str(amount_currency_formatted) + ' from Current Account to Investments Account', 'danger')

        elif from_account == 'savings':
            if float(amount) < savings_account_total: # don't let the savings account go overdrawn
                if to_account == 'current':
                    data['current_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer from Savings', 'Amount': plus_amount,})
                    data['savings_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer to Current', 'Amount': minus_amount,})
                    flash('£' + str(amount_currency_formatted) + ' transferred from Savings Account to Current Account', 'success')
                elif to_account == 'investments':
                    data['investments_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer from Savings', 'Amount': plus_amount,})
                    data['savings_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer to Investments', 'Amount': minus_amount,}) 
                    flash('£' + str(amount_currency_formatted) + ' transferred from Savings Account to Investments Account', 'success')
            else:
                flash('There were insufficient funds to transfer £' + str(amount_currency_formatted) + ' from Savings Account to Investments Account', 'danger')

        elif from_account == 'investments':
            if float(amount) < investments_account_total: # don't let the investments account go overdrawn
                if to_account == 'current':
                    data['current_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer from Investments', 'Amount': plus_amount,})
                    data['investments_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer to Current', 'Amount': minus_amount,})
                    flash('£' + str(amount_currency_formatted) + ' transferred from Investments Account to Current Account', 'success')
                elif to_account == 'savings':
                    data['savings_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer from Investments', 'Amount': plus_amount,})
                    data['investments_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Transfer to Savings', 'Amount': minus_amount,})
                    flash('£' + str(amount_currency_formatted) + ' transferred from Investments Account to Savings Account', 'success')
            else:
                flash('There were insufficient funds to transfer £' + str(amount_currency_formatted) + ' from Investments Account to Savings Account', 'danger')

        data['current_account'].reverse()
        data['savings_account'].reverse() # flip list back to newest at top
        data['investments_account'].reverse() 
        
        # save the appended data back to ["static/json/" + str(current_user.email) + "_account.json"] 
        with open(json_url, 'w') as f:
            json.dump(data, f)
        return redirect(url_for('views.accounts'))
    else:
        return render_template('transfer.html', user=current_user)


@actions.route("/pay", methods=['GET', 'POST'])
@login_required
def pay():
    if request.method == 'POST':
        # don't allow empty amount or the 'from' and 'to' account to be the same
        if request.form['amount'] == '':
            return render_template('pay.html')
        else:
            amount = request.form['amount']
            from_account=request.form['from_account']
            to_account=request.form['to_account']

        # build the json filename
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static/json/" + str(current_user.email) + "_account.json")
        data = json.load(open(json_url))

        # work out total for current account
        current_account_total = 0
        for p in data['current_account']:
            current_account_total += float(p['Amount'])

        # work out total for savings account
        savings_account_total = 0
        for p in data['savings_account']:
            savings_account_total += float(p['Amount'])

        # work out total for investments account
        investments_account_total = 0
        for p in data['investments_account']:
            investments_account_total += float(p['Amount'])

        # create 16-digit random reference number
        transaction_id = int(random.random()*10000000000000000)

        data['savings_account'].reverse()    
        data['investments_account'].reverse() # reverse the order to append the item
        data['current_account'].reverse()

        # format number as currencies (12,345.00)
        plus_amount = "{0:.2f}".format(float(amount))
        minus_amount = "{0:.2f}".format(float(amount)*-1)
        amount_currency_formatted = "{0:,.2f}".format(float(amount))

        if from_account == 'current':
            if float(amount) < current_account_total: # don't let the current account go overdrawn
                data['current_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Payment to ' + str(to_account), 'Amount': minus_amount,})
                flash('£' + str(amount_currency_formatted) + ' paid from Current Account to ' + str(to_account), 'success')
            else:
                flash('There were insufficient funds to transfer £' + str(amount_currency_formatted) + ' from Current Account to ' + str(to_account), 'danger')

        elif from_account == 'savings':
            if float(amount) < savings_account_total: # don't let the savings account go overdrawn
                data['savings_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Payment to ' + str(to_account), 'Amount': minus_amount,})
                flash('£' + str(amount_currency_formatted) + ' paid from Savings Account to ' + str(to_account), 'success')
            else:
                flash('There were insufficient funds to transfer £' + str(amount_currency_formatted) + ' from Savings Account to ' + str(to_account), 'danger')

        elif from_account == 'investments':
            if float(amount) < investments_account_total: # don't let the investments account go overdrawn
                data['investments_account'].append({'ID': transaction_id, 'Date': time.strftime("%d-%m-%Y"), 'Type': 'Payment to ' + str(to_account), 'Amount': minus_amount,})
                flash('£' + str(amount_currency_formatted) + ' paid from Investments Account to ' + str(to_account), 'success')
            else:
                flash('There were insufficient funds to transfer £' + str(amount_currency_formatted) + ' from Investments Account to ' + str(to_account), 'danger')

        data['savings_account'].reverse()    
        data['investments_account'].reverse() # flip them all back
        data['current_account'].reverse()

        # save the appended data back to ["static/json/" + str(current_user.email) + "_account.json"]
        with open(json_url, 'w') as f:
            json.dump(data, f)

        return redirect(url_for('views.accounts'))
    else:
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static/json", "payees.json")
        data = json.load(open(json_url))
        # build payees list from payees.json
        payees_list = []
               
        for p in data['my_payees']:
            payees_list.append(p['payee_name'])

        return render_template('pay.html', payees_list=payees_list, user=current_user)


@actions.route("/payees", methods=['GET', 'POST'])
@login_required
def payees():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "payees.json")
    data = json.load(open(json_url))
    
    if request.method == 'GET': # show payees
        return render_template('payees.html', data=data, user=current_user)

    elif request.method == 'POST':
        payee_name = request.form['payee_name']
        
        new_list = []
        for x in data['my_payees']:
            if x['payee_name'] != payee_name:
                new_list.append(x)

        data['my_payees'] = new_list

        # save the appended data back to ["static/json/payees.json"]
        with open(json_url, 'w') as f:
            json.dump(data, f)

        return render_template('payees.html', data=data, user=current_user)


@actions.route("/add_payee", methods=['GET', 'POST'])
@login_required
def add_payee():

    # build the json filename
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "payees.json")
    data = json.load(open(json_url))
    
    if request.method == 'GET':
        return render_template('add_payee.html', data=data, user=current_user)
    
    elif request.method == 'POST':
        payee_name = request.form['payee_name']
        payee_sort_code = request.form['sort_code']
        payee_account_number = request.form['account_number']
        payee_reference = request.form['payee_reference']

        # append new payee data
        data['my_payees'].append({'payee_acc_number': str(payee_account_number), 'payee_name': str(payee_name), 'payee_ref': str(payee_reference), 'payee_sort_code': str(payee_sort_code),})
        
        # save the appended data back to ["static/json/payees.json"]
        with open(json_url, 'w') as f:
            json.dump(data, f)

        return render_template('payees.html', data=data, user=current_user)


@actions.route("/delete_payee", methods=['GET', 'POST'])
@login_required
def delete_payee():

    # build the json filename
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "payees.json")
    data = json.load(open(json_url))
    
    if request.method == 'GET':
        return render_template('delete_payee.html', data=data, user=current_user)
    
    elif request.method == 'POST':
        payee_name = request.form['payee_name']

        # append new payee data
        #data['my_payees'].append({'payee_acc_number': str(payee_account_number), 'payee_name': str(payee_name), 'payee_ref': str(payee_reference), 'payee_sort_code': str(payee_sort_code),})
        
        new_list = []
        for x in data['my_payees']:
            if x['payee_name'] != payee_name:
                new_list.append(x)

        data['my_payees'] = new_list

        # save the appended data back to ["static/json/payees.json"]
        with open(json_url, 'w') as f:
            json.dump(data, f)

        return render_template('payees.html', data=data, user=current_user)
