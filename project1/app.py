from flask import Flask, request, session, jsonify, render_template, url_for, flash, redirect
# from flask.ext.wtf import Form
from wtforms import RadioField, Form
import psycopg2 as psql
import os
from forms import UserRegistrationForm, LoginForm, BookIssuesForm
# from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_login import login_required,login_manager
from functools import wraps
from flask_login import LoginManager


# login_manager = LoginManager()
# login_manager.init_app(app)


SECRET_KEY='development'
# 

psql.extensions.register_type(psql.extensions.UNICODE)
psql.extensions.register_type(psql.extensions.UNICODEARRAY)
try:
	connection = psql.connect(user="postgres",
							password="2474",
							host="localhost",
							database = "project1")
	cursor = connection.cursor();
	print(connection.get_dsn_parameters(), "\n")

	cursor.execute("select version();")
	record = cursor.fetchone()
	print("Your are connected to - " , record, "\n")
   
except Exception as e:
	print("Error while connection to postgresSql", e)
# cursor = connection.cursor();
app = Flask (__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/adminlogin", methods=['GET', 'POST'])
def admin_login():
	stringvalue=['Not an Admin', 'Click Here', "Admin", "User Signin","login_user" ]
	form = LoginForm()
	username = form.name.data
	password = form.password.data
	if request.method=='POST':
		username=username.upper()
		adminloginquery = "select * from admindetails where username = '{}' and password = '{}';".format(username, password);
		cursor.execute(adminloginquery)
		usernametable = cursor.fetchall()
		if len(usernametable) != 0:
			return redirect(url_for('admin1', username=username))
		else:
			flash("user doesn't exist")
	return render_template('login.html', title='AdminLogin', form=form, stringvalue=stringvalue)

@app.route("/adminlogin/admin1", methods=['GET', 'POST'])
def admin1():
	username=request.args.get('username', None)
	print(username);
	stmt = "select * from admindetails where username = '{}';".format(username)
	cursor.execute(stmt)
	tables = cursor.fetchall()
	posts = tables[0]
	
	
	return render_template('admin1.html', posts=posts)


@app.route("/adminlogin/userhistory", methods=['GET', 'POST'])
def user_history():

	return render_template('userhistory.html')

@app.route("/adminlogin/returnbook", methods=['GET', 'POST'])
def book_return():
	return render_template('returnbook.html')

@app.route("/signup", methods=['GET', 'POST'])
def add_user():
    stringvalue=["Already Have an Account", "Sign in", "User", "Admin Singin", "admin_login",]
    form = UserRegistrationForm()
    if not form.validate_on_submit():
    	flash('please enter valid user details')
    else:
	    entrynumber = form.entryNumber.data
	    name = form.name.data
	    password = form.password.data
	    emailid = form.emailId.data
    if request.method == 'POST' and userNotAvailabe(entrynumber) and len(entrynumber)>4 and len(name) > 3 and len(password) > 7 and '@' in emailid and not pendingAvailable(entrynumber):
    	insertstmt = "insert into pending values ('{}', '{}', '{}', '{}',{},{},{});".format(entrynumber, name, password, emailid,0,0,0)
    	cursor.execute(insertstmt)
    	connection.commit()
    	flash("Please wait till confirmation")
    	return redirect(url_for('login_user'))
    elif request.method=='POST' and len(entrynumber) < 6:
    	flash('length of userid is too sort')
    elif request.method=='POST' and len(name) < 4:
    	flash('length of name is too sort')
    elif request.method=='POST' and len(password) < 8:
    	flash('Please enter at least 8 word password')
    elif request.method=='POST' and ('@' not in emailid):
    	flash('Please enter valid email id')
    elif request.method=='POST' and pendingAvailable(entrynumber):
    	flash("Already signup....Please wait till confirmation")
    elif request.method=='POST' and not userNotAvailabe(entrynumber):
    	flash("Userid Already taken please try different userid")

    return render_template('register.html',title='Register',form=form, stringvalue=stringvalue)

def userNotAvailabe(userid):
	userid = userid.upper()
	userAvailabe = "select id from userdetails where id='{}';".format(userid)
	cursor.execute(userAvailabe)
	tables = cursor.fetchall()
	if len(tables) == 0:
		return True
	elif len(userid) < 5:
		return True
	return False

def validateUser(userid, password):
	userid = userid.upper()
	checkUser = "select id from userdetails where password='{}' and id='{}';".format(password, userid)
	cursor.execute(checkUser)
	tables = cursor.fetchall()
	if len(tables) != 0:
		return True
	return False
def pendingAvailable(userid):
	userid=userid.upper()
	checkUser="select id from pending where id='{}';".format(userid)
	cursor.execute(checkUser)
	tables = cursor.fetchall()
	if len(tables) != 0:
		return True
	return False
@app.route('/login', methods=['POST','GET'])
def login_user():
    form = LoginForm()
    stringvalue=["New User", "Sign Up", "User", "Admin Sign in", "admin_login"]
    userid = form.name.data
    password = form.password.data
    if request.method=='POST' and (not userNotAvailabe(userid) and validateUser(userid, password)) and not pendingAvailable(userid):
    	return redirect(url_for('search_form'))
    elif request.method=='POST' and pendingAvailable(userid):
    	flash("User haven't confirmed yet Please wait")
    elif request.method=='POST' and userNotAvailabe(userid):
    	flash("Username not available please sign up")
    elif request.method=='POST' and not userNotAvailabe(userid):
    	flash("Password doesn't match")


    return render_template('login.html',title='Login',form=form, stringvalue=stringvalue)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login_user'))
    return wrap

@app.route('/bookissues/<book_name>')
def book_issues(book_name):
	form = BookIssuesForm()
	book_search = "select * from library_collection_inventory where isbn='{}';".format(book_name)
	print(book_name)
	cursor.execute(book_search)
	tables = cursor.fetchall()
	posts =[e for e in tables]
	userId = form.userId.data
	return render_template('bookIssues.html', posts=posts, form=form)

@app.route("/search", methods=['GET', 'POST'])
def search_form():
	initialtenvalue="""select * from library_collection_inventory limit 10;"""
	cursor.execute(initialtenvalue)
	posts1=[e for e in cursor.fetchall()]
	searchby = ""
	if request.method == 'POST':
		print(searchby)
		book_name = request.form.get('book_name')
		try:
			stmt = """select * from library_collection_inventory where {} like '%{}%' limit 20;""".format(searchby, book_name)
			print(stmt)
			cursor.execute(stmt)
			tables = cursor.fetchall()
			posts1=[e for e in tables]
			return render_template("searchpage.html", posts=posts1)
		except Exception as e:
			raise e
	return render_template("searchpage.html", posts=posts1)



#TODO make this as insert new book methods
@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name=request.form.get('name')
        author=request.form.get('author')
        published=request.form.get('published')
        try:
            return name
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")


def checkTableExists(tablename):
    dbcur = connection.cursor()
    stmt = "select * from '{}';".format(tablename)
    try:
    	dbcur.execute(stmt)
    	return True
    except Exception as e:
    	return False
    dbcur.close()
    return False

@app.route('/user/<username>')
# @login_required
def user(username):
	cursor.execute("select name from userdetails where name = '{}';".format(username))
	user = cursor.fetchall()
	# uu=user[0]
	cursor.execute("select * from checkin_data where userid = '{}';".format(user[0][0]))#assuming that checkouts_by_title_data_lens contains column of user name
	table_history = cursor.fetchall()
	cursor.execute("select * from checkouts_data where userid = '{}';".format(user[0][0]))#assuming that checkout_List is for present  contains column of user name
	table_current = cursor.fetchall()
	if len(user)!=0 :
		posts = [
		{'author': table_current, 'body': table_current},
		{'author': table_history, 'body': table_history}
		]
		return render_template('user.html', user=user, posts=posts)
   	else: 
   		return 'not found'
    
   




if __name__ == '__main__':
    app.run()
    cursor.close()
    connection.close()
    searchby=request.form['searchbyradio']