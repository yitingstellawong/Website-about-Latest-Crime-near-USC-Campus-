# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 00:37:56 2022

@author: ThinkBook
"""

from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import closing

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'stella0902'
app.config['MYSQL_DATABASE_DB'] = 'incidents'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# set a secret key for the session
app.secret_key = 'why would I tell you my secret key?'

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        with closing(mysql.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                _hash_password = generate_password_hash(_password) 
        
                cursor.callproc('sp_createUser',(_name,_email,_password))
                data = cursor.fetchall()
                
                if len(data) == 0:
                    conn.commit()
                    return json.dumps({'message':'User created successfully !'})
                else:
                    return json.dumps({'error':str(data[0])})  
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})     


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin', methods = ['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        session['user'] = _username
        return redirect('/userHome')
        
    #except Exception as e:
        #return render_template('error.html',error=str(e))
    finally:
        cursor.close()
        con.close()

    

@app.route('/userHome', methods = ['GET', 'POST'])
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/showAddIncidents')
def showAddIncidents():
    return render_template('addIncidents.html')

@app.route('/addIncidents', methods = ['POST'])
def addIncidents():
    if request.method == 'POST':
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _date = request.form['date']
            _location = request.form['location']
            _vehicle = request.form['vehicle']
            _incident = request.form['incident']
            _suspect = request.form['suspect']
            
            with closing(mysql.connect()) as conn:
                 with closing(conn.cursor()) as cursor:
                     cursor.callproc('sp_addIncidents',(_user, _title, _date, _location, _vehicle, _incident, _suspect))
                     data = cursor.fetchall()
 
                     if len(data) == 0:
                         conn.commit()
                         return redirect('/getIncidents')
                     else:
                         return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')


@app.route('/getIncidents', methods = ['GET'])
def getIncidents():
    if request.method == 'GET':
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetIncidentsByUser',(_user,))
            incidents = cursor.fetchall()
 
            incidents_lst = []
            for i in incidents:
                incident_dict = {
                        'User_id': i[0],
                        'Report Offense': i[1],
                        'Date & Time of Occurrence': i[2],
                        'Location': i[3],
                        'Vehicle Description': i[4],
                        'Incident Description': i[5],
                        'Suspect Description': i[6]}
                incidents_lst.append(incident_dict)
 
            return json.dumps(incidents_lst)
        else:
            return render_template('error.html', error = 'Unauthorized Access')

@app.route('/showIncidents', methods = ['GET'])
def showIncidents():
    if request.method == 'GET':
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_GetAllIncidents')
        incidents = cursor.fetchall()
        
        incidents_lst = []
        for i in incidents:
            incident_dict = {
                        'Report Offense': i[0],
                        'Date & Time of Occurrence': i[1],
                        'Location': i[2],
                        'Vehicle Description': i[3],
                        'Incident Description': i[4],
                        'Suspect Description': i[5]}
            incidents_lst.append(incident_dict)
        
        json_object = json.dumps(incidents_lst, indent = 4)
        return json_object
 
        

if __name__ == "__main__":
    app.run(port = 551, debug = True)
    
#http://localhost:551/
    
    
    
    
    
    
    