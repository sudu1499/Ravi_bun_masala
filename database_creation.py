import sqlite3
def login():
    conn=sqlite3.connect('login.db')
    c=conn.cursor()
    c.execute('create table login (name text,email text primary key ,password text)')
    conn.commit()
    conn.close()

def order():
    conn=sqlite3.connect('order.db')
    c=conn.cursor()
    c.execute('create table order_table (name text,email text ,dish text,count number,time number)')
    conn.commit()
    conn.close()

def status():
    conn=sqlite3.connect('status.db')
    c=conn.cursor()
    c.execute('create table status (name text,email text,dish text,status text)')
    conn.commit()
    conn.close()

def paid():
    conn=sqlite3.connect('paid.db')
    c=conn.cursor()
    c.execute('create table paid (name text ,email text ,dish text ,count number ,time number)')
    conn.commit()
    conn.close()
login()
order()
status()

paid()
