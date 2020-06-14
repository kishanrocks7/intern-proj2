import uuid,pybase64,os
from random import randint
from databaselibrary import getdbcur
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

def wreg():
    if request.method =='POST':
        fullkey = uuid.uuid4()
        uid = fullkey.time
        em = request.form['email']
        passwd = request.form['password']
        cpasswd = request.form['confirmpassword']
        if(passwd!=cpasswd):
            #flash msg
            flash('Password and Confirm Password does not match')
            return redirect(url_for('warehouse_register'))
        wname = str(pybase64.b64encode((request.form['warehouseName']).encode("utf-8")),"utf-8")
        mname = str(pybase64.b64encode((request.form['managerName']).encode("utf-8")),"utf-8")
        email = str(pybase64.b64encode((request.form['email']).encode("utf-8")),"utf-8")
        compno = str(pybase64.b64encode((request.form['companyNumber']).encode("utf-8")),"utf-8")
        pno = str(pybase64.b64encode((request.form['phoneNumber']).encode("utf-8")),"utf-8")
        address = str(pybase64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
        password  = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getdbcur()
        checkusersql = "select * from warehouse where (email = %s OR phoneNumber = %s )"
        cur.execute(checkusersql,(email,pno))
        checkusercount = cur.rowcount
        if checkusercount == 0 :
            insertusersql = 'insert into warehouse(id,warehouseName,managerName,companyNumber,phoneNumber,email,address,password) values (%s,%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertusersql,(uid,wname,mname,compno,pno,email,address,password))
            insertcount = cur.rowcount
            if insertcount >= 1 :
                #getting mail app with app
                app = current_app._get_current_object()
                mail = Mail(app)
                subject = "Your registration successful !"
                msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
                msg.body = "Hey ! you are registered with us. \n Your unique id to access the dashboard is " + str(uid) + "\n Save this key for your future reference !!"
                mail.send(msg) 
                flash('You have succesfully register, You can now login!')
                return redirect(url_for('warehouse_login'))
            else:
                return render_template('warehouseregister.html',failuremsg = "There is error!")
        else:
            return render_template('warehouseregister.html',failuremsg = "User is already registered with same Email or Phone Number!")
    return render_template('warehouseregister.html')


def wdashboard():
    if request.method == "POST":
        user_id = request.form['userid']
        em_or_num = str(pybase64.b64encode((request.form['em_or_num']).encode("utf-8")),"utf-8")
        manager_name = request.form['manager_name']
        mname = str(pybase64.b64encode((request.form['manager_name']).encode("utf-8")),"utf-8")
        passwd = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getdbcur()
        sql = "select managerName from warehouse where (id = %s  AND (email = %s OR phoneNumber = %s ) AND managerName=%s AND password= %s ) "
        cur.execute(sql,(user_id, em_or_num, em_or_num , mname, passwd))
        sqlres = cur.rowcount
        mname = cur.fetchone()
        print(mname)
        if sqlres == 1 :
            session['user_id'] = user_id 
            session['user_name'] = manager_name
            return render_template('warehouse_dashboard.html', m_name = manager_name)
        else:
            flash("Incorrect credentials!")
            return redirect(url_for('warehouse_login'))
    return redirect(url_for('warehouse_login'))

def wareforget():
    if request.method == 'POST':
        user_id =  request.form['id']
        em = request.form['email']
        email = str(pybase64.b64encode((em).encode("utf-8")),"utf-8")
        randcode = randint(100000,999999)   #Generating 6 digit random int
        sql = ' update warehouse set passwordResetcode = %s where (id = %s  AND email = %s) '
        cur = getdbcur()
        cur.execute(sql,(randcode, user_id, email))
        n = cur.rowcount
        if n == 1 :
        #getting mail app with app
            app = current_app._get_current_object()
            mail = Mail(app)
            subject = "verification code for account"
            msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
            msg.body = "Your verification code for change password is " + str(randcode) 
            mail.send(msg) 
            flash('Check your verification code in your email')
            return  redirect(url_for('reset_password'))
        else:
            return render_template('forgot_password.html', fmsg ="Either unique Id or email is incorrect..try again!")
    return render_template('forgot_password.html')

def respass():
    if request.method == 'POST':
        user_id =  request.form['id']
        verifcode =  request.form['verifcode'] 
        passwd = str(pybase64.b64encode((request.form['pass']).encode("utf-8")),"utf-8")
        if(verifcode == None):
            flash("please fill out the verification code")
            return redirect(url_for('reset_password'))
        cur = getdbcur()
        idquery = 'select managerName from warehouse where id= "'+user_id+'" AND passwordResetCode = "'+verifcode+'"  '
        cur.execute(idquery)
        m =cur.rowcount
        if m == 1:
            resquery = ' update warehouse set password = %s  where (id = %s  AND passwordResetCode = %s) '
            cur.execute(resquery,(passwd, user_id, verifcode))
            n = cur.rowcount
            if n ==1 :
                delquery = ' update warehouse set passwordResetCode = %s  where id = %s '
                cur.execute(delquery,(uuid.uuid4().hex,user_id))
                flash('Your password is Changed ..You can now Login!')
                return redirect(url_for('warehouse_login'))
            else:
                return render_template('reset_password.html', samepassmsg ="You password is same as previous One..login from below")
        else:
                return render_template('reset_password.html', rmsg ="Either unique Id or verification code is incorrect.. please try again!")
    return render_template('reset_password.html')

def wareprofile():
    if 'user_id' in session:
        id = session['user_id']
        cur = getdbcur()
        if request.method == 'POST':
            wareimg = request.files['wareimg']
            if wareimg:
                    checkphoto = "select warehouseImage from warehouse where id='"+id+"'"
                    cur.execute(checkphoto)
                    n=cur.rowcount
                    if n == 1:
                        prevphoto=cur.fetchone()
                        photo=prevphoto[0]
                        if photo != None:
                            os.remove("./static/photos/"+photo)
                    path=os.path.basename(wareimg.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    imgfilename=str(uuid.uuid4())+'.'+file_ext
                    wimgname = secure_filename(imgfilename)
                    app = current_app._get_current_object()
                    wareimg.save(os.path.join(app.config['UPLOAD_FOLDER'],wimgname))
            warename = str(pybase64.b64encode((request.form['warename']).encode("utf-8")),"utf-8")
            manname = str(pybase64.b64encode((request.form['manname']).encode("utf-8")),"utf-8")
            manemail = str(pybase64.b64encode((request.form['manemail']).encode("utf-8")),"utf-8")
            compno = str(pybase64.b64encode((request.form['compno']).encode("utf-8")),"utf-8")
            manno = str(pybase64.b64encode((request.form['manno']).encode("utf-8")),"utf-8")
            wareaddress = str(pybase64.b64encode((request.form['wareaddress']).encode("utf-8")),"utf-8")
            isonum = request.form['isonum']
            editprofsql = ' update warehouse set warehouseName = %s,  managerName = %s, companyNumber = %s,  phoneNumber = %s, email = %s,  address = %s, warehouseImage = %s, isoNumber = %s  where id = %s '
            viewprofsql = 'select * from warehouse where id ="'+id+'"  '
            try:
                cur.execute(editprofsql,(warename,manname,compno,manno,manemail,wareaddress,wimgname,isonum,id))
            except:
                editprofsql = ' update warehouse set warehouseName = %s,  managerName = %s, companyNumber = %s,  phoneNumber = %s, email = %s,  address = %s, isoNumber = %s  where id = %s '
                cur.execute(editprofsql,(warename,manname,compno,manno,manemail,wareaddress,isonum,id))
            n = cur.rowcount
            cur.execute(viewprofsql)
            m = cur.rowcount
            if m==1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(1,len(cd[i])-3):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                return render_template('warehouse_profile.html',profmsg = "Profile Updated !",pdata = td)
            return render_template('warehouse_profile.html',profmsg = "There is error while changing data !",pdata = td) 
        viewprofsql = 'select * from warehouse where id ="'+id+'"  '
        cur.execute(viewprofsql)
        n = cur.rowcount
        if n == 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])-3):
                    cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            print(td)
            return render_template('warehouse_profile.html',pdata = td)
        return render_template('warehouse_profile.html',profmsg = "There is error in displaying profile msg")
    flash('Direct access to this page is Not allowed ..Login First!')
    return redirect(url_for('warehouse_login'))