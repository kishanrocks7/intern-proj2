import uuid,pybase64,os
from random import randint
from blogdb import getblogcur
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

def bloggerregister():
    if request.method  == "POST":
        fullkey = uuid.uuid4()
        uid = fullkey.time
        em = request.form['email'].lower()
        passwd = request.form['password']
        cpasswd = request.form['confirmpassword']
        if(passwd!=cpasswd):
            #flash msg
            flash('Password and Confirm Password does not match')
            return redirect(url_for('blogger_register'))
        name = str(pybase64.b64encode((request.form['bloggerName']).encode("utf-8")),"utf-8")
        email = (request.form['email'].lower())
        pno = str(pybase64.b64encode((request.form['phoneNumber']).encode("utf-8")),"utf-8")
        dob = str(pybase64.b64encode((request.form['dob']).encode("utf-8")),"utf-8")
        gender = str(pybase64.b64encode((request.form['gender']).encode("utf-8")),"utf-8")
        profession = str(pybase64.b64encode((request.form['profession']).encode("utf-8")),"utf-8")
        address = str(pybase64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
        password  = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getblogcur()
        checkusersql = "select * from blogger where (email = %s)"
        cur.execute(checkusersql,(em))
        checkusercount = cur.rowcount
        if checkusercount == 0 :
            insertusersql = 'insert into blogger(id,name,email,phone,dob,gender,address,profession,password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertusersql,(uid,name,email,pno,dob,gender,profession,address,password))
            insertcount = cur.rowcount
            if insertcount >= 1 :
                #getting mail app with app
                app = current_app._get_current_object()
                mail = Mail(app)
                subject = "Your registration successful !"
                msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
                msg.body = "Hey ! you are registered with us as a Blogger !!!"
                mail.send(msg) 
                flash('You have succesfully register, You can now login!')
                return redirect(url_for('blogger_login'))
            else:
                return render_template('Blog/bloggerregister.html',failuremsg = "There is error!")
        else:
            return render_template('Blog/bloggerregister.html',failuremsg = "User is already registered with same Email !")
    return render_template('Blog/bloggerregister.html')

def bloggerlogin():
    if request.method == "POST":
        email = request.form['email'].lower()
        passwd = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getblogcur()
        sql = "select id,name from blogger where (email = %s   AND password= %s ) "
        cur.execute(sql,(email, passwd))
        sqlres = cur.rowcount
        logindata= cur.fetchone()
        print(logindata)
        if sqlres == 1 :
            session['blogger_id'] = logindata[0]
            session['blogger_name'] = logindata[1]
            return redirect(url_for('blogs'))
        else:
            flash("Incorrect credentials!")
            return redirect(url_for('blogger_login'))
    return render_template('Blog/bloggerlogin.html')
