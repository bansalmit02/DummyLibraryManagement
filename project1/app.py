from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
# from flask.ext.wtf import Form
from wtforms import RadioField, Form
import psycopg2 as psql
import os
from forms import UserRegistrationForm, LoginForm

SECRET_KEY='development'
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

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

class SimpleForm(object):
	"""docstring for SimpleForm"""
	example=RadioField("label", choices=[('value', 'description'), ('value_two', 'dsfafd')])
	
@app.route('/hello',methods=['post','get'])
def hello_world():
    form = SimpleForm()
    if form.validate_on_submit():
        print form.example.data
    else:
        print form.errors
    return render_template('example.html',form=form)

@app.route("/")
def hello():
    return "Hello World! This is Asif Anwar"


@app.route("/adduser", methods=['GET', 'POST'])
def add_user():
    form = UserRegistrationForm()
    if not form.validate_on_submit():
    	flash('please enter valid user details')
    else:
	    entrynumber = form.entryNumber.data
	    name = form.name.data
	    password = form.password.data
	    emailid = form.emailId.data
    if request.method == 'POST' and validateForm(entrynumber):
    	insertstmt = "insert into userDetails values ('{}', '{}', '{}', '{}',{},{},{});".format(entrynumber, name, password, emailid,0,0,0)
    	cursor.execute(insertstmt)
    	connection.commit()
    	return redirect(url_for('search_form'))
    else:
    	flash('user already exist')
    	


    return render_template('register.html',title='Register',form=form)

def validateForm(userId):
    userAvailabe = "select id from userDetails where id='{}';".format(userId)
    cursor.execute(userAvailabe)
    tables = cursor.fetchall()
    if len(tables) == 0:
    	return True
    return False
def validateUser(name, password):
	checkUser = "select id from userDetails where password='{}';".format(password)
	cursor.execute(checkUser)
	tables = cursor.fetchall()
	if len(tables) != 0:
		return True
	return False
@app.route('/login', methods=['post','get'])
def login_user():
    form = LoginForm()
    name = form.name.data
    password = form.password.data
    if request.method=='POST' and (not validateForm(name) and validateUser(name, password)):
    	return redirect(url_for('search_form'))
    else:
    	flash("user doesn't exitst please sign in")


    return render_template('login.html',title='Login',form=form)

# @app.route("/add")
# def add_book():
# 	name=request.args.get('name')
# 	author=request.args.get('author')
# 	published=request.args.get('published')
# 	try:
# 		book=models.Book(
# 			name=name,
# 			author=author,
# 			published=published
# 			)
# 		db.session.add(book)
# 		db.session.commit()
# 		return "Book added. book id={}".format(book.id)
# 	except Exception as e:
# 		return(str(e))

# @app.route("/getall")
# def get_all():
# 	try:
# 		books = models.Book.query.all()
# 		return jsonify([e.serialize() for e in books])
# 	except Exception as e:
# 		return(str(e))
# @app.route("/get/<id_>")
# def get_by_id(id_):
#     try:
#         book=models.Book.query.filter_by(id=id_).first()
#         return jsonify(book.serialize())
#     except Exception as e:
# 	    return(str(e))
@app.route("/search", methods=['GET', 'POST'])
def search_form():
	print('-------------')
	print(request.form.get('radio'))
	print('-------------')
	if request.method == 'POST':
		
		if (request.form.get('radio')=='title'):
			print("hello world")
		book_name = request.form.get('book_name')
		try:
			stmt = """select * from library_collection_inventory where title like '%{}%';""".format(book_name)
			print(stmt)
			cursor.execute(stmt)
			tables = cursor.fetchall()
			return jsonify([e for e in tables])
		except Exception as e:
			raise e
	return render_template("searchpage.html")

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

@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

# @app.route("/details")
# def get_book_details():
#     author=request.args.get('author')
#     published=request.args.get('published')
#     return "Author : {}, Published: {}".format(author,published)
@app.route("/name/na", methods=['GET', 'POST', 'PUT'])
def get_name():
	if request.method == 'POST':
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		try:
			# cursor = connection.cursor();
			# if not checkTableExists("Asif"):
				# print("Table Dont exist")

			cursor.execute("insert into user1 values ('{}', '{}');".format(fname, lname))
			connection.commit()
			# cursor.close()
			# return "Name Added = {}".format(fname + " " + lname);
			return get_name1()
		except Exception as e:
			# cursor = connection.cursor();
			# cursor.execute("create table user1(fname VARCHAR(10), lname VARCHAR(40));")
			# connection.commit()
			# cursor.execute("insert into user1 values ({}, {});".format(fname, lname))
			# cursor.close()
			# return "Name Added = {}".format(fname + " " + lname);
			raise e
	return render_template('name.html')
def checkTableExists(tablename):
    dbcur = connection.cursor()
    stmt = "select * from '{}';".format(tablename)
    # dbcur.execute("""
    #     SELECT COUNT(*)
    #     FROM information_schema.tables
    #     WHERE table_name = '{0}'
    #     """.format(tablename.replace('\'', '\'\'')))
    try:
    	dbcur.execute(stmt)
    	return True
    except Exception as e:
    	return False
    dbcur.close()
    return False
def asif(f,l):
	return{
		'fname': f,
		'lname': l
	}
@app.route("/name/na/getall")
def get_name1():
	cursor.execute("select * from library_collection_inventory limit 100;")
	tables=cursor.fetchall()
	# print("-----------------")
	# for table in tables:
	# 	print(table)
	# 	print("-----------------")
	return jsonify([e for e in tables])

@app.route("/author/<bibnum1>")
def get_author(bibnum1):
	cursor.execute("select author from library_collection_inventory where bibnum = {}".format(bibnum1))
	author = cursor.fetchall()
	return jsonify([e for e in author])

if __name__ == '__main__':
    app.run()
    cursor.close()
    connection.close()