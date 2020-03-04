from flask import Flask, request, session, jsonify, render_template, url_for, flash, redirect
from wtforms import RadioField, Form
import psycopg2 as psql
import os
from forms import UserRegistrationForm, LoginForm, BookIssuesForm, BookReturnForm, UserHistory
from flask_login import login_required,login_manager
from functools import wraps
from flask_login import LoginManager, UserMixin


# login_manager = LoginManager()
# login_manager.init_app(app)


SECRET_KEY='development'
# 
# SocketServer.TCPServer.allow_reuse_address = True
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
psql.extensions.register_type(psql.extensions.UNICODE)
psql.extensions.register_type(psql.extensions.UNICODEARRAY)
try:
	connection = psql.connect(
							# user="postgres",
							# password="2474",
							# host="localhost",
							# # port="5432",
							# database = "project1"
							user="group_36",
							password="787-867-421",
							host="10.17.50.126",
							port="5432",
							database="group_36"

							)
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

class User(UserMixin):
	def __init__(self, id,password, b):
		self.id = id
		self.password=password
		self.bool=b
		self.admin=False
	def login(self):
		self.bool=True

	def logout(self):
		self.bool=False
	def admin_in(self):
		self.admin=True
		self.bool=True
	def admin_ou(self):
		self.admin=False
		self.bool=False
	def set_id(self,id):
		self.id=id
	def get_id(self):
		return self.id
	def is_admin(self):
		if(self.admin==True):
			return True
		else:
			return False
	def is_login(self):
		if(self.bool==True):
			return True
		else:
			False


obj=User('','',False)
@app.route("/")
def welcome():
    return render_template('welcome.html', title="Welcome Page")


@app.route("/adminlogin", methods=['GET', 'POST'])
def admin_login():
	stringvalue=['Not an Admin', 'Click Here', "Admin", "User Signin","login_user" ]
	form = LoginForm()
	username = form.name.data
	password = form.password.data
	if request.method=='POST':
		username=username.upper()
		# cursor.execute("drop index admindetails_username;")
		cursor.execute("create unique index admindetails_username on admindetails (username);")
		adminloginquery = "select * from admindetails where username = '{}' and password = '{}';".format(username, password);
		cursor.execute(adminloginquery)
		usernametable = cursor.fetchall()
		cursor.execute("drop index admindetails_username;")
		if len(usernametable) != 0:
			obj.admin_in()
			obj.set_id(username)
			# obj.set_pwd(password)
			return redirect(url_for('admin1', username=username))
		else:
			flash("user doesn't exist")
	return render_template('login.html', title='AdminLogin', form=form, stringvalue=stringvalue)

@app.route("/adminlogin/admin1", methods=['GET', 'POST'])
def admin1():
	username=request.args.get('username', None)

	# print(username);
	if (obj.is_admin() and obj.is_login()):
		username = obj.get_id()
		stmt = "select * from admindetails where username = '{}';".format(username.upper())
		cursor.execute(stmt)
		tables = cursor.fetchall()
		posts = tables[0]
		cursor.execute("select * from pending limit 20;")
		pendings=cursor.fetchall();
		cursor.execute("select * from checkouts_data where admin_issued='{}' order by issue_date desc limit 10;".format(username.upper()))
		chekouthistorys=cursor.fetchall()
		cursor.execute("select * from checkin_data where admin_issued='{}' order by return_date limit 10;".format(username.upper()))
		tables1 = cursor.fetchall()
		# for e in tables:
		# 	print(e)
		# 	chekouthistorys.append(e)
		return render_template('admin1.html', posts=posts, pendings=pendings, chekouthistorys=chekouthistorys, checkinhistorys=tables1)
	elif (obj.is_login()):
		flash("You are not Admin")
		return redirect(url_for('search_form'))
	else:
		flash("Sorry, You are not logged in as Admin")
		return redirect(url_for('admin_login'))

