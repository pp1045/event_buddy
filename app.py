# import mysql.connector,sys
# import datetime
# from mysql.connector import Error
# from flask import Flask, request, jsonify, render_template,redirect, url_for
# from random import randint


# app = Flask(__name__)


# @app.route('/',methods=['GET', 'POST'])
# def renderLoginPage():
#     events = runQuery("SELECT * FROM events")
#     branch =  runQuery("SELECT * FROM branch")
#     if request.method == 'POST':
#         Name = request.form['FirstName'] + " " + request.form['LastName']
#         Mobile = request.form['MobileNumber']
#         Branch_id = request.form['Branch']
#         Event = request.form['Event']
#         Email = request.form['Email']

#         if len(Mobile) != 10:
#             return render_template('loginfail.html',errors = ["Invalid Mobile Number!"])

#         if Email[-4:] != '.com':
#             return render_template('loginfail.html', errors = ["Invalid Email!"])

#         if len(runQuery("SELECT * FROM participants WHERE event_id={} AND mobile={}".format(Event,Mobile))) > 0 :
#             return render_template('loginfail.html', errors = ["Student already Registered for the Event!"])

#         if runQuery("SELECT COUNT(*) FROM participants WHERE event_id={}".format(Event)) >= runQuery("SELECT participants FROM events WHERE event_id={}".format(Event)):
#             return render_template('loginfail.html', errors = ["Participants count fullfilled Already!"])

#         runQuery("INSERT INTO participants(event_id,fullname,email,mobile,college,branch_id) VALUES({},\"{}\",\"{}\",\"{}\",\"COEP\",\"{}\");".format(Event,Name,Email,Mobile,Branch_id))

#         return render_template('index.html',events = events,branchs = branch,errors=["Succesfully Registered!"])

#     return render_template('index.html',events = events,branchs = branch)
    


# @app.route('/loginfail',methods=['GET'])
# def renderLoginFail():
#     return render_template('loginfail.html')


# @app.route('/admin', methods=['GET', 'POST'])
# def renderAdmin():
#     if request.method == 'POST':
#         UN = request.form['username']
#         PS = request.form['password']

#         cred = runQuery("SELECT * FROM admin")
#         print(cred)
#         for user in cred:
#             if UN==user[0] and PS==user[1]:
#                 return redirect('/eventType')

#         return render_template('admin.html',errors=["Wrong Username/Password"])

#     return render_template('admin.html')    



# @app.route('/eventType',methods=['GET','POST'])
# def getEvents():
#     eventTypes = runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE T.type_id IN (SELECT type_id FROM events AS E WHERE E.event_id = P.event_id ) ) AS COUNT FROM event_type AS T;") 

#     events = runQuery("SELECT event_id,event_title,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E;")

#     types = runQuery("SELECT * FROM event_type;")

#     location = runQuery("SELECT * FROM location")


#     if request.method == "POST":
#         try:

#             Name = request.form["newEvent"]
#             fee=request.form["Fee"]
#             participants = request.form["maxP"]
#             Type=request.form["EventType"]
#             Location = request.form["EventLocation"]
#             Date = request.form['Date']
#             runQuery("INSERT INTO events(event_title,event_price,participants,type_id,location_id,date) VALUES(\"{}\",{},{},{},{},\'{}\');".format(Name,fee,participants,Type, Location,Date))

#         except:
#             EventId=request.form["EventId"]
#             runQuery("DELETE FROM events WHERE event_id={}".format(EventId))

#     return render_template('events.html',events = events,eventTypes = eventTypes,types = types,locations = location) 


# @app.route('/eventinfo')
# def rendereventinfo():
#     events=runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E LEFT JOIN event_type USING(type_id) LEFT JOIN location USING(location_id);")

#     return render_template('events_info.html',events = events)

# @app.route('/participants',methods=['GET','POST'])
# def renderParticipants():
    
#     events = runQuery("SELECT * FROM events;")

#     if request.method == "POST":
#         Event = request.form['Event']

#         participants = runQuery("SELECT p_id,fullname,mobile,email FROM participants WHERE event_id={}".format(Event))
#         return render_template('participants.html',events = events,participants=participants)

#     return render_template('participants.html',events = events)

# def runQuery(query):

#     try:
#         db = mysql.connector.connect( host='localhost',database='event_mgmt',user='root',password='root')

#         if db.is_connected():
#             print("Connected to MySQL, running query: ", query)
#             cursor = db.cursor(buffered = True)
#             cursor.execute(query)
#             db.commit()
#             res = None
#             try:
#                 res = cursor.fetchall()
#             except Exception as e:
#                 print("Query returned nothing, ", e)
#                 return []
#             return res

