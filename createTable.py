from flask import Flask, render_template, url_for, request, redirect
import psycopg2
import config

# PostgreSQL and psycopg2 server
con = psycopg2.connect(dbname='cntUserForm',
                       user='postgres',
                       host='localhost',
                       port='5432',
                       password=config.Config.SERVER_PASSWORD)

# Cursor object to execute SQL statements
cur = con.cursor()

create_table_query = "CREATE TABLE userTable (email TEXT PRIMARY KEY, firstName TEXT NOT NULL, lastName TEXT NOT NULL, age INTEGER NOT NULL) ;"
try:
    cur.execute(create_table_query)  # Execute the query to create table in database
    con.commit()  # commit changes
except:
    print('there was an error creating the table.')
