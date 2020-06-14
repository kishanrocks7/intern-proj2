import uuid,pybase64
from random import randint
from databaselibrary import getdbcur
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message


def producerhome():
    if 'user_id' in session:
        sql = 'select * from producer'
        cur = getdbcur()
        cur.execute(sql)
        n = cur.rowcount
        if n >= 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])):
                    cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('producers.html',pdata = td)
        else:
            return render_template('producers.html', pmsg = "currently there is Producer information !")
    flash('You must login first to view Producers!')
    return redirect(url_for('warehouse_login'))

def addproducer():
    if 'user_id' in session:
        if request.method == 'POST':
            fullkey = uuid.uuid4()
            uid = fullkey.time
            name = str(pybase64.b64encode((request.form['name']).encode("utf-8")),"utf-8")
            phoneNumber = str(pybase64.b64encode((request.form['phoneNumber']).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email']).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender']).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age']).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
            commodityType = str(pybase64.b64encode((request.form['commodityType']).encode("utf-8")),"utf-8")
            commodityUnits = str(pybase64.b64encode((request.form['commodityUnits']).encode("utf-8")),"utf-8")
            addquery ='insert into producer values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cur = getdbcur()
            cur.execute(addquery,( uid,name,age,gender,phoneNumber,email,address,commodityType,commodityUnits ))
            n = cur.rowcount
            if (n == 1):
                flash(' New Producer details added!')
                return redirect(url_for('producer'))
            else:
                return render_template('producers.html', pmsg = 'Adding new producer details failed!')
        return render_template('producers.html')
    flash('Direct access to this page is Not allowed !')
    return redirect(url_for('warehouse_login'))
    

#change_producer_details' delete_producer_details

def changeproducer():
    if 'user_id' in session:
        if request.method == 'POST':
            id =request.form['id']
            name = str(pybase64.b64encode((request.form['producername']).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['produceremail']).encode("utf-8")),"utf-8")
            number = str(pybase64.b64encode((request.form['producernumber']).encode("utf-8")),"utf-8")
            commoditytype = str(pybase64.b64encode((request.form['commoditytype']).encode("utf-8")),"utf-8")
            commodityunits = str(pybase64.b64encode((request.form['commodityunits']).encode("utf-8")),"utf-8")
            editquery = 'update producer set name =%s,emailId=%s,contactNumber=%s,commodityType=%s,commodityUnits=%s  where unique_key=%s '
            cur =getdbcur()
            cur.execute(editquery,(name,email,number,commoditytype,commodityunits,id))
            n =cur.rowcount
            if n == 1:
                flash('producers Details changed Successfully !')
                return redirect(url_for('producer'))
            else:
                flash('There is error in changing producers details !')
                return redirect(url_for('producer'))
        return redirect(url_for('producer'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('warehouse_login'))

def deleteproducer():
    if 'user_id' in session:
        if request.method == 'POST':
            id = request.form['id']
            delquery = 'delete from producer where unique_key="'+id+'"   '
            cur =getdbcur()
            cur.execute(delquery)
            n =cur.rowcount
            if n == 1:
                flash('producers Details deleted Successfully !')
                return redirect(url_for('producer'))
            else:
                flash('There is error in deleting producers details !')
                return redirect(url_for('producer'))
        return redirect(url_for('producer'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('warehouse_login'))

def searchproducer():
    if 'user_id' in session:
        if request.method == 'POST':
            si = str(pybase64.b64encode((request.form['searchinput']).encode("utf-8")),"utf-8")
            searchquery = "select * from producer where (name like  '%"+si+"%'  OR commodityType like   '%"+si+"%' )  "
            cur =getdbcur()
            cur.execute(searchquery)
            n =cur.rowcount
            if n == 1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(1,len(cd[i])):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                session['searchdata'] = td
                flash('Results For your search !')
                return redirect(url_for('producer'))
            else:
                flash('There is error in searching producers details !')
                return redirect(url_for('producer'))
        return redirect(url_for('producer'))
    flash('Direct access to this page is Not Allowed Login first To view this page!')
    return redirect(url_for('warehouse_login'))