#/usr/bin/python

import json

json_url = '{"my_payees": [{"payee_acc_number": "1234 5678", "payee_name": "Giles Hadden", "payee_ref": "MHADDEN", "payee_sort_code": "01-02-03"}, {"payee_acc_number": "5687 3332", "payee_name": "Ben Brown", "payee_ref": "BROWN", "payee_sort_code": "01-02-03"}, {"payee_acc_number": "9467 1477", "payee_name": "Charleen Taylor", "payee_ref": "TAYLOR-C", "payee_sort_code": "01-02-03"}, {"payee_acc_number": "1234 5678", "payee_name": "Miles Hadden", "payee_ref": "MHADDEN", "payee_sort_code": "01-02-03"}, {"payee_acc_number": "1234 5678", "payee_name": "Brian Tagg", "payee_ref": "BT2", "payee_sort_code": "12-34-56"}, {"payee_acc_number": "4512 9566", "payee_name": "Cath Chambers", "payee_ref": "CHAMB001", "payee_sort_code": "10-52-63"}, {"payee_acc_number": "6352 4141", "payee_name": "David Dickinson", "payee_ref": "DD1000", "payee_sort_code": "65-45-23"}, {"payee_acc_number": "6598 4147", "payee_name": "Eric Idle", "payee_ref": "Go8", "payee_sort_code": "74-89-51"}, {"payee_acc_number": "8546 4755", "payee_name": "Fred Forsythe", "payee_ref": "OK1", "payee_sort_code": "74-77-35"}]}'
data = json.loads(json_url)
#print(data)

new_list = []

for x in data['my_payees']:
    if x['payee_name'] != "Cath Chambers":
        new_list.append(x)

print(new_list)
