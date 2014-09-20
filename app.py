import os
import MySQLdb
import datetime

from flask import Flask, request, redirect, render_template

from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

conf = {
	'db': os.environ.get('PYWALL_DB', 'pywall'),
	'dbhost': os.environ.get('PYWALL_DBHOST', 'localhost'),
	'dbuser': os.environ.get('PYWALL_DBUSER', 'pywall'),
	'dbpass': os.environ.get('PYWALL_DBPASS', 'pywall'),
}

# ORM
 
def sql(query):
	"""
		executes an sql query
	"""
	conn = MySQLdb.connect(conf['dbhost'], conf['dbuser'], conf['dbpass'])
	conn.select_db(conf['db'])
	cursor = conn.cursor()
	cursor.execute('begin')
	cursor.execute(query)
	ret = cursor.fetchall()
	cursor.execute('commit')
	conn.close()
	return ret

def insert_record(table, record):
	"""
		Insert a record(dict) in a table
	"""
	columns = ",".join(record.keys())
	values = "'" + "', '".join(record.values()) + "'"
	query = "insert into `{}` ({}) values({})".format(table, columns, values)
	sql(query)

def list_records(table, columns, order_by=None):
	"""
		Get all records (with list of columns) of a table.
	"""
	order_by = "order by {}".format(order_by)
	query = "select {} from {} {}".format(', '.join(columns), table, order_by)
	values = sql(query)
	return [dict(zip(columns, value)) for value in values]

# Wall methods

def add_to_wall(message, posted_by):
	"""
		Add a message to the wall
	"""
	insert_record('wall', {
		'message': message,
		'posted_by': posted_by,
		'posted_on': str(datetime.datetime.now())
	})

def get_wall():
	"""
		Get all messages on wall
	"""
	return list_records('wall', ['message', 'posted_by', 'posted_on'], order_by='-posted_on')

# Web views

@app.route('/')
def get_wall_view():
	return render_template('wall.html', messages=get_wall())

@app.route('/message/', methods=['POST'])
def add_to_wall_view():
	posted_by = request.form['posted_by']
	message = request.form['message']
	add_to_wall(message, posted_by)
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)