@app.route("/adminlogin/<userid>")
def acces_granted(userid):
	cursor.execute("select * from pending where id='{}';".format(userid))
	storevalue = cursor.fetchall()
	cursor.execute("insert into userdetails values('{}', '{}', '{}','{}','{}', {}, {})".format(storevalue[0][0], storevalue[0][1], storevalue[0][2], storevalue[0][3], 0, 0, 0))
	connection.commit()
	cursor.execute("delete from pending where id='{}'".format(userid))
	connection.commit()
	return redirect(url_for('admin1'))

@app.route("/adminlogin/userhistory", methods=['GET', 'POST'])
def user_history():
	form=UserHistory()
	userid=form.userId.data
	if (obj.is_admin() and obj.is_login()):
		if request.method=='POST':
			# stmt1="select * from checkouts_data where userid = '{}'".format(userid)
			# stmt2="select * from checkin_data where userid = '{}'".format(userid)
			# cursor.execute("create unique index userdetails_id on userdetails (id);")
			cursor.execute("select * from userdetails where id = '{}';".format(userid.upper()))
			user = cursor.fetchall()
			# cursor.execute("drop index userdetails_id;")
			# uu=user[0]

			# print (user)
			# print(obj.get_id())
			cursor.execute("create view userchekin as (select * from library_collection as b join checkin_data as a on a.bookid=b.id);")
			cursor.execute("select id,title,issue_date,due_date,return_date from userchekin as k where k.userid= '{}';".format(user[0][0].upper()))
			table_history = cursor.fetchall()
			posts1=[e for e in table_history]
			cursor.execute("drop view userchekin;")
			cursor.execute("create view usercheckouts as (select * from library_collection as b join checkouts_data as a on a.bookid=b.id);")
			cursor.execute("select id,title,issue_date,due_date from usercheckouts as k where k.userid= '{}';".format(user[0][0].upper()))

			
			table_current = cursor.fetchall()
			posts2=[e for e in table_current]
			cursor.execute("drop view usercheckouts;")
			if len(user)!=0 :
				# posts1= table_history
				posts = [
				{'author': table_current, 'body': posts1},
				{'author': table_history, 'body': posts2}
				]
				return render_template('userhistory.html',form=form, user=user, post1=posts2, post2=posts1)

		return render_template('userhistory.html', form=form)
	elif(obj.is_login):
		flash("You are not Admin")
		return redirect(url_for('search_form'))
	else:
		flash("Sorry, You are not logged in as Admin")
		return redirect(url_for('add_user'))

@app.route("/adminlogin/returnbook", methods=['GET', 'POST'])
def book_return():
	form=BookReturnForm()
	if (obj.is_admin() and obj.is_login()):
		userid=form.userId.data
		storevalue=[]
		if request.method=='POST':
			userid=userid.upper()
			stmt = "select * from checkouts_data where userid='{}';".format(userid)
			cursor.execute(stmt)
			posts = cursor.fetchall()
			if len(posts) == 0:
				flash("No book issued for that user")
				return redirect(url_for('book_return'))
			cursor.execute("select date(current_timestamp);")
			todaydate = cursor.fetchall()[0][0]
			# cursor.execute("select acc_type from userdetails where id ='{}';").format(userid)
			# accType = cursor.fetchall()[0][0]
			fines=[]
			i=0
			newposts=[]
			for post in posts:
				duedate=post[4]
				cursor.execute("select {} < {};".format(duedate, todaydate))
				istrue = cursor.fetchall()
				#TODO add fine according to the booking limit table
				if (istrue[0][0] == 't'):
					stmt="SELECT DATE_PART('day', '{} 00:00:00'::timestamp - '{} 00:00:00'::timestamp);".format(todaydate-duedate)
					cursor.execute(stmt)
					fine = cursor.fetchall()[0][0]*5
					post=list(post)
					post.append(fine)
					newposts.append(post)
					i+=1
				else:
					post=list(post)
					post.append(0)
					newposts.append(post)
					i += 1
			return render_template('returnbook.html', form=form, posts=newposts, userid=userid)

		return render_template('returnbook.html', form=form)
	elif(obj.is_login()):
		flash("You are not Admin")
		return redirect(url_for('search_form'))
	else:
		flash("Sorry, You are not logged in as Admin")
		return redirect(url_for('login_user'))

