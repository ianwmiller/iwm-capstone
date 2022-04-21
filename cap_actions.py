import csv
from random import choices
import sqlite3
import bcrypt
from datetime import *
connection = sqlite3.connect('capstone_db.db')
cursor = connection.cursor()




def view_comp(user_id):
    choice = []
    while True:
        comp_opt = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
        print('**** COMPETENCIES ****')
        print(f'{"ID":<4}{"Competency Name":<25}')
        for i in comp_opt:
            print(f'{i[0]:<4} {i[1]:<25}')
            choice.append(str(i[0]))
        comp_choice = input('Select the ID of the Competency you would like to see your competency level in (Press Enter to Exit):')
        if comp_choice == '':
            break
        elif comp_choice in choice:
            query = 'SELECT scale FROM User_Competency WHERE competency_id = ? and user_id = ?'
            values = (comp_choice, user_id)
            scale = cursor.execute(query, values).fetchall();
            print(f'You have a competency level of {scale[0][0]} in this Competency.')
            another = input('Would you like to view another? (Y/N):')
            if another == 'N' or another == 'n':
                break
            else: 
                continue
        else:
            print('Try again')





def view_assess(user_id):
    choice = []
    attempt_num = []
    while True:
        assessment_opt = cursor.execute('SELECT assessment_id, name FROM Assessments ').fetchall();
        print('**** ASSESSMENTS ****')
        print(f'{"ID":<4}{"Assessment Name":<25}')
        for i in assessment_opt:
            print(f'{i[0]:<4} {i[1]:<25}')
            choice.append(str(i[0]))
        assess_choice = input('Select the ID of the Assessment you would like to see your score on (Press Enter to Exit):')
        if assess_choice == '':
            break
        elif assess_choice in choice:
            query = 'SELECT result_id, date_taken FROM C_A_Results WHERE assessment_id = ? and user = ?'
            values = (assess_choice, user_id)
            indiv_assess = cursor.execute(query, values).fetchall();
            print(f'{"Attempt":<9}{"Date Taken":<20}')
            for i in indiv_assess:
                print(f'{i[0]:<9} {i[1]:<20}')
                attempt_num.append(str(i[0]))
            attempt_choice = input('Select the ID of the assessment attempt you would like to see your score for (Press Enter to Exit): ')
            if attempt_choice == '':
                break
            elif attempt_choice in attempt_num:
                query = 'SELECT score FROM C_A_Results WHERE result_id = ?'
                values = (attempt_choice,)
                score = cursor.execute(query, values).fetchall();
                print(f'You scored a {score[0][0]} on this Assessment.')
                another = input('Would you like to view another score? (Y/N):')
                if another == 'N' or another == 'n':
                    break
                else: 
                    continue
            else:
                print('Try again')
        else: print('Try again')





