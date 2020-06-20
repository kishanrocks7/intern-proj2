#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
from random import randint
#secure Filename
from werkzeug.utils import secure_filename
#importing mail
from flask_mail import Mail, Message
########importing database lib##########
from databaselibrary import getoutletcur
##############endlib ###############

def outletregister():
    if request.method =='POST':
        fullkey = uuid.uuid4()
        uid = fullkey.time
        em = request.form['email']
        passwd = request.form['password']
        cpasswd = request.form['confirmpassword']
        if(passwd!=cpasswd):
            #flash msg
            flash('Password and Confirm Password does not match')
            return redirect(url_for('outlet_register'))
        otype = str(pybase64.b64encode((request.form['type'].lower()).encode("utf-8")),"utf-8")
        mname = str(pybase64.b64encode((request.form['managername'].lower()).encode("utf-8")),"utf-8")
        email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
        cinno = str(pybase64.b64encode((request.form['cinno']).encode("utf-8")),"utf-8")
        pno = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
        address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
        password  = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getoutletcur()
        checkusersql = "select * from outlet where (email = %s OR contactNumber = %s )"
        cur.execute(checkusersql,(email,pno))
        checkusercount = cur.rowcount
        if checkusercount == 0 :
            insertusersql = 'insert into outlet(id,type,managerName,contactNumber,email,address,CINnumber,password) values (%s,%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertusersql,(uid,otype,mname,pno,email,address,cinno,password))
            insertcount = cur.rowcount
            if insertcount >= 1 :
                #getting mail app with app
                app = current_app._get_current_object()
                mail = Mail(app)
                subject = "Your registration successful !"
                msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
                msg.body = "Hey ! you are registered with us. \n Your unique id to access the Outlet dashboard is " + str(uid) + "\n Save this key for your future reference !!\n Thank you for choosing our services."
                mail.send(msg) 
                flash('You have succesfully register, You can now login as Oulet user !')
                return redirect(url_for('outlet_login'))
            else:
                return render_template('Outlet/outletregister.html',failuremsg = "There is error!")
        else:
            return render_template('Outlet/outletregister.html',failuremsg = "User is already registered with same Email or Phone Number!")
    return render_template('Outlet/outletregister.html')


def outletdash():
    if request.method == "POST":
        user_id = request.form['userid']
        em_or_num = str(pybase64.b64encode((request.form['em_or_num'].lower()).encode("utf-8")),"utf-8")
        manager_name = request.form['manager_name']
        mname = str(pybase64.b64encode((request.form['manager_name'].lower()).encode("utf-8")),"utf-8")
        passwd = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getoutletcur()
        sql = "select managerName from outlet where (id = %s  AND (email = %s OR contactNumber = %s ) AND managerName=%s AND password= %s ) "
        cur.execute(sql,(user_id, em_or_num, em_or_num , mname, passwd))
        sqlres = cur.rowcount
        mname = cur.fetchone()
        if sqlres == 1 :
            session['outlet_id'] = user_id 
            session['user_name'] = manager_name
            return render_template('Outlet/outlet_home.html', m_name = manager_name)
        else:
            flash("Incorrect credentials!")
            return redirect(url_for('outlet_login'))
    flash("You have to Login First!")
    return redirect(url_for('outlet_login'))

def outletforget():
    if request.method == 'POST':
        user_id =  request.form['id']
        em = request.form['email']
        email = str(pybase64.b64encode((em).encode("utf-8")),"utf-8")
        randcode = randint(100000,999999)   #Generating 6 digit random int
        sql = ' update outlet set resetcode = %s where (id = %s  AND email = %s) '
        cur = getoutletcur()
        cur.execute(sql,(randcode, user_id, email))
        n = cur.rowcount
        if n == 1 :
        #getting mail app with app
            app = current_app._get_current_object()
            mail = Mail(app)
            subject = "verification code for account"
            msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
            msg.body = "Your verification code  is " + str(randcode) +" after input you have to change your password!!" 
            mail.send(msg) 
            flash('Check your verification code in your email')
            return  redirect(url_for('reset_outlet_password'))
        else:
            return render_template('Outlet/forgot_outlet_password.html', fmsg ="Either unique Id or email is incorrect..try again!")
    return render_template('Outlet/forgot_outlet_password.html')

def resoutletpass():
    if request.method == 'POST':
        user_id =  request.form['id']
        verifcode =  request.form['verifcode'] 
        passwd = str(pybase64.b64encode((request.form['pass']).encode("utf-8")),"utf-8")
        if(verifcode == None):
            flash("please fill out the verification code")
            return redirect(url_for('reset_password'))
        cur = getoutletcur()
        idquery = 'select managerName from outlet where id= "'+user_id+'" AND resetcode = "'+verifcode+'"  '
        cur.execute(idquery)
        m =cur.rowcount
        if m == 1:
            resquery = ' update outlet set password = %s  where (id = %s  AND resetcode = %s) '
            cur.execute(resquery,(passwd, user_id, verifcode))
            n = cur.rowcount
            if n ==1 :
                delquery = ' update outlet set resetcode = %s  where id = %s '
                cur.execute(delquery,(uuid.uuid4().hex,user_id))
                flash('Your password is Changed ..You can now Login!')
                return redirect(url_for('outlet_login'))
            else:
                return render_template('Outlet/reset_outlet_password.html', samepassmsg ="You password is same as previous One..login from below")
        else:
                return render_template('Outlet/reset_outlet_password.html', rmsg ="Either unique Id or verification code is incorrect.. please try again!")
    return render_template('Outlet/reset_outlet_password.html')
