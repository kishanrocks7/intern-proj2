import uuid,base64
from databaselibrary import getdbcur
from flask import Flask,render_template,request,session,redirect,url_for,flash

password_key = 'secret4password'

def wreg():
    if request.method =='POST':
        fullkey = uuid.uuid4()
        uid = fullkey.time
        wname = str(base64.b64encode((request.form['warehouseName']).encode("utf-8")),"utf-8")
        mname = str(base64.b64encode((request.form['managerName']).encode("utf-8")),"utf-8")
        email = str(base64.b64encode((request.form['email']).encode("utf-8")),"utf-8")
        compno = str(base64.b64encode((request.form['companyNumber']).encode("utf-8")),"utf-8")
        pno = str(base64.b64encode((request.form['phoneNumber']).encode("utf-8")),"utf-8")
        address = str(base64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
        password  = str(base64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getdbcur()
        checkusersql = "select * from warehouse where (email = %s OR phoneNumber = %s )"
        cur.execute(checkusersql,(email,pno))
        checkusercount = cur.rowcount
        if checkusercount == 0 :
            insertusersql = 'insert into warehouse(id,warehouseName,managerName,companyNumber,phoneNumber,email,address,password) values (%s,%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertusersql,(uid,wname,mname,compno,pno,email,address,password))
            insertcount = cur.rowcount
            if insertcount >= 1 :
                flash('You have succesfully register, You can now login!')
                return redirect(url_for('warehouselogin'))
            else:
                return render_template('warehouseregister.html',failuremsg = "There is error!")
        else:
            return render_template('warehouseregister.html',failuremsg = "User is already registered with same Email or Phone Number!")
    return render_template('warehouseregister.html')