def edit_info(user_id):
    while True:
        query = 'SELECT first_name, last_name, email, password FROM Users WHERE user_id = ?'
        values = (user_id,)
        attributes = cursor.execute(query, values).fetchone()
        print('**** EDIT YOUR INFORMATION ****')
        print('(F)irst Name\n(L)ast Name\n(P)hone\n(E)mail\nPass(W)ord\n')
        edit_field = input('Select which of these you would like to edit (Press Enter to Exit): ')
        if edit_field == 'F' or edit_field == 'f':
            print(f'Current First Name: {attributes[0]}')
            new_first = input('Enter what you would like to change your name to: ')
            query = 'UPDATE Users SET first_name = ? WHERE user_id = ?'
            values = (new_first, user_id)
            cursor.execute(query, values)
            connection.commit()
        elif edit_field == 'L' or edit_field == 'l':
            print(f'Current Last Name: {attributes[1]}')
            new_last = input('Enter what you would like to change your last name to: ')
            query = 'UPDATE Users SET last_name = ? WHERE user_id = ?'
            values = (new_last, user_id)
            cursor.execute(query, values)
            connection.commit()
        elif edit_field == 'P' or edit_field == 'p':
            print(f'Current Phone Number: {attributes[2]}')
            new_phone = input('Enter what you would like to change your phone to: ')
            query = 'UPDATE Users SET phone = ? WHERE user_id = ?'
            values = (new_phone, user_id)
            cursor.execute(query, values)
            connection.commit()
        elif edit_field == 'E' or edit_field == 'e':
            print(f'Current Email: {attributes[3]}')
            new_email = input('Enter what you would like to change your email to: ')
            query = 'UPDATE Users SET email = ? WHERE user_id = ?'
            values = (new_email, user_id)
            cursor.execute(query, values)
            connection.commit()
        elif edit_field == 'W' or edit_field == 'w':
                user_password = input('Enter your current Password: ')
                user_password = user_password.encode()
                query = 'SELECT password FROM Users WHERE user_id = ?'
                value = (user_id,)
                db_password = cursor.execute(query, value).fetchone()
                hash_pass = db_password[0].encode()
                if bcrypt.checkpw(user_password,hash_pass):
                    new_pass = input('Enter what you would like to change your password to: ')
                    new_pass = new_pass.encode()
                    hash = bcrypt.hashpw(new_pass, bcrypt.gensalt())
                    hash = hash.decode()
                    query = 'UPDATE Users SET password = ? WHERE user_id = ?'
                    values = (hash, user_id)
                    cursor.execute(query, values)
                    connection.commit()
                else:
                    print('Wrong Password')
                    again = input('Try again? (Y/N):')
                    if again == 'Y' or again == 'y':
                        continue
                    else:
                        break
        elif edit_field == '':
            break
        else:
            print('Please Try again')
            continue











def manager_view():
    while True:
        view_opt = input("Select what you would like to view (Press Enter to Exit): \n[1] User Information\n[2] Competencies List for One User\n[3] All Users Competency Level in a Competency\n[4] Competency Levels of One User\n[5] Assessments List for One User: ")
        if view_opt == '':
            break
        elif view_opt == '1':
            rows = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
            print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<15} {row[2]:<15}')
            indepth = input('Press \'Y\' To see more information about a specific user(Press Enter to Exit): ')
            if indepth == 'Y' or indepth == 'y' or indepth == 'yes':
                first = input('Enter the First Name of the User you would like to see more information about: ')
                last = input('Enter the Last Name of the User you would like to see more information about: ')
                query = 'SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type FROM Users WHERE first_name = ? and last_name = ?'
                values = (first, last)
                rows = cursor.execute(query, values).fetchall();
                # can clean this up with better code since it will only be one row, too lazy rn though
                print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15} {"Phone":<15} {"Email":<30} {"On":<2} {"Date Created":<15} {"Hire Date":<15} {"Type":<8}')
                for row in rows:
                    print(f'{row[0]:<4} {row[1]:<15} {row[2]:<15} {row[3]:<15} {row[4]:<30} {row[5]:<2} {row[6]:<15} {row[7]:<15} {row[8]:<8}')
                    if type(row) == None:
                        print('None')
            else:
                break
        elif view_opt == '2':
            rows = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
            print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<15} {row[2]:<15}')
            users_comp = input('Enter the ID of the User who\'s List of Competencies you would like to see: ')
            query = 'SELECT c.name, uc.* FROM User_Competency uc LEFT OUTER JOIN Competencies c ON uc.competency_id = c.competency_id WHERE uc.user_id = ? AND scale IS NOT NULL'
            values = (users_comp, )
            list_of_comp = cursor.execute(query, values).fetchall();
            print(f'{"ID":<4} {"Name":<30} {"Score":<5}')
            for comp in list_of_comp:
                print(f'{comp[2]:<4} {comp[0]:<30} {comp[3]:<5}')

        elif view_opt == '3':
            rows = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
            print(f'{"ID":<4} {"Competency Name":<25}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<25}')
            which_comp = input('Enter the ID of the Competency you want to see all Competency Levels for: ')
            query = 'SELECT u.first_name, u.last_name, uc.* FROM User_Competency uc LEFT OUTER JOIN Users u ON uc.user_id = u.user_id WHERE uc.competency_id = ?'
            values = (which_comp, )
            all_users_comp = cursor.execute(query, values).fetchall();
            print(f'{"User":<30} {"Scale":<6}')
            for user in all_users_comp:
                print(f'{user[0]:<15} {user[1]:<15} {user[4]:<6}')

        elif view_opt == '4':
            rows = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
            print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<15} {row[2]:<15}')
            users_comp = input('Enter the ID of the User who\'s List of Competencies Level\'s you would like to see: ')
            query = 'SELECT c.name, uc.* FROM User_Competency uc LEFT OUTER JOIN Competencies c ON uc.competency_id = c.competency_id WHERE uc.user_id = ?'
            values = (users_comp, )
            list_of_comp = cursor.execute(query, values).fetchall();
            print(f'{"Name":<25} {"ID":<4} {"Scale":<6}')
            for comp in list_of_comp:
                print(f'{comp[0]:<25} {comp[2]:<4} {comp[3]:<6}')


        elif view_opt == '5':
            rows = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
            print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<15} {row[2]:<15}')
            users_assess = input('Enter the ID of the User who\'s List of Assessment Results you would like to see: ')
            query = 'SELECT a.name, car.* FROM C_A_Results car LEFT OUTER JOIN Assessments a ON car.assessment_id = a.assessment_id WHERE car.user = ?'
            values = (users_assess, )
            list_of_assess = cursor.execute(query, values).fetchall();
            print(f'{"Name":<45} {"Score":<6} {"Date Taken":<21} {"Proctor":<25} ')
            for assess in list_of_assess:
                print(f'{assess[0]:<45} {assess[2]:<6} {assess[3]:<21} {assess[4]:<25}')

        else:
            print('Sorry, Try Again')
            continue












