from cap_actions import *
import bcrypt
import sqlite3
connection = sqlite3.connect('capstone_db.db')
cursor = connection.cursor()

while True:
    print('WELCOME TO THE CAPSTONE PROJECT')
    user_email = input('Email: ')
    query = 'SELECT user_id, first_name FROM Users WHERE email = ?'
    values = (user_email,)
    account = cursor.execute(query,values).fetchall()
    for piece in account:
        print(f'Welcome {piece[1]}')
    user_password = input('Password: ')
    user_password = user_password.encode()
    query = 'SELECT password FROM Users WHERE user_id = ?'
    for piece in account:
        value = (piece[0],)
    db_password = cursor.execute(query, value).fetchone()
    db_password = db_password[0].encode()
    if bcrypt.checkpw(user_password,db_password):
        query = 'SELECT user_type FROM Users WHERE user_id = ?'
        for piece in account:
            value = (piece[0],)
        user_type = cursor.execute(query,value).fetchone()
        while True:
            if user_type[0] == 'user':
                    print("**** USER MENU **** \n")
                    db_choice = input("Select the option you would like: \n[1] View Competencies\n[2] View Assessment Data\n[3] Edit Your Info\n[L] Logout\n")
                    if db_choice == '1':
                        for piece in account:
                            view_comp(piece[0])
                    elif db_choice == '2':
                        for piece in account:
                            view_assess(piece[0])
                    elif db_choice == '3':
                        for piece in account:
                            edit_info(piece[0])
                    elif db_choice == 'L' or db_choice == 'l':
                        other = input('Would you Like to login with a different account? (Y/N):')
                        if other == 'Y' or other =='y':
                            break
                        else:
                            exit()
                    else:
                        print('Try Again!')

            elif user_type[0] == 'manager':
                    print("**** MANAGER MENU **** \n")
                    db_choice = input("Select the option you would like: \n[1] View Information\n[2] Edit Information\n[3] Add Information\n[4] Delete Assessment Result\n[5] Transfer Data through a CSV File\n[L] Logout\n")
                    if db_choice == '1':
                        manager_view()
                    elif db_choice == '2':
                        manager_edit()
                    elif db_choice == '3':
                        manager_add()
                    elif db_choice == '4':
                        manager_delete()
                    elif db_choice == '5':
                        manager_csv()
                    elif db_choice == 'L' or db_choice == 'l':
                        other = input('Would you Like to login with a different account? (Y/N):')
                        if other == 'Y' or other =='y':
                            break
                        else:
                            exit()
                    else:
                        print('Try Again!')
            else:
                print('Try again')
                break
    else:
        print('Incorrect Username or Password')
        again = input('Do you want to Try Again? (Y/N): ')
        if again == 'Y' or again == 'y':
            continue
        else:
            break