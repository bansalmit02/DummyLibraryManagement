from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
import psycopg2 as psql
import os
import models
try:
	conncetion = psql.connect(user="postgres",
							password="2474",
							host="localhost",
							database = "project1")
	cursor = conncetion.cursor();
	print(conncetion.get_dsn_parameters(), "\n")

	cursor.execute("select version();")
	record = cursor.fetchone()
	print("Your are connected to - " , record, "\n")
	# cursor.close()
   
except Exception as e:
	print("Error while connection to postgresSql", e)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)



@app.route("/")
def hello():
    return "Hello World! This is Asif Anwar"

@app.route("/add")
def add_book():
	name=request.args.get('name')
	author=request.args.get('author')
	published=request.args.get('published')
	try:
		book=models.Book(
			name=name,
			author=author,
			published=published
			)
		db.session.add(book)
		db.session.commit()
		return "Book added. book id={}".format(book.id)
	except Exception as e:
		return(str(e))

@app.route("/getall")
def get_all():
	try:
		books = models.Book.query.all()
		return jsonify([e.serialize() for e in books])
	except Exception as e:
		return(str(e))
@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=models.Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
	    return(str(e))
@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name=request.form.get('name')
        author=request.form.get('author')
        published=request.form.get('published')
        try:
            book=models.Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            # return 
            return get_name1()
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_book_details():
    author=request.args.get('author')
    published=request.args.get('published')
    return "Author : {}, Published: {}".format(author,published)
@app.route("/name/na", methods=['GET', 'POST', 'PUT'])
def get_name():
	if request.method == 'POST':
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		try:
			# cursor = conncetion.cursor();
			# if not checkTableExists("Asif"):
				# print("Table Dont exist")

			cursor.execute("insert into user1 values ('{}', '{}');".format(fname, lname))
			conncetion.commit()
			# cursor.close()
			# return "Name Added = {}".format(fname + " " + lname);
			return get_name1()
		except Exception as e:
			# cursor = conncetion.cursor();
			# cursor.execute("create table user1(fname VARCHAR(10), lname VARCHAR(40));")
			# conncetion.commit()
			# cursor.execute("insert into user1 values ({}, {});".format(fname, lname))
			# cursor.close()
			# return "Name Added = {}".format(fname + " " + lname);
			raise e
	return render_template('name.html')
def checkTableExists(tablename):
    dbcur = conncetion.cursor()
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


    # result = dbcur.fetchone()
    # if dbcur.fetchone()[0] == 1:
    #     dbcur.close()
    #     return True
    # if result:
    # 	dbcur.close()
    # 	return True

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
	return jsonify([asif(e[0], e[1]) for e in tables])

@app.route("/author/<bibnum1>")
def get_author(bibnum1):
	cursor.execute("select author from library_collection_inventory where bibnum = {}".format(bibnum1))
	author = cursor.fetchall()
	return jsonify([e for e in author])

if __name__ == '__main__':
    app.run()
    cursor.close()
    conncetion.close()