def manager_add():
    while True:
        add_opt = input("Select what you would like to add (Press Enter to Exit): \n[1] User Information\n[2] New Competency\n[3] New Assessment to a Competency\n[4] Competency Level for a User\n[5] Assessment Result for a User for an Assessment: ")
        if add_opt == '':
            break
        elif add_opt == '1':
            while True:
                f_name = input('Enter User\'s first name: ')
                l_name = input('Enter User\'s last name: ')
                phone_num = input(f'Enter {f_name}\'s Phone Number: ')
                if phone_num == '':
                    phone_num = None
                email = input(f'Enter {f_name}\'s Email: ')
                passw = input(f'Enter {f_name}\'s password: ')
                passw = passw.encode()
                hash_pass = bcrypt.hashpw(passw, bcrypt.gensalt())
                hash_pass = hash_pass.decode()
                active = input(f'Is {f_name} currently acitve? (Y/N): ')
                if active == 'N' or active == 'n':
                    active = 0
                else:
                    active = 1
                d = datetime.today()
                date_created = d.date()
                hired_today = input('Was this person hired today? (Y/N):')
                if hired_today == 'Y' or 'y':
                    d = datetime.today()
                    hire_date = d.date()
                elif hired_today == 'N' or 'n':
                    year = input('Enter the 4 digit Year they were hired: ')
                    mon = input('Enter the 2 digit Month they were hired: ')
                    day = input('Enter the 2 digit Day they were hired: ')
                    date = [year, mon, day]
                    hire_date = "-".join(date)
                user_type = input(f'Is {f_name} a Manager? (Y/N): ')
                if user_type == 'Y' or user_type == 'y':
                    user_type = 'manager'
                else: 
                    user_type = 'user'
                

                query = 'INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) values(?, ?, ?, ?, ?, ?, ?, ?, ?)'
                values = (f_name, l_name, phone_num, email, hash_pass, active, date_created, hire_date, user_type)

                cursor.execute(query, values)
                connection.commit()
                print(f'SUCCESS: User \"{f_name}\" has been added!')   
                another = input('Would you like to add another User? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break


        elif add_opt == '2':
            while True:   
                name = input('Enter Name of Competency: ')
                d = datetime.today()
                date_created = d.date()

                query = 'INSERT INTO Competencies (name, date_created) values(?, ?)'
                values = (name, date_created)

                cursor.execute(query, values)
                connection.commit()
                print(f'SUCCESS: Competency \"{name}\" has been added!')   
                another = input('Would you like to add another Competency? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break


        elif add_opt == '3':
            while True:
                rows = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
                print(f'{"ID":<4} {"Competency Name":<25}')
                for row in rows:
                    print(f'{row[0]:<4} {row[1]:<25}')
                print('\n')
                comp = input('Enter the Competency ID of the Competency you are adding this Assessment to: ')
                
                name = input('Enter the Name of this New Assessment: ')
                d = datetime.today()
                date_created = d.date()
                query = 'INSERT INTO Assessments (competency_id, name, date_created) values(?, ?, ?)'
                values = (comp, name, date_created)

                cursor.execute(query, values)
                connection.commit()
                print(f'SUCCESS: Assessment \"{name}\" has been added!')   
                another = input('Would you like to add another Assessment? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break


        elif add_opt == '4':
            while True:
                users = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
                print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
                for user in users:
                    print(f'{user[0]:<4} {user[1]:<15} {user[2]:<15}')
                print('\n')
                id_of_user = input('Enter The User you want to Add a New Competency Level for: ')
                
                comps = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
                print(f'{"ID":<4} {"Competency Name":<25}')
                for comp in comps:
                    print(f'{comp[0]:<4} {comp[1]:<25}')
                print('\n')
                id_for_comp = input(f'Enter the ID of the Competency you want to Update The User\'s Competency Level for:')
                
                scale = input(f'Enter the New Competency Level for this Competency (0-4): ')
                query = 'INSERT INTO User_Competency (user_id, competency_id, scale) values(?, ?, ?)'
                values = (id_of_user, id_for_comp, scale)

                cursor.execute(query, values)
                connection.commit()
                print(f'SUCCESS: Competency Level for this User has been added!')   
                another = input('Would you like to add another User\'s Competency Level? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break
    
        elif add_opt == '5':
            while True:   
                assesses = cursor.execute('SELECT assessment_id, name FROM Assessments').fetchall();
                print(f'{"ID":<4} {"Assessment Name":<25}')
                for assess in assesses:
                    print(f'{assess[0]:<4} {assess[1]:<25}')
                print('\n')
                id_for_assess = input(f'Enter the ID of the Assessment you want to Add this score for:')

                users = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
                print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
                for user in users:
                    print(f'{user[0]:<4} {user[1]:<15} {user[2]:<15}')
                id_of_user = input('Enter The ID of the User who took the Assessment: ')
                id_of_proc = input('Enter The ID of the Proctor of this Assessment: ')

                score = input('Enter the Score of the Assessment: ')
                taken_when = input('Was this Assessment taken today? (Y/N): ')
                if taken_when == 'Y' or taken_when == 'y':
                    d = datetime.today()
                    date_taken = d.date()
                else:
                    year = input('Enter the 4 digit Year they were hired: ')
                    mon = input('Enter the 2 digit Month they were hired: ')
                    day = input('Enter the 2 digit Day they were hired: ')
                    date = [year, mon, day]
                    date_taken = "-".join(date)
                query = 'INSERT INTO C_A_Results (score, date_taken, user, manager, assessment_id) values(?, ?, ?, ?, ?)'
                values = (score, date_taken, id_of_user, id_of_proc, id_for_assess)

                cursor.execute(query, values)
                connection.commit()
                print(f'SUCCESS: Assessment Score has been added!')   
                another = input('Would you like to add another Assessment Score? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break














def manager_edit():
    while True:
        edit_opt = input("Select what you would like to Edit (Press Enter to Exit): \n[1] User Information\n[2] Competency Information\n[3] Assessment Information\n[4] Competency Level for a User\n[5] Assessment Result for a User for an Assessment: ")
        if edit_opt == '':
            break
        elif edit_opt == '1':
            while True:
                users = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
                print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
                for user in users:
                    print(f'{user[0]:<4} {user[1]:<15} {user[2]:<15}')
                id_choice = input('Enter the ID of the User who\'s information you want to edit: ')
                query = 'SELECT * FROM Users WHERE user_id = ?'
                values = (id_choice)
                attributes = cursor.execute(query, values).fetchall()
                print('(F)irst Name\n(L)ast Name\n(P)hone\n(E)mail\nPass(W)ord\n(A)ctive\n(D)ate Created\n(H)ire Date\n(U)ser Type')
                edit_field = input('Select which of these you would like to edit (Press Enter to Exit): ')
                if edit_field == 'F' or edit_field == 'f':
                    print(f'Current First Name: {attributes[0][1]}')
                    new_first = input('Enter what you would like to change your name to: ')
                    query = 'UPDATE Users SET first_name = ? WHERE user_id = ?'
                    values = (new_first, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'L' or edit_field == 'l':
                    print(f'Current Last Name: {attributes[0][2]}')
                    new_last = input('Enter what you would like to change your last name to: ')
                    query = 'UPDATE Users SET last_name = ? WHERE user_id = ?'
                    values = (new_last, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'P' or edit_field == 'p':
                    print(f'Current Phone Number: {attributes[0][3]}')
                    new_phone = input('Enter what you would like to change the phone to: ')
                    query = 'UPDATE Users SET phone = ? WHERE user_id = ?'
                    values = (new_phone, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'E' or edit_field == 'e':
                    print(f'Current Email: {attributes[0][4]}')
                    new_email = input('Enter what you would like to change the email to: ')
                    query = 'UPDATE Users SET email = ? WHERE user_id = ?'
                    values = (new_email, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'W' or edit_field == 'w':
                    user_password = input('Enter this User\'s Current Password: ')
                    user_password = user_password.encode()
                    query = 'SELECT password FROM Users WHERE user_id = ?'
                    value = (id_choice,)
                    db_password = cursor.execute(query, value).fetchone()
                    db_password = db_password[0].encode()
                    if bcrypt.checkpw(user_password,db_password):
                        new_pass = input('Enter what you would like to change this password to: ')
                        new_pass = new_pass.encode()
                        hash = bcrypt.hashpw(new_pass,bcrypt.gensalt())
                        hash_pass = hash.decode()
                        query = 'UPDATE Users SET password = ? WHERE user_id = ?'
                        values = (hash_pass, id_choice)
                        cursor.execute(query, values)
                        connection.commit()
                    else:
                        print('Wrong Password')
                        again = input('Try again? (Y/N):')
                        if again == 'Y' or again == 'y':
                            continue
                        else:
                            break
                elif edit_field == 'A' or edit_field == 'a':
                    print(f'Current Activity: {attributes[0][6]}')
                    new_active = input('Enter what you would like to change the Activity to(Y/N): ')
                    if new_active == 'N' or new_active == 'n':
                        new_active = 0
                    else: 
                        new_active = 1
                    query = 'UPDATE Users SET active = ? WHERE user_id = ?'
                    values = (new_active, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'D' or edit_field == 'd':
                    print(f'Current Creation Date: {attributes[0][7]}')
                    new_date = input('Enter what you would like to change the Creation Date to (YYYY-MM-DD): ')
                    query = 'UPDATE Users SET date_created = ? WHERE user_id = ?'
                    values = (new_date, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'H' or edit_field == 'h':
                    print(f'Current Hire Date: {attributes[0][8]}')
                    new_hire_day = input('Enter what you would like to change the Hire Date to (YYYY-MM-DD): ')
                    query = 'UPDATE Users SET hire_date = ? WHERE user_id = ?'
                    values = (new_hire_day, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == 'U' or edit_field == 'u':
                    print(f'Current User Type: {attributes[0][9]}')
                    new_u_type = input('Enter what you would like to change this User Type to: ')
                    query = 'UPDATE Users SET user_type = ? WHERE user_id = ?'
                    values = (new_u_type, id_choice)
                    cursor.execute(query, values)
                    connection.commit()
                elif edit_field == '':
                    break
                else:
                    print('Please Try again')
                    continue
                another = input('Would you like to edit another User? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break





        elif edit_opt == '2':
            while True:   
                rows = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
                print(f'{"ID":<4} {"Competency Name":<25}')
                for row in rows:
                    print(f'{row[0]:<4} {row[1]:<25}')
                print('\n')
                comp = input('Enter the Competency ID of the Competency you want to Edit: ')

                comp_piece = input('(N)ame\n(C)orrecting Creation Date\n\nEnter What part of this Competency you would like to Edit: ')
                if comp_piece == 'N' or comp_piece == 'n' or comp_piece == 'Name':
                    name = input('Enter the New Name for the Competency: ')
                    query = 'UPDATE Competencies SET name = ? WHERE competency_id = ?'
                    values = (name, comp)
                    cursor.execute(query, values)
                    connection.commit()
                    print(f'SUCCESS: Competency \"{name}\" has been added!')   
                    another = input('Would you like to add another Competency? (Y/N) ')
                    print('\n')
                    if another == 'Y' or another == 'y':
                        continue
                    else:
                        break
                elif comp_piece == 'C' or comp_piece == 'c' or comp_piece == 'creation date':
                    new_day = input('Enter the Correct Creation Date of the Competency\'s Creation (YYYY-MM-DD): ')
                    query = 'UPDATE Competencies SET date_created = ? WHERE competency_id = ?'
                    values = (new_day, comp)
                    cursor.execute(query, values)
                    connection.commit()
                    print(f'SUCCESS: Creation Date for Competency \"{comp}\" has been corrected!')   
                    another = input('Would you like to add another Competency? (Y/N) ')
                    print('\n')
                    if another == 'Y' or another == 'y':
                        continue
                    else:
                        break






        elif edit_opt == '3':
            while True:
                assesses = cursor.execute('SELECT assessment_id, name FROM Assessments').fetchall();
                print(f'{"ID":<4} {"Assessment Name":<25}')
                for assess in assesses:
                    print(f'{assess[0]:<4} {assess[1]:<25}')
                print('\n')
                new_assess = input('Enter the Assessment ID of the Assessment you are editing: ')

                assess_change = input('Select what you will edit about this Assessment:\n[I]D of Competency it Falls Under\n[N]ame\n[C]orrecting Creation Date')
                if assess_change == 'I' or assess_change == 'i':
                    rows = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
                    print(f'{"ID":<4} {"Competency Name":<25}')
                    for row in rows:
                        print(f'{row[0]:<4} {row[1]:<25}')
                    print('\n')
                    comp = input('Enter the Competency ID of the Competency you want to Add the Assessment to: ')
                    query = 'UPDATE Asssessments SET competency_id = ? WHERE assessment_id = ?'
                    values = (comp, new_assess)
                    cursor.execute(query, values)
                    connection.commit()
                    print(f'SUCCESS: The Assessment has been added to a new Competency!')
                    another = input('Would you like to edit another Assessment? (Y/N) ')
                    print('\n')
                    if another == 'Y' or another == 'y':
                        continue
                    else:
                        break

                elif assess_change == 'N' or assess_change == 'n':
                    name = input('Enter the New Name of this Assessment: ')
                    query = 'UPDATE Asssessments SET name = ? WHERE assessment_id = ?'
                    values = (name, new_assess)
                    cursor.execute(query, values)
                    connection.commit()
                    print(f'SUCCESS: The Assessment\'s name has been changed!')
                    another = input('Would you like to edit another Assessment? (Y/N) ')
                    print('\n')
                    if another == 'Y' or another == 'y':
                        continue
                    else:
                        break

                elif assess_change == 'C' or assess_change == 'c':
                    new_date = input('Enter the Correct Creation Date of this Assessment (YYYY-MM-DD): ')
                    query = 'UPDATE Asssessments SET date_created = ? WHERE assessment_id = ?'
                    values = (new_date, new_assess)
                    cursor.execute(query, values)
                    connection.commit()
                    print(f'SUCCESS: The Assessment\'s Creation Date has been corrected!')
                    another = input('Would you like to edit another Assessment? (Y/N) ')
                    print('\n')
                    if another == 'Y' or another == 'y':
                        continue
                    else:
                        break






        elif edit_opt == '4':
            while True:
                users = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
                print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
                for user in users:
                    print(f'{user[0]:<4} {user[1]:<15} {user[2]:<15}')
                print('\n')
                id_of_user = input('Enter The User you want to Edit a Competency Level for: ')
                
                comps = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
                print(f'{"ID":<4} {"Competency Name":<25}')
                for comp in comps:
                    print(f'{row[0]:<4} {row[1]:<25}')
                print('\n')
                id_for_comp = input(f'Enter the ID of the Competency you want to Update The User\'s Competency Level for:')
                
                scale = input(f'Enter the New Competency Level for this Competency (0-4): ')
                query = 'UPDATE User_Competency SET scale = ? WHERE user_id = ? AND competency_id = ?'
                values = (scale, id_of_user, id_for_comp)

                cursor.execute(query, values)
                connection.commit()
                print(f'SUCCESS: Competency Level for this User has been changed!')   
                another = input('Would you like to edit another User\'s Competency Level? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break
    



        elif edit_opt == '5':
            while True:   
                assesses = cursor.execute('SELECT assessment_id, name FROM Assessments').fetchall();
                print(f'{"ID":<4} {"Assessment Name":<25}')
                for assess in assesses:
                    print(f'{assess[0]:<4} {assess[1]:<25}')
                print('\n')
                id_for_assess = input(f'Enter the ID of the Assessment you want to Edit the score for:')

                users = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
                print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
                for user in users:
                    print(f'{user[0]:<4} {user[1]:<15} {user[2]:<15}')
                print('\n')
                id_of_user = input('Enter The ID of the User who\'s Result you are Editing: ')

                query = 'SELECT result_id, date_taken, score FROM C_A_Results WHERE assessment_id = ? AND user = ?'
                values = (id_for_assess, id_of_user)
                results = cursor.execute(query, values).fetchall();
                print(f'{"ID":<4} {"Date Taken":<21} {"Score":<6}')
                for result in results:
                    print(f'{result[0]:<4} {result[1]:<21} {result[2]:<6}')
                print('\n')
                id_of_result = input('Enter the ID of the Result you will change the score for: ')
                score = input('Enter the new Score of the Assessment Attempt: ')

                query = 'UPDATE C_A_Results SET score =? WHERE result_id = ?'
                values = (score, id_of_result)
                cursor.execute(query, values)
                connection.commit()

                print(f'SUCCESS: Assessment Score has been changed!')   
                another = input('Would you like to edit another Assessment Score? (Y/N) ')
                print('\n')
                if another == 'Y' or another == 'y':
                    continue
                else:
                    break










def manager_delete():
    while True:
        users = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
        print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
        for user in users:
            print(f'{user[0]:<4} {user[1]:<15} {user[2]:<15}')
        print('\n')
        id_of_user = input('Enter The User you want to remove an Assessment Score for: ')
        query = 'SELECT car.result_id, a.name, car.score, car.date_taken FROM C_A_Results car LEFT OUTER JOIN Assessments a ON car.assessment_id = a.assessment_id WHERE car.user = ?'
        values = (id_of_user, )
        list_of_assess = cursor.execute(query, values).fetchall();
        print(f'{"Result ID":<10} {"Assessment Name":<45} {"Score":<6} {"Date Taken":<21}')
        for assess in list_of_assess:
            print(f'{assess[0]:<10} {assess[1]:<45} {assess[2]:<6} {assess[3]:<21}')
        delete_id = input("Select the Result ID you would like to Delete for this User: ")
        delete_conf = input(f'Do you REALLY want to DELETE Result ID {delete_id}? (Y/N): ')
        if delete_conf == 'Y' or delete_conf == 'y':
            del_query = 'DELETE FROM C_A_Results WHERE result_id = ?'
            del_value = (delete_id)
            cursor.execute(del_query,del_value)
            connection.commit()
            print(f'SUCCESS: Assessment Score has been deleted!')   
        else: 
            break
        another = input('Would you like to delete another Assessment Score? (Y/N) ')
        print('\n')
        if another == 'Y' or another == 'y':
            continue
        else:
            break




def manager_csv():
    while True:
        csv_opt = input("Select what you would like to do with the CSV File (Press Enter to Exit): \n[1] Export User List to CSV File\n[2] Export Competency Information to CSV File\n[3] Export User Competency Summary (All Competency levels for a Single User)\n[4]Competency Results Summary (All Users Competency Levels for a Single Competency)\n[5]Import Information from CSV File: ")
        if csv_opt == '':
            break
        elif csv_opt =='1':
            header_fields = ['First Name', 'Last Name', 'Phone Number', 'Email', 'Hire Date', 'User Type']
            rows = cursor.execute('SELECT first_name, last_name, phone, email, hire_date, user_type FROM Users')
            with open('capstone.csv', 'w') as outfile:
                wrt = csv.writer(outfile)
                wrt.writerow(header_fields)        
                wrt.writerows(rows)
            print('EXPORT SUCCESSFUL')
        elif csv_opt =='2':
            header_fields = ['Competency Name', 'Date Created']
            rows = cursor.execute('SELECT name, date_created FROM Competencies')
            with open('capstone.csv', 'w') as outfile:
                wrt = csv.writer(outfile)
                wrt.writerow(header_fields)        
                wrt.writerows(rows)
            print('EXPORT SUCCESSFUL')
        elif csv_opt == '3':
            rows = cursor.execute('SELECT user_id, first_name, last_name FROM Users').fetchall();
            print(f'{"ID":<4} {"First Name":<15} {"Last Name":<15}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<15} {row[2]:<15}')
            users_comp = input('Enter the ID of the User who\'s List of Competencies you would like to see: ')
            query = 'SELECT c.name, uc.competency_id, uc.scale FROM User_Competency uc LEFT OUTER JOIN Competencies c ON uc.competency_id = c.competency_id WHERE uc.user_id = ? AND scale IS NOT NULL'
            values = (users_comp, )
            list_of_comp = cursor.execute(query, values).fetchall();
            query = 'SELECT a.name, a.assessment_id, a.competency_id, car.score FROM Assessments a LEFT OUTER JOIN C_A_Results car ON a.assessment_id = car.assessment_id WHERE car.user = ? AND score IS NOT NULL'
            values = (users_comp, )
            list_of_comp_two = cursor.execute(query, values).fetchall();
            header_fields_one =["Competenecy Name", "Competency ID", "Competency Level"]
            header_fields_two =["Assessment Name", "Assessment ID","Competency ID", "Assessment Score"]
            with open('capstone.csv', 'w') as outfile:
                wrt = csv.writer(outfile)
                wrt.writerow(header_fields_one)        
                wrt.writerows(list_of_comp)
                wrt.writerow(header_fields_two)        
                wrt.writerows(list_of_comp_two)
            print('EXPORT SUCCESSFUL')
        elif csv_opt == '4':
            rows = cursor.execute('SELECT competency_id, name FROM Competencies').fetchall();
            print(f'{"ID":<4} {"Competency Name":<25}')
            for row in rows:
                print(f'{row[0]:<4} {row[1]:<25}')
            which_comp = input('Enter the ID of the Competency you want to see all Competency Levels for: ')
            query = 'SELECT u.first_name, u.last_name, uc.competency_id, uc.scale FROM User_Competency uc LEFT OUTER JOIN Users u ON uc.user_id = u.user_id WHERE uc.competency_id = ?'
            values = (which_comp, )
            all_users_comp = cursor.execute(query, values).fetchall();
            query = 'SELECT a.name, a.assessment_id, car.user, car.score FROM Assessments a LEFT OUTER JOIN C_A_Results car ON a.assessment_id = car.assessment_id WHERE a.competency_id = ?'
            values = (which_comp, )
            all_users_comp_two = cursor.execute(query, values).fetchall();
            header_fields_one = ["First Name", "Last Name",f"Competency: {rows[int(which_comp)][1]}", "Scale"]
            header_fields_two =["Assessment Name", "Assessment ID","User ID", "Assessment Score"]
            with open('capstone.csv', 'w') as outfile:
                wrt = csv.writer(outfile)
                wrt.writerow(header_fields_one)        
                wrt.writerows(all_users_comp)
                wrt.writerow(header_fields_two)        
                wrt.writerows(all_users_comp_two)
            print('EXPORT SUCCESSFUL')
        elif csv_opt =='5':
            with open('capstone.csv', 'r') as csvfile:
                header = csvfile.readline()
                splitting = header.strip('\n').split(',')
                print(f'{splitting}\n')
                for line in csvfile:
                    words = line.strip('\n').split(',')
                    print(f'{words}\n')
