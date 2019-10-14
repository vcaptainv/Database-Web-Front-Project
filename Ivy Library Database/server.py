#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://yh3097:5468@34.73.21.127/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

columnnamedict ={'librarian': ['libraryname', 'name', 'age', 'ssn', 'email'],
'school':['schoolname'],
'students': ['sid', 'name', 'schoolname', 'age', 'schoolyear',],
'book': ['libraryname', 'bookname', 'publishdate', 'author', 'publisher', 'isbn'],
'journal': ['tittle', 'libraryname', 'publishdate', 'author', 'website'],
'dvd' : ['dvdname', 'libraryname', 'id', 'publisher'],
'library': ['schoolname', 'libraryname', 'adress'],
}

studenttable = ['book', 'journal', 'dvd']
librariantable = ['students', 'book', 'journal', 'dvd', 'library', 'librarian', 'school']

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/table_search')
def table_search():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  tablename = 'book'
  if not tablename:
  	tablename = 'book'
  #tablename = request.form('dropdown1')
  cursor = g.conn.execute("SELECT * FROM {}".format(tablename))
  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)
  


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("table_search.html", data = names , columnname = columnnamedict[tablename], studenttable = studenttable, librariantable = librariantable)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#



@app.route('/location_search')
def another():
  return render_template("location_search.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')

	
@app.route("/table_search" , methods=['POST'])
def table():
	tablename = request.form.get('dropdown1')
	cursor = g.conn.execute("SELECT * FROM {}".format(tablename))
	names = []
	for result in cursor:
		names.append(result)  # can also be accessed using result[0]
	cursor.close()
	return render_template("table_search.html", tablename=tablename, data = names , columnname = columnnamedict[tablename], studenttable = studenttable, librariantable = librariantable)

@app.route('/location_search', methods = ['POST'])
def location():
	entity = request.form.get('entityname')
	name = request.form.get('bookname')
	#print(name)
	locations = []	
	cursor = g.conn.execute("SELECT b.{}name, l.libraryname, l.address FROM {} b, library l WHERE b.libraryname = l.libraryname AND lower(b.{}name) like '%%{}%%' GROUP BY b.{}name, l.libraryname, l.address".format(str(entity), str(entity), str(entity), str(name), str(entity)))
	for result in cursor:
		locations.append(result)		
	cursor.close()
		
	if not locations:
		locations = [['Your Current Search result is Empty']]
	
	return render_template('location_search.html', entity = entity, locations = locations, name = name)
	
@app.route('/university_search', methods = ['GET', 'POST'])
def university():
	
	schoolnames = str(request.form.get('schoolname')).replace(" ", '')
	print( schoolnames + 'is here')
	cursor4 = g.conn.execute("SELECT * FROM BOOK B WHERE B.libraryname IN( SELECT L.libraryname FROM library L INNER JOIN school S ON L.schoolname = S.schoolname WHERE LOWER(L.schoolname) LIKE LOWER('%%{}%%'))".format(str(schoolnames)))
	schoolbooks = []
	for wtf in cursor4:
		schoolbooks.append(wtf)
	cursor4.close()
	print(schoolbooks)
	if not schoolbooks:
		schoolbooks = [['Your Current Search Result is Empty']]
	print(schoolbooks)
	
	
	university = []
	print('before cursor3 is runned')
	cursor3 = g.conn.execute("SELECT * FROM school")
	for result in cursor3:
		university.append(str(result[0]))
	cursor3.close()
	return render_template('university_search.html', schoolnames = schoolnames, schoolbooks = schoolbooks, university = university, bookcolumns = columnnamedict['book'])

@app.route('/checkedBooks', methods = ['GET','POST'])
def checkBooks():
	name = request.form.get('name')
	print name
	cursor = g.conn.execute("SELECT * FROM book R WHERE R.isbn IN(SELECT B.isbn FROM librarian L INNER JOIN checkout_book B ON L.ssn = B.ssn WHERE lower(L.name) like lower('{}'))".format(str(name)))
	books = []
	for result in cursor:
		books.append(result)
	print books
	cursor.close()
	return render_template('checkedBooks.html', books = books, name = name, columnname = columnnamedict['book'])
	
	

@app.route('/login', methods = ['GET', 'POST'])
def login():
	username = request.form.get('username')
	passcode = request.form.get('passcode')
	person = request.form.get('person')
	if not person: 
		person = 'student'
	print(username)
	print(passcode)
	print(person)
	if person == 'student':
		cursor =  g.conn.execute("SELECT * FROM students s where lower(s.name) = lower('{}') and lower(s.sid) = lower('{}')".format(str(username), str(passcode)))
	elif person == 'librarian':
		cursor =  g.conn.execute("SELECT * FROM librarian l where lower(l.name) = lower('{}') and l.ssn = '{}'".format(str(username), str(passcode)))
	

	success = []
	for result in cursor:
		success.append(result)
	print(success)
	output = 'Login Success. Welcome {} {}'.format(str(person), str(username))
	print('before if not success')
	if not success: 
		output = 'Log In failed. Please Renter Check Your ID Number'
		print('not success')
	print('before close cursor')
	cursor.close()
	print('we are about to return the function')
	return render_template('login.html', username = username, person = person, passcode = passcode, output = output, success = success)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
