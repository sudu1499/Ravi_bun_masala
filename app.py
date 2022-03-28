import hashlib
import hmac
import sqlite3
from flask import Flask, redirect,request,render_template,session, url_for
import time
import razorpay

sec_key='78zEiPdCi0MPegpw7wKCsH8H'
clnt=razorpay.Client(auth=('rzp_test_aynu7XqQ7ECJHs',sec_key))

app=Flask(__name__)
app.secret_key='lowday idanna crack madbeda'
d_c={'bun masala':30,'nippattu masala':20,'kalu masala':35,'shev masala':40,'soda masala':25 }
dish_orders=[]

@app.route('/',methods=['POST','GET'])
def defaulr_home():
    conn=sqlite3.connect('status.db')
    c=conn.cursor()

    c.execute('delete from status')

    conn.commit()
    conn.close()
    conn=sqlite3.connect('order.db')
    c=conn.cursor()

    c.execute('delete from order_table')

    conn.commit()
    conn.close()
    session.clear()
    return render_template('home.html')

@app.route('/home',methods=['POST','GET'])
def home():
    # if request.method=='POST':
    #     d=request.form.get('dish')
    #     session[d]=1
    return render_template('home.html')
@app.route("/addto",methods=['POST'])
def addto():
    if request.method=='POST':
        print('hay')
        d=request.form.get('item')
        print("@@@@@@@@@@@@@@@@@@@@@",d)
        session[d]=1
        return('',204)
@app.route('/login' ,methods=['POST','GET'])
def login():
    
    if request.method=='POST':
        conn=sqlite3.connect('login.db')
        c=conn.cursor()
        name=request.form.get('c_name')
        email=request.form.get('eid')
        password=request.form.get('pswd')
        q='select count(*) from login where email="{}"'.format(email)
        if c.execute(q).fetchall()[0][0]==1:
            return render_template('signup.html',result='already email id is registered')
        q="insert into login values('{}','{}','{}')".format(name,email,password)
        print(q)
        c.execute(q)
        conn.commit()
        conn.close()
    return render_template('login.html')
@app.route('/validate',methods=['POST','GET'] )
def validate():
    if request.method=='POST':
        email=request.form.get('eid')
        password=request.form.get('pswd')
        conn=sqlite3.connect('login.db')
        c=conn.cursor()
        q='select count(*) from login where email="{}"'.format(email)
        if c.execute(q).fetchall()[0][0]==0:
            return render_template('login.html',result1='invalid user name')
        q="select password from login where email='{}'".format(email)
        c.execute(q)
        print(q)
        given=c.fetchall()
        if password==given[0][0].strip():
            session['email']=email
            session['total']=0
            session['cost']=d_c
            session['done']=0

            return render_template('cart.html')
        else:
            return render_template('login.html',result2='invalid user name or password')
@app.route('/signup',methods=['POST','GET'])
def signup():
    return render_template('signup.html')
@app.route('/cart')
def cart():
    if 'email' not in session:
        return render_template('login.html')
    else:
        return render_template('cart.html')
@app.route('/logout')
def logout():
    session.clear()
    conn=sqlite3.connect('order.db')
    c=conn.cursor()
    c.execute('delete from order_table')
    conn.commit()
    conn.close()
    return render_template('home.html')
@app.route('/queue')
def queue():
    conn=sqlite3.connect('paid.db')
    c=conn.cursor()
    c.execute('select * from paid')
    r=c.fetchall()

    conn=sqlite3.connect('status.db')
    c=conn.cursor()
    c.execute('select * from status')
    s=c.fetchall()
    
    return render_template('queue.html',r=r,s=s)
@app.route('/locate')
def locate():
    return render_template('location.html')

@app.route('/ravi')
def ravi():
    conn=sqlite3.connect('paid.db')
    c=conn.cursor()
    c.execute('select * from paid')
    r=c.fetchall()
    return render_template('ravi.html',r=r)
