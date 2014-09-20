
import os
conf = {
	'db': os.environ.get('PYWALL_DB', 'pywall'),
	'dbhost': os.environ.get('PYWALL_DBHOST', 'localhost'),
	'dbuser': os.environ.get('PYWALL_DBUSER', 'pywall'),
	'dbpass': os.environ.get('PYWALL_DBPASS', 'pywall'),
}

import MySQLdb
def sql(query):
	"""
	executes an sql query
	"""
	conn = MySQLdb.connect(conf['dbhost'], conf['dbuser'], 
			       conf['dbpass'])
	conn.select_db(conf['db'])
	conn.autocommit(True)
	cursor = conn.cursor()
	cursor.execute(query)
	ret = cursor.fetchall()
	conn.close()
	return ret

def insert_record(table, record):
	"""
	Insert a record(dict) in a table
	"""
	columns = record.keys()
	values = record.values()

	# ['col1', 'col2', 'col3' ] -> "col1,col2,col3"
	columns_fragment = ",".join(columns)

	# ['val1', 'val2', 'val3' ] to "'val1', 'val2', 'val3'"
	values_fragment = "'" + "', '".join(values) + "'"

	query = "insert into `{}` ({}) values({})".format(table, 
				columns_fragment, values_fragment)
	sql(query)

def list_records(table, columns, order_by=None):
	"""
	Get all records (with list of columns) of a table.
	"""
	ret = []
	order_by_fragment = "order by {}".format(order_by) if order_by else ""
	query = "select {} from {} {}".format(', '.join(columns), 
				table, order_by_fragment)
	rows = sql(query)
	for row in rows:
		ret.append(dict(zip(columns, row)))
	return ret

import datetime
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
	return list_records('wall', ['message', 'posted_by', 'posted_on'], 
			    order_by='-posted_on')

from flask import Flask, request, redirect, render_template
app = Flask(__name__)

@app.route('/')
def get_wall_view():
	return render_template('wall.html', messages=get_wall())

@app.route('/message/', methods=['POST'])
def add_to_wall_view():
	posted_by = request.form['posted_by']
	message = request.form['message']
	add_to_wall(message, posted_by)
	return redirect('/')

if __name__ == "__main__":
	app.run(debug=True)
