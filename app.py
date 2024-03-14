import re,os,sqlite3
from flask import Flask, render_template,flash,redirect, url_for
from forms import LoginForm, RegistrationForm
from flask import request,session,g
from datetime import datetime
from flask_migrate import Migrate,migrate
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash



app =Flask(__name__)

app.config['SECRET_KEY'] = 'e70ecafe2896f60c78693f421d67f79e'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

# @app.teardown_appcontext
# def close_database(error):
#     if hasattr(g, 'mysql'):
#         g.mysql.close()
#     return g.mysql




def get_current_user():
    user = None

    if 'user' in session:
        user = session['user']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registration WHERE username =%s',[user])
        user = cur.fetchone()

    return user




@app.route("/home")
def home():
    user = get_current_user() 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registration')
    fetchdata = cur.fetchall()
    cur.close()
    return render_template ('layout.html',title="homepage", user=user,data=fetchdata)

@app.route("/about")
def about():
    return render_template("layout.html",title="about")

@app.route("/login" ,methods=["POST","GET"])
def login():
    error = None
    user = get_current_user()
    if request.method =='POST':
        username = request.form.get('name')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registration WHERE username = %s ',[username])
        user = cur.fetchall()
        hashed_password = ""

        if len(user) == 1:
            for record in user:

                hashed_password = str(record[3])
        
        if user :
            if check_password_hash(hashed_password,password):
                session['user'] = username
                return redirect(url_for('home', user=user))
            else:
                error = "Password do not match"


        mysql.connection.commit()
        cur.close()


    return render_template('login.html', title='login',loginerror=error,user=user)

@app.route("/", methods=['GET','POST'])
def register():
    error = None
    user = get_current_user() 
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        hashed_password = generate_password_hash(password)
        hashed_confirm_password = generate_password_hash(confirm_password)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registration where username= %s', [username])
        existing_username = cur.fetchone()

        if existing_username:
            return redirect(url_for('register', registererror = 'username already taken , try a different username!'))
        
        # Save data to the database
        cur.execute('INSERT INTO registration (username, email , password, confirm_password ) VALUES (%s, %s,%s,%s)', (username, email, hashed_password, hashed_confirm_password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home',user=user))
    
    return render_template('signup.html', title='Register', registrationerror=error)
@app.route('/profile', methods=["POST","GET"])
def profile():
    user = get_current_user()
    if request.method == 'GET':
       cur = mysql.connection.cursor()
       cur.execute('SELECT * FROM employees')
       employees = cur.fetchall()
       data = employees
       
    # if len(data) == 1:
    #         for recor in data:
    #             return recor

                
      
    return render_template('profile.html',user=user,profiledata=data)

@app.route('/new', methods=['GET','POST'])
def new():
    user=get_current_user()
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        date = request.form.get('date')
        num = request.form.get('num')
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        num3 = request.form.get('num3')
        department = request.form.get('department')
        profession = request.form.get('profession')
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO employees (username,email,phone,address,joining_date,total_projects,total_test_case,total_defects_found,total_defects_pending, department, profession)(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
        (username,email,phone,address,date,num,num1,num2,num3,department,profession))
        mysql.connection.commit()
        return redirect('profile')


    return render_template('add_new_employee.html',user=user)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
    