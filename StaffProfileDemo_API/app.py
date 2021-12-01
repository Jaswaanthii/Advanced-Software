
import urllib

from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from advisor import Advisor
from manager import Manager
from text import Text
from video import Video
from project import Project
from staffproject import StaffProject
from clientservice import ClientService
from contract import Contract

import requests  # for API example
import urllib.parse  # for API example

mysql = MySQL()

# initializing a variable of Flask
app = Flask(__name__, template_folder="templates")

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'data_staff'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

the_list = []  # a list of StaffProject objects


@app.route('/enternewmanager')
def new_manager():
    return render_template('new_manager.html')


@app.route('/enternewadvisor')
def new_advisor():
    return render_template('new_advisor.html')


@app.route('/updatenew')
def update_user():
    return render_template('update.html')


@app.route('/remove')
def remove_user():
    return render_template('remove.html')


@app.route('/getclients')
def get_clients():
    names = ""
    # ClientAPI to find clients details --------------------------------------------------------------------
    clients = ClientService.get_clients()
    for client in clients:
        name = client['client']
        names = names + " " + name
    print("get a list of clients via API ")
    # ------------------------------------------------------------------------------------------------------
    return render_template("index.html", names=names)


@app.route("/staff", methods=['GET'])
def get_staff():
    names = ""
    try:
        con = mysql.connect()  # set up database connection
        cur = con.cursor()
    except:
        con.rollback()
    finally:
        cur.execute('SELECT staff.username, staff.email, staff.start_date, staff.role, '
                    'profile.type, staff_project.project, contract.pay '
                    'FROM staff, profile, staff_project, contract '
                    'WHERE staff.username = profile.username AND '
                    'staff.username = staff_project.username AND '
                    'staff.username = contract.username')
        rows = cur.fetchall()
        con.commit()

        return render_template("index.html", rows=rows, names=names)
        con.close()


@app.route('/register_advisor', methods=['POST', 'GET'])
def register_advisor():
    if request.method == 'POST':
        con = mysql.connect()  # set up database connection
        cur = con.cursor()
        rows = []
        address = ""
        try:
            print("--------------------------Demo Start-------------------------------------------------------")
            username = request.form['username']  # retrieve form data
            email = request.form['email']
            start_year = request.form['start_year']
            remote = request.form['remote']
            profile_type = request.form['profile']
            project = request.form['project']
            contract_pay = float(request.form['pay'])

            """
            # API to find location details --------------------------------------------------------------------
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(remote) + '?format=json'
            response = requests.get(url).json()
            print("" + str(response[0]))  # response details
            address = response[0]["display_name"]  # retrieve response details form the attribute, display_name
            # -------------------------------------------------------------------------------------------------
            """
            staff = Advisor()
            staff.set_user_name(username)
            staff.set_email(email)
            staff.set_start_year(start_year)
            role = "advisor"
            staff.set_role(role)
            staff.set_remote(remote)

            if profile_type.lower() == "video":
                staff.set_profile(profile_type)
                video = Video()
                video.set_username(username)
                video.set_type(profile_type)
            elif profile_type.lower() == "text":
                staff.set_profile(profile_type)
                text = Text()
                text.set_username(username)
                text.set_type(profile_type)

            staff.set_contract(contract_pay)  # composition
            contract = Contract()
            contract.set_username(username)
            contract.set_pay(contract_pay)

            the_project = Project()  # set the Project
            the_project.set_name(project)

            staff_project = StaffProject()  # set the StaffProject
            staff_project.set_project(the_project)  # aggregation
            staff_project.set_staff(staff)  # aggregation

            the_list.append(staff_project)  # add to the list of StaffProject objects

            # insert data to the database
            cur.execute('INSERT INTO staff (username, email, start_date, role, remote)'
                        'VALUES( %s, %s, %s, %s, %s)',
                        (username, email, start_year, role, remote))
            con.commit()
            print("write to the staff table")

            cur.execute('INSERT INTO project (name)VALUES( %s)', project)  # note: name is primary key
            con.commit()
            print("write to the project table")

            cur.execute('INSERT INTO staff_project (username, project)VALUES( %s, %s)', (username, project))
            con.commit()
            print("write to the staff_project table")

            cur.execute('INSERT INTO contract (username, pay)VALUES( %s, %s)', (username, contract_pay))
            con.commit()
            print("write to the contract table")

            if profile_type.lower() == "video":
                time_limit = video.get_time_limit()
                cur.execute('INSERT INTO profile (username, type, time_limit)VALUES( %s, %s, %s)',
                            (username, profile_type, time_limit))
            elif profile_type.lower() == "text":
                word_limit = text.get_word_limit()
                cur.execute('INSERT INTO profile (username, type, word_limit)VALUES( %s, %s, %s)',
                            (username, profile_type, word_limit))
            con.commit()
            print("write to the profile table")

            # testing - retrieve data from the database
            cur.execute('SELECT staff.username, staff.email, staff.start_date, staff.role, '
                        'profile.type, staff_project.project, contract.pay '
                        'FROM staff, profile, staff_project, contract '
                        'WHERE staff.username = profile.username AND '
                        'staff.username = staff_project.username AND '
                        'staff.username = contract.username')
            rows = cur.fetchall()
            row_num = len(rows)
            print("staff:  ", row_num)
            for row in rows:
                print("username: ", row[0])
                print("email: ", row[1])

            con.commit()
            rows = rows
            return render_template("index.html", rows=rows, address=address)
        except:

            con.rollback()

        finally:
            rows = rows
            return render_template("index.html", rows=rows, address=address)
            con.close()


