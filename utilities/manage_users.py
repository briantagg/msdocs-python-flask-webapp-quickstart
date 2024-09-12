import sqlite3
from sqlite3 import Error
from create_bank_transactions import create_user_bank_accounts
import os

# create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# tasks
def show_all_user_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def create_user_accounts(conn):
    cur = conn.cursor()
    cur.execute("SELECT email FROM user")
    rows = cur.fetchall()
    
    for row in rows:
        row = str(row)
        account_holder = row[2:-3] # changes: ('name@mail.com',) => name@gmail.com
        create_user_bank_accounts(account_holder)


def delete_user(conn, id):
    cur = conn.cursor()
    
    # Delete user json
    cur.execute("SELECT email FROM user WHERE id=" + id)
    rows = cur.fetchall()

    for row in rows:
        json_to_delete = str(row)[2:-3]
        print(json_to_delete)
    
    #command_string = "del ..\website\static\json\\" + str(json_to_delete) + "_account.json"
    command_string = "del ../website/static/json/" + str(json_to_delete) + "_account.json"
    os.system(command_string)
    print("json " + json_to_delete + " deleted.\n")
    
    # Delete user from db
    cur.execute("DELETE FROM user WHERE id=?", (id,))
    print("id " + id + " deleted.")


def main():
    database = r"../instance/database.db"

    # create a database connection
    try:
        conn = create_connection(database)
        while True:
            with conn:
                # functions
                print("\n")
                print("1. Show All Users")
                print("2. Delete User")
                print("3. Create User Accounts")
                print("[Ctrl]+C to Exit")
                
                chosen_function = input("Which Function? ")

                if chosen_function == "1":
                    show_all_user_data(conn)
                elif chosen_function == "2":
                    id_to_delete = input("Delete which id? ")
                    delete_user(conn, id_to_delete)
                    conn.commit()
                elif chosen_function == "3":
                    create_user_accounts(conn)

    except KeyboardInterrupt:
        print("\n\nProgram Terminated.\n\n")

    finally:    
        conn.close()


if __name__ == '__main__':
    main()