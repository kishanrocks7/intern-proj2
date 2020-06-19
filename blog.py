import uuid,pybase64,os
from random import randint
from blogdb import getblogcur
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from datetime import date
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
            session['blogger_name'] = str(pybase64.b64decode(logindata[1]),"utf-8")
            return redirect(url_for('blogs'))
        else:
            flash("Incorrect credentials!")
            return redirect(url_for('blogger_login'))
    return render_template('Blog/bloggerlogin.html')

def sendforgotpassmail(email):
    fullkey = uuid.uuid4()
    password = (fullkey.time)//10000000000
    passwd = str(pybase64.b64encode((str(password)).encode("utf-8")),"utf-8")
    cur = getblogcur()
    sql = "update blogger set password = %s where email = %s"
    cur.execute(sql,(passwd,email))
    n = cur.rowcount
    if n == 1:
        app = current_app._get_current_object()
        mail = Mail(app)
        subject = "Password Reset !"
        msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(email)])
        msg.body = "Hey ! you are requested to reset your password for your Login Account !!!" + "\n We are sending you a temporary Password . \n Change this after your first login under the profile section ." + "\n\n\n\n Password - "+str(password) 
        mail.send(msg) 
    else:
        flash("There is a problem with mail server !!")
        return redirect(url_for('blogger_forgot_password'))

def bloggerforgot():
    if request.method == "POST":
        email = request.form['email'].lower()
        cur = getblogcur()
        sql = "select * from blogger where (email = %s) "
        cur.execute(sql,(email))
        sqlres = cur.rowcount
        logindata= cur.fetchone()
        if sqlres == 1:
            sendforgotpassmail(email)
            flash("A Mail has been sent to you with further instructions !!")
            return redirect(url_for('blogger_login'))
        else:
            flash("You are not Registered with us as a Blogger !!")
            return redirect(url_for('blogger_forgot_password'))
    return render_template('Blog/bloggerforgotpass.html')

def bloggerprofile():
    if 'blogger_id' in session:
        id = session['blogger_id']
        cur = getblogcur()
        if request.method == 'POST':
            bloggerimg = request.files['bloggerimg']
            if bloggerimg:
                    checkphoto = "select image from blogger where id='"+id+"'"
                    cur.execute(checkphoto)
                    n=cur.rowcount
                    if n == 1:
                        prevphoto=cur.fetchone()
                        photo=prevphoto[0]
                        if photo != None:
                            os.remove("./static/photos/"+photo)
                    path=os.path.basename(bloggerimg.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    imgfilename=str(uuid.uuid4())+'.'+file_ext
                    bloggerimgname = secure_filename(imgfilename)
                    app = current_app._get_current_object()
                    bloggerimg.save(os.path.join(app.config['UPLOAD_FOLDER'],bloggerimgname))
            name = str(pybase64.b64encode((request.form['name']).encode("utf-8")),"utf-8")
            phone = str(pybase64.b64encode((request.form['phone']).encode("utf-8")),"utf-8")
            dob = str(pybase64.b64encode((request.form['dob']).encode("utf-8")),"utf-8")
            profession = str(pybase64.b64encode((request.form['profession']).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
            editprofsql = ' update blogger set name = %s,  phone = %s, dob = %s,  address = %s, profession = %s,   image = %s  where id = %s '
            viewprofsql = 'select * from blogger where id ="'+id+'"  '
            try:
                cur.execute(editprofsql,(name,phone,dob,address,profession,bloggerimgname,id))
            except:
                editprofsql = ' update blogger set name = %s,  phone = %s, dob = %s,  address = %s, profession = %s where id = %s '
                cur.execute(editprofsql,(name,phone,dob,address,profession,id))
            n = cur.rowcount
            cur.execute(viewprofsql)
            m = cur.rowcount
            if m==1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(1,len(cd[i])-1):
                        if(j!=2):
                            cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                return render_template('Blog/blogger_profile.html',profmsg = "Profile Updated !",pdata = td)
            return render_template('Blog/blogger_profile.html',profmsg = "There is error while changing data !",pdata = td) 
            #########GET##############################
        viewprofsql = 'select * from blogger where id ="'+id+'"  '
        cur.execute(viewprofsql)
        n = cur.rowcount
        if n == 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])-1):
                    if(j!=2):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('Blog/blogger_profile.html',pdata = td)
        return render_template('Blog/blogger_profile.html',profmsg = "There is error in displaying profile msg")
    flash('Direct access to this page is Not allowed !! Login First!')
    return redirect(url_for('blogger_login'))

def changebloggerpass():
    if 'blogger_id' in session:
        usid = session['blogger_id']
        if request.method == 'POST':
            oldpass = str(pybase64.b64encode((request.form['oldPassword']).encode("utf-8")),"utf-8")
            newpass = str(pybase64.b64encode((request.form['newPassword']).encode("utf-8")),"utf-8")
            cpass = str(pybase64.b64encode((request.form['confirmPassword']).encode("utf-8")),"utf-8")
            if(newpass != cpass):
                return render_template('Blog/changebloggerpassword.html',passmsg = "new password and confirm password doesn't match..")
            cur = getblogcur()
            cpasssql = "update blogger set password='"+newpass+"' where id = '"+usid+"' "
            cur.execute(cpasssql)
            n = cur.rowcount
            if n == 1:
                flash("password changed successfully !")
                session.pop('blogger_id',None)
                session.pop('blogger_name',None)
                return redirect(url_for('blogger_login'))
            return render_template('Blog/changebloggerpassword.html',passmsg = "New password is same as Old password")
        return render_template('Blog/changebloggerpassword.html')
    flash('Direct access to this page is Not allowed ..Login First!')
    return redirect(url_for('blogger_login'))

def addblog():
    if 'blogger_id' in session:
        ownerid = session['blogger_id']
        if request.method == 'POST': 
            ownername = str(pybase64.b64encode((session['blogger_name']).encode("utf-8")),"utf-8")
            d = str(pybase64.b64encode((str(date.today())).encode("utf-8")),"utf-8")
            fullkey = uuid.uuid4()
            blogId = fullkey.time
            title = str(pybase64.b64encode((request.form['title'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            content = str(pybase64.b64encode((request.form['content'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            img = request.files['blogimg']
            path=os.path.basename(img.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            blogimg = secure_filename(imgfilename)
            cur = getblogcur()
            insertblogsql = 'insert into blogs(blogId,ownerId,blogImage,title,content,ownerName,date) values (%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertblogsql,(blogId,ownerid,blogimg,title,content,ownername,d))
            n = cur.rowcount
            if n == 1:
                app = current_app._get_current_object()
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],blogimg))
                flash('Blog Added Successully !')
                return redirect(url_for('blogs'))
            flash('There is a problem while adding the Blog. Try again Later !!')
            return redirect(url_for('blogs'))
        return redirect(url_for('blogs'))
    flash('Direct access to this page is Not allowed ..Login First!')
    return redirect(url_for('blogger_login'))

def displayallblogs():
    cur = getblogcur()
    sql = 'select * from blogs'
    cur.execute(sql)
    n = cur.rowcount
    if n >= 1:
        data = cur.fetchall()
        print(data)
        cd = [list(i) for i in data]
        print(cd)
        for i in range(0,len(cd)):
            for j in range(3,len(cd[i])):
                cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
        td = tuple(tuple(i) for i in cd)
        return render_template('Blog/blog.html',bdata = td)
    flash('There is no blogs . Add some blogs here !!')
    return render_template('Blog/blog.html')    
