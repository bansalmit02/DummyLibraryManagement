# Dummy Library Mangement

## col362 project IIT DELHI

Using Flask Web Application Framework for backend and PSQL for database.

**psycopg2** for connecting backend to database. We had to do raw query that's why we are using thie package.




**Following things are required before running this library management.**
1. First activate python environment
```
   $cd/project1
   $source env/bin/activate
```
2. Then setup your database in app.py 
```python
connection = psql.connect(
    user="your_user_name",
    password="Password",
    host="localhost",
    port="5432",
    database = "database_name"
)
```