@app.route("/adminlogin/returnbook/<userid>/<bookid>/<fine>", methods=['GET', 'POST'])
def book_return_by_user(userid, bookid, fine):
	stmt="select * from checkouts_data where userid='{}' and bookid='{}';".format(userid, bookid)
	cursor.execute(stmt)
	tables = cursor.fetchall()[0]
	cursor.execute("select date(current_timestamp);")
	date = cursor.fetchall()[0][0]
	userid=userid.upper()
	stmt="insert into checkin_data values('{}',{},'{}'::date,'{}', '{}'::date, '{}'::date,'{}');".format(userid, bookid,tables[2], tables[3], tables[4],date,obj.get_id())
	cursor.execute(stmt)
	connection.commit()
	stmt="delete from checkouts_data where userid='{}' and bookid='{}'".format(userid, bookid)
	cursor.execute(stmt)
	connection.commit()
	userupdate="update userdetails set books_issued = books_issued - 1, fine =fine + {} where id ='{}'".format(fine, userid)
	cursor.execute(userupdate)
	connection.commit()
	bookupdate="update library_collection set itemcount = itemcount + 1 where id='{}';".format(bookid)
	cursor.execute(bookupdate)
	connection.commit()
	flash("Sucessfully return")
	return redirect(url_for('book_return'))

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
    	flash('length of userid is too sort at least 7 char')
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
	cursor.execute("create unique index userAvailablityCheck on userdetails (id);")
	userAvailabe = "select id from userdetails where id='{}';".format(userid)
	cursor.execute(userAvailabe)
	tables = cursor.fetchall()
	cursor.execute("drop index userAvailablityCheck;")
	if len(tables) == 0:
		return True
	elif len(userid) < 5:
		return True
	return False

def validateUser(userid, password):
	userid = userid.upper()
	cursor.execute("create unique index userAvailablityCheck on userdetails (id);")
	checkUser = "select id from userdetails where password='{}' and id='{}';".format(password, userid)
	cursor.execute(checkUser)
	tables = cursor.fetchall()
	cursor.execute("drop index userAvailablityCheck;")
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
    	obj.login()
    	obj.set_id(userid)
    	return redirect(url_for('search_form'))
    elif request.method=='POST' and pendingAvailable(userid):
    	flash("User haven't confirmed yet Please wait")
    elif request.method=='POST' and userNotAvailabe(userid):
    	flash("Username not available please sign up")
    elif request.method=='POST' and not userNotAvailabe(userid):
    	flash("Password doesn't match")


    return render_template('login.html',title='Login',form=form, stringvalue=stringvalue)

@app.route('/logout')
def logout():
	if (obj.is_login()):
		obj.admin_ou()
		flash("Sucessfully, Loged Out")
		# connection.close()
		return redirect(url_for('login_user'))
	else:
		flash("You are not Logged in, login first")
		return redirect(url_for('login_user'))

@app.route('/bookissues/<book_id>', methods=['POST', 'GET'])
def book_issues(book_id):
	if (obj.is_admin() and obj.is_login()):
		form = BookIssuesForm()
		# userid = form.userId.data
		cursor.execute("create unique index BookSearch on library_collection (id);")
		book_search = "select * from library_collection where id={};".format(book_id)
		# print(book_name)
		cursor.execute(book_search)
		tables = cursor.fetchall()
		cursor.execute("drop index BookSearch;")
		posts =[e for e in tables]
		userid = form.userId.data
		adminid = obj.get_id()
		itemcount=tables[0][13]
		if request.method=='POST':
			stmt="select books_issued, fine from userdetails where id='{}'".format(userid)
			cursor.execute(stmt)
			(book_issued, fine) = cursor.fetchall()[0]
			userid.upper() 
			#TODO insert here booklimit fine all the things
			cursor.execute("select acc_type from userdetails where id='{}';".format(userid))
			accType=cursor.fetchall()[0][0]
			cursor.execute("select * from booklimit where type={};".format(accType))
			print(accType)
			# print(cursor.fetchall())
			tab = cursor.fetchall()
			maxfine=tab[0][2]
			maxbookissued=tab[0][1]
			maxdays=tab[0][3]
			if(itemcount > 0 and not userNotAvailabe(userid)) and book_issued < maxbookissued and fine < maxfine:
				stmt="insert into checkouts_data values ('{}','{}',date(current_timestamp),'{}',date(current_timestamp + interval '{} days'));".format(userid, book_id, adminid, maxdays)
				stmtupdate="update library_collection set itemcount = itemcount-1 where id ='{}'".format(book_id)
				userupdate="update userdetails set books_issued = books_issued + 1 where id ='{}'".format(userid)
				cursor.execute(stmt)
				connection.commit()
				cursor.execute(stmtupdate)
				connection.commit()
				cursor.execute(userupdate)
				connection.commit()
				flash('book issued')
				return render_template('bookIssues.html', posts=posts, form=form)
			elif userNotAvailabe(userid):
				flash("User not available")
			elif fine >= maxfine:
				flash("Please Pay fine first")
			elif book_issued >= maxbookissued:
				flash("You already have more Five books issued")
			else:
				flash("Book not available")

		return render_template('bookIssues.html', posts=posts, form=form)
	else:
		flash("You can't issue book, either you are not Admin or Not loggedin as Admin")
		return redirect(url_for('search_form'))


@app.route("/search", methods=['GET', 'POST'])
def search_form():
	if (obj.is_login()):
		initialtenvalue="""select * from library_collection limit 10;"""
		cursor.execute(initialtenvalue)
		posts1=[e for e in cursor.fetchall()]
		searchby = ""
		if request.method == 'POST':
			# print(searchby)
			searchby=request.form['searchbyradio']
			book_name = request.form.get('book_name')
			try:
				stmt = """select * from library_collection where {} like '%{}%' limit 20;""".format(searchby, book_name)
				print(stmt)
				cursor.execute(stmt)
				tables = cursor.fetchall()
				return render_template("searchpage.html", posts=tables)
			except Exception as e:
				raise e
		return render_template("searchpage.html", posts=posts1)
	else:
		flash("Login first")
		return redirect(url_for('login_user'))

@app.route("/bookdetails/<bookid>", methods=['GET', 'POST'])
def book_details(bookid):
	stmt="select * from library_collection where id={}".format(bookid)
	cursor.execute(stmt)
	posts=cursor.fetchall()[0]
	return render_template('BookDetails.html', posts=posts)


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

@app.route('/user')
def user():
	if obj.is_login() and obj.is_admin():
		return redirect(url_for('admin1'))
	elif(obj.is_login()):
		cursor.execute("create unique index userAvailablityCheck on userdetails (id);")
		cursor.execute("select * from userdetails where id = '{}';".format(obj.get_id().upper()))
		user = cursor.fetchall()
		cursor.execute("drop index userAvailablityCheck;")
		cursor.execute("create view userchekin as (select * from library_collection as b join checkin_data as a on a.bookid=b.id);")
		cursor.execute("select id,title,issue_date,due_date,return_date from userchekin as k where k.userid= '{}';".format(user[0][0]))
		table_history = cursor.fetchall()
		posts1=[e for e in table_history]
		cursor.execute("drop view userchekin;")
		cursor.execute("create view usercheckouts as (select * from library_collection as b join checkouts_data as a on a.bookid=b.id);")
		cursor.execute("select id,title,issue_date,due_date from usercheckouts as k where k.userid= '{}';".format(user[0][0]))
		table_current = cursor.fetchall()
		posts2=[e for e in table_current]
		cursor.execute("drop view usercheckouts;")
		if len(user)!=0 :
			# posts1= table_history
			posts = [
			{'author': table_current, 'body': posts1},
			{'author': table_history, 'body': posts2}
			]
			return render_template('user.html', user=user, post1=posts2, post2=posts1)
	   	else: 
	   		return 'not found'
	else:
		flash("you are not logged in, login first")
		return redirect(url_for('login_user'))
    
   




if __name__ == '__main__':
    app.run()
    cursor.close()
    connection.close()
    searchby=request.form['searchbyradio']