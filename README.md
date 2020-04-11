# Dummy Library Mangement

## col362 project IIT DELHI

Using Flask Web Application Framework for backend and PSQL for database.

**psycopg2** for connecting backend to database. We had to do raw query that's why we are using this package.

**First create database and then run 
```\i createtable```
file for creating all the table or schema in your psql database**

**Following things are required before running this library management.**
1. First create python3 virtual environment and activatae
2. then run requirements.txt
```
   $pip install -r requiremnts.txt
   
```
3. Then setup your database in app.py 
```python
connection = psql.connect(
    user="your_user_name",
    password="Password",
    host="localhost",
    port="5432",
    database = "database_name"
)
```
3. After creating database and setting step2 run app.py
```python app.py```

**Environment is created using python3**

[LICENSE](https://github.com/asifanwar007/DummyLibraryManagement/blob/master/LICENSE.md "MIT License")

