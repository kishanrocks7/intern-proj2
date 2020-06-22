####################NECCESSARY IMPORTS ################
import uuid,pybase64
from random import randint
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message

############databaselib###################
from databaselibrary import getoutletcur

def outletclients():
    if 'outlet_id' in session:
        sql = 'select * from clients'
        cur = getoutletcur()
        cur.execute(sql)
        n = cur.rowcount
        if n >= 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])):
                    cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('Outlet/outlet_clients.html',pdata = td)
        else:
            return render_template('Outlet/outlet_clients.html', pmsg = "currently there is NO Producer information !")
    flash('You must login first to view Clients details!')
    return redirect(url_for('outlet_login'))

def addclient():
    if 'outlet_id' in session:
        if request.method == 'POST':
            fullkey = uuid.uuid4()
            uid = fullkey.time
            name = str(pybase64.b64encode((request.form['name'].lower()).encode("utf-8")),"utf-8")
            phoneNumber = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender'].lower()).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age'].lower()).encode("utf-8")),"utf-8")
            purpose = str(pybase64.b64encode((request.form['purposevisit'].lower()).encode("utf-8")),"utf-8")
            commodityType = str(pybase64.b64encode((request.form['commoditytype'].lower()).encode("utf-8")),"utf-8")
            lastvisited = str(pybase64.b64encode((request.form['lastvisited'].lower()).encode("utf-8")),"utf-8")
            addquery ='insert into clients values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cur = getoutletcur()
            cur.execute(addquery,( uid,name,age,gender,lastvisited,email,phoneNumber,commodityType,purpose))
            n = cur.rowcount
            if (n == 1):
                flash(' New Clients details added!')
                return redirect(url_for('outlet_clients'))
            else:
                flash( 'Adding new producer details failed!')
                return redirect(url_for('outlet_clients'))
        return redirect(url_for('outlet_clients'))
    flash('Direct access to this page is Not allowed !')
    return redirect(url_for('outlet_login'))
    