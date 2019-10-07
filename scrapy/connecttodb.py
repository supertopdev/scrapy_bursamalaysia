#!/usr/bin/python

import MySQLdb

SQL_DB = 'fareasth_bursa'
SQL_HOST = 'localhost'
SQL_USER = 'fareasth_bursa'
SQL_PASSWD = '1410Qf-9Hv.SH(g'


# Open database connection
db = MySQLdb.connect(SQL_HOST, SQL_USER, SQL_PASSWD, SQL_DB)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

# disconnect from server
db.close()
