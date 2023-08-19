''' Importing Modules '''
from flask import Flask, redirect, render_template, Response, url_for,session, request, make_response
from flask_mysqldb import MySQL

''' Creating a Flask App '''
app = Flask(__name__)

''' Connecting Database '''
'''
Step 1: Create Database [here CRUD]
Step 2: Create Your tables [here Users]
 
drop table `CRUD`.`Users`;
CREATE TABLE `CRUD`.`Users` (
`id` INT( 8 ) NOT NULL AUTO_INCREMENT ,
`Fname` VARCHAR( 30 ) NOT NULL ,
`LName` VARCHAR( 30 ) NOT NULL ,
`Email` VARCHAR( 30 ) NOT NULL ,
`Password` VARCHAR( 30 ) NOT NULL ,
PRIMARY KEY ( `Email` ) ,
UNIQUE (
`id`
)
) ENGINE = MYISAM ;
Step 3: Set up MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
'''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='CRUD'

''' Connecting Flask App with MySQL '''
mysql = MySQL(app)

@app.route('/')  
def home():
    return render_template("index.html")  

@app.route('/signup')  
def signup():
    return render_template("register.html") 

@app.route('/signin')  
def signin():
    return render_template("login.html") 

'''
We have one registration page:register.html
     in register.html
     there is a form contains 4 feilds:-
     1) First Name=FName
     2) Last Name=LName
     3) Email= Email
     4) Password = Password
    
    Now when we will click, Signup button in
    registration page,then action will be ::/registration
    method is ::post
    
    Regitster.html -> form()-> /registration -> Database -> redirect to login.html
    
    '''

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
    print('Registration')
    try:
        if request.method == 'POST':
           FName = request.form['FName']
           LName = request.form['LName']
           Email=request.form['Email']
           Password = request.form['Password']
           confirm_password=request.form['Password']
           print(FName,LName,Email,Password,confirm_password)
           
           
           resp = make_response(render_template('login.html'))
           resp.set_cookie('Email', Email)
           resp.set_cookie('Password',Password)
           
           cur = mysql.connection.cursor()
           if Password==confirm_password:
               sql = "INSERT INTO users (FName, LName, Email, Password) VALUES (%s,%s,%s,%s)"
               val = (FName, LName,Email,Password)
               cur.execute(sql, val)
               cur.close()
           else:
               return render_template('register.html')
                
           return render_template('login.html')
    except:
        return render_template('register.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    
    print("0")
    try:
        if request.method == 'POST':
           print("1")
           email=request.form['email']   
           print("2")
           password = request.form['password']
           print("3")
           print(email,password)
           resp = make_response(render_template('login.html'))
           resp.set_cookie('email', email)
           resp.set_cookie('Password',password)
           
           
           cur = mysql.connection.cursor()
           sql = "SELECT * FROM users WHERE email=%s and password=%s"
           val = (email,password)
           cur.execute(sql, val)
           
           fetchdata=cur.fetchall()
           print(fetchdata)
           cur.close()
           if len(fetchdata)!=0:
               print("successful login")
               #session['email']=request.form['email']  
               return render_template('crud.html')
           return resp
    except:
        print("login failed")
        return render_template('login.html')
    
    
if __name__ == '__main__':
    app.run(threaded=True)