#     except Exception as e:
#         print(e)
#         return []

#     db.close()

#     print("Couldn't connect to MySQL")
#     return None


# if __name__ == "__main__":
#     app.run() 


import psycopg2
import sys
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for
from random import randint
import stripe

app = Flask(__name__)



def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="root",
            host="localhost",
            port="5433",
            database="postgres"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

@app.route('/', methods=['GET', 'POST'])
def renderLoginPage():
    events = runQuery("SELECT * FROM events")
    branch = runQuery("SELECT * FROM branch")
    if request.method == 'POST':
        Name = request.form['FirstName'] + " " + request.form['LastName']
        Mobile = request.form['MobileNumber']
        Branch_id = request.form['Branch']
        Event = request.form['Event']
        print("Event_name",Event)
        Email = request.form['Email']

        

        if len(Mobile) != 10:
            return render_template('loginfail.html', errors=["Invalid Mobile Number!"])

        if not Email.endswith('.com'):
            return render_template('loginfail.html', errors=["Invalid Email!"])

        if len(runQuery("SELECT * FROM participants WHERE event_id=%s AND mobile=%s", (Event, Mobile))) > 0:
            return render_template('loginfail.html', errors=["Student already Registered for the Event!"])

        if runQuery("SELECT COUNT(*) FROM participants WHERE event_id=%s", (Event,)) >= runQuery(
                "SELECT participants FROM events WHERE event_id=%s", (Event,)):
            return render_template('loginfail.html', errors=["Participants count fulfilled Already!"])
        
        try:
            

            runQuery("INSERT INTO participants(event_id,fullname,email,mobile,college,branch_id) VALUES(%s,%s,%s,%s,%s,%s)",
                    (Event, Name, Email, Mobile, 'COEP', Branch_id))

            return render_template('index.html', events=events, branchs=branch, errors=[f"Successfully Registered!"])

        except stripe.error.CardError as e:
            # Payment failed, display error message to user
            return render_template('loginfail.html', errors=[e.error.message])

    return render_template('index.html', events=events, branchs=branch)


@app.route('/loginfail', methods=['GET'])
def renderLoginFail():
    return render_template('loginfail.html')


@app.route('/admin', methods=['GET', 'POST'])
def renderAdmin():
    if request.method == 'POST':
        UN = request.form['username']
        PS = request.form['password']

        cred = runQuery("SELECT * FROM admin")
        print(cred)
        for user in cred:
            if UN == user[0] and PS == user[1]:
                return redirect('/eventType')

        return render_template('admin.html', errors=["Wrong Username/Password"])

    return render_template('admin.html')


@app.route('/eventType', methods=['GET', 'POST'])
def getEvents():
    eventTypes = runQuery(
        "SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE T.type_id IN (SELECT type_id FROM events AS E WHERE E.event_id = P.event_id ) ) AS COUNT FROM event_type AS T;")

    events = runQuery(
        "SELECT event_id,event_title,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E;")

    types = runQuery("SELECT * FROM event_type;")

    location = runQuery("SELECT * FROM location")

    if request.method == "POST":
        try:

            Name = request.form["newEvent"]
            fee = request.form["Fee"]
            participants = request.form["maxP"]
            Type = request.form["EventType"]
            Location = request.form["EventLocation"]
            Date = request.form['Date']
            runQuery(
                "INSERT INTO events(event_title,event_price,participants,type_id,location_id,date) VALUES(%s, %s, %s, %s, %s, %s)",
                (Name, fee, participants, Type, Location, Date))

        except:
            EventId = request.form["EventId"]
            runQuery("DELETE FROM events WHERE event_id=%s", (EventId,))

    return render_template('events.html', events=events, eventTypes=eventTypes, types=types, locations=location)


@app.route('/eventinfo')
def render_event_info():
    events = runQuery(
        "SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E LEFT JOIN event_type USING(type_id) LEFT JOIN location USING(location_id);")

    return render_template('events_info.html', events=events)


@app.route('/participants', methods=['GET', 'POST'])
def renderParticipants():
    events = runQuery("SELECT * FROM events;")

    if request.method == "POST":
        Event = request.form['Event']

        participants = runQuery("SELECT p_id,fullname,mobile,email FROM participants WHERE event_id=%s", (Event,))
        return render_template('participants.html', events=events, participants=participants)

    return render_template('participants.html', events=events)


def runQuery(query, data=None):
    try:
        connection = connect_to_postgres()
        if connection is not None:
            cursor = connection.cursor()
            print("Connected to PostgreSQL, running query: ", query)
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            if 'SELECT' in query:
                res = cursor.fetchall()
                # print("query res",res)
                return res
            else:
                connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    app.run()