@app.route('/done',methods=['POST','GET'])
def done():
    if request.method=='POST':
        print(request.form.get('dish').split(','))
        name,email,d,count,t=request.form.get('dish').split(',')
        
        conn=sqlite3.connect('paid.db')
        c=conn.cursor()
        c.execute(f'delete from paid where email="{email}" and dish="{d}" and count="{count}" and time="{t}"')
        print(f'delete from paid where email="{email}" and dish="{d} and count="{count}" ')
        conn.commit()
        conn.close()

        conn=sqlite3.connect('status.db')
        c=conn.cursor()
        print(f'insert into status values("{name}","{email}","{d}","DONE")')
        c.execute(f'insert into status values("{name}","{email}","{d}","DONE")')

        conn.commit()
        conn.close()
        return redirect(url_for('ravi'))

@app.route('/checkout',methods=['POST','GET'])
def checkout():
    global d_c,dish_orders
    if request.method=='POST':
        ################################################################################## for name
        conn=sqlite3.connect('login.db')
        c=conn.cursor()
        c.execute(f'select name from login where email=\'{session["email"]}\'')
        name=c.fetchall()[0][0]
        conn.close()
        ###################################################################################
        email=session['email']
        t=request.form.getlist('qt')
        d=[]
        count=[]
        d.append(t[0])
        for i in range(1,len(t)):
            if i%2==1:
                count.append(t[i])
            else:
                d.append(t[i])
        dish_orders=d
        conn=sqlite3.connect('order.db')
        c=conn.cursor()
        print("############################################",d,count)
        if session['done']==0:
            for i,j in zip(d,count):
                c.execute(f'insert into order_table values("{name}","{email}","{i}","{j}","{time.time()}")')
                # session.pop(i,None)
            conn.commit()
            session['done']=1
        else:
            c.execute(f'delete from order_table where email="{email}"')
            for i,j in zip(d,count):
                c.execute(f'insert into order_table values("{name}","{email}","{i}","{j}","{time.time()}")')
            conn.commit()
        sum=0
        for i in c.execute(f'select * from order_table where email="{email}" ').fetchall():
            sum+=int(d_c[i[2]])*int(i[3])
        session['total']=sum
        
        f=c.execute(f'select * from order_table where email="{email}"').fetchall()
        data = { "amount": session['total']*100, "currency": "INR", "receipt": "order_rcptid_11" }
        p = clnt.order.create(data=data)
        return render_template('pay.html',p=p,f=f)
@app.route('/pay_done',methods=['POST','GET'])
def pay_done():
    if request.method=='POST':
        
        conn1=sqlite3.connect('order.db')
        conn2=sqlite3.connect('paid.db')
        c1=conn1.cursor()
        c2=conn2.cursor()
        for i in c1.execute('select * from order_table').fetchall():
            c2.execute(f'insert into paid values("{i[0]}","{i[1]}","{i[2]}","{i[3]}","{i[4]}")')
        conn2.commit()
        conn1.close()
        conn2.close()
        rid=request.form.get('razorpay_payment_id')
        roid=request.form.get('razorpay_order_id')
        rsg=request.form.get('razorpay_signature')
        msg=roid+"|"+rid
        gs=hmac.new(str.encode(sec_key),msg.encode('UTF-8'),hashlib.sha256)
        dv=gs.hexdigest()
        if dv==rsg:
            render_template("thank.html")
            clnt.utility.verify_payment_signature({
                'razorpay_order_id': roid,
                'razorpay_payment_id': rid,
                'razorpay_signature': rsg})
        return ('',204)
        
@app.route('/tq')
def tq():
    global dish_orders
    print("!!!!!!!!!!!!!!!!!!!!!",dish_orders)
    for i in dish_orders:
        session.pop(i,None)
    return render_template('thank.html')

@app.route('/remove_item',methods=['POST'])
def remove_item():
    if request.method=='POST':
        print('rocky')
        d=request.form.get('item')
        session.pop(d,None)
        return('',204)




if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)
    