@app.route('/register_manager', methods=['POST', 'GET'])
def register_manager():
    if request.method == 'POST':
        rows = []
        try:
            print("--------------------------Demo Start-------------------------------------------------------")
            con = mysql.connect()  # set up database connection
            cur = con.cursor()
            username = request.form['username']  # retrieve form data
            email = request.form['email']
            start_year = request.form['start_year']
            bonus = float(request.form['bonus'])
            profile_type = request.form['profile']
            project = request.form['project']
            contract_pay = float(request.form['pay'])

            print("testing 02")
            staff = Manager()
            staff.set_user_name(username)
            staff.set_email(email)
            staff.set_start_year(start_year)
            role = "advisor"
            staff.set_role(role)
            staff.set_bonus(bonus)

            if profile_type.lower() == "video":
                staff.set_profile(profile_type)
                video = Video()
                video.set_username(username)
                video.set_type(profile_type)
            elif profile_type.lower() == "text":
                staff.set_profile(profile_type)
                text = Text()
                text.set_username(username)
                text.set_type(profile_type)

            staff.set_contract(contract_pay)  # composition
            contract = Contract()
            contract.set_username(username)
            contract.set_pay(contract_pay)

            the_project = Project()  # set the Project
            the_project.set_name(project)

            staff_project = StaffProject()  # set the StaffProject
            staff_project.set_project(the_project)  # aggregation
            staff_project.set_staff(staff)  # aggregation

            the_list.append(staff_project)  # add to the list of StaffProject objects

            # insert data to the database
            cur.execute('INSERT INTO staff (username, email, start_date, role, bonus)'
                        'VALUES( %s, %s, %s, %s, %s)',
                        (username, email, start_year, role, bonus))

            con.commit()
            print("write to the staff table")

            cur.execute('INSERT INTO project (name)VALUES( %s)', project)  # note: name is primary key
            con.commit()
            print("write to the project table")

            cur.execute('INSERT INTO staff_project (username, project)VALUES( %s, %s)', (username, project))
            con.commit()
            print("write to the staff_project table")

            cur.execute('INSERT INTO contract (username, pay)VALUES( %s, %s)', (username, contract_pay))
            con.commit()
            print("write to the contract table")

            if profile_type.lower() == "video":
                time_limit = video.get_time_limit()
                cur.execute('INSERT INTO profile (username, type, time_limit)VALUES( %s, %s, %s)',
                            (username, profile_type, time_limit))
            elif profile_type.lower() == "text":
                word_limit = text.get_word_limit()
                cur.execute('INSERT INTO profile (username, type, word_limit)VALUES( %s, %s, %s)',
                            (username, profile_type, word_limit))
            con.commit()
            print("write to the profile table")

            # testing - retrieve data from the database
            cur.execute('SELECT staff.username, staff.email, staff.start_date, staff.role, '
                        'profile.type, staff_project.project, contract.pay '
                        'FROM staff, profile, staff_project, contract '
                        'WHERE staff.username = profile.username AND '
                        'staff.username = staff_project.username AND '
                        'staff.username = contract.username')

            rows = cur.fetchall()
            row_num = len(rows)
            print("staff:  ", row_num)
            for row in rows:
                print("username: ", row[0])
                print("email: ", row[1])

            con.commit()
            rows = rows
            return render_template("index.html", rows=rows)
        except:

            con.rollback()

        finally:
            rows = rows
            return render_template("index.html", rows=rows)

            con.close()


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']

            con = mysql.connect()
            cur = con.cursor()
            cur.execute('UPDATE Staff SET email=%s WHERE username=%s', (email, username))
            con.commit()
            print("update the staff table")

            cur.execute('SELECT staff.username, staff.email, staff.start_date, staff.role, '
                        'profile.type, staff_project.project, contract.pay '
                        'FROM staff, profile, staff_project, contract '
                        'WHERE staff.username = profile.username AND '
                        'staff.username = staff_project.username AND '
                        'staff.username = contract.username')
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()

        finally:
            return render_template("index.html", rows=rows)
            con.close()


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            username = request.form['username']
            con = mysql.connect()
            cur = con.cursor()

            cur.execute('DELETE FROM Staff WHERE username=%s', username)
            con.commit()
            print("delete the staff from the staff table")

            cur.execute('DELETE FROM Profile WHERE username=%s', username)
            con.commit()
            print("delete the staff from the profile table")

            cur.execute('DELETE FROM Staff_Project WHERE username=%s', username)
            con.commit()
            print("delete the staff from the Staff_Project table")

            cur.execute('DELETE FROM Contract WHERE username=%s', username)
            con.commit()
            print("delete the staff from the contract table")

        except:
            con.rollback()

        finally:
            cur.execute('SELECT staff.username, staff.email, staff.start_date, staff.role, '
                        'profile.type, staff_project.project, contract.pay '
                        'FROM staff, profile, staff_project, contract '
                        'WHERE staff.username = profile.username AND '
                        'staff.username = staff_project.username AND '
                        'staff.username = contract.username')
            rows = cur.fetchall()
            con.commit()

            return render_template("index.html", rows=rows)
            con.close()


if __name__ == "__main__":
    app.run()
