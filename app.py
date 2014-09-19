import os
import MySQLdb
import datetime

conf = {
	'db': os.environ.get('PYWALL_DB', 'pywall'),
	'dbhost': os.environ.get('PYWALL_DBHOST', 'localhost'),
	'dbuser': os.environ.get('PYWALL_DBUSER', 'pywall'),
	'dbpass': os.environ.get('PYWALL_DBPASS', 'pywall'),
}
 
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

def list_records(table, columns):
	"""
		Get all records (with list of columns) of a table.
	"""
	query = "select {} from {}".format(', '.join(columns), table)
	values = sql(query)
	return dict(zip(columns, values[0]))

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
	return list_records('wall', ['message', 'posted_by', 'posted_on'])
