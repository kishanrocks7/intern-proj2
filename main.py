#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash   

#importing database library
from databaselibrary import getdbcur

#warehouse functions
from warehouse import wdashboard

#universal unique ID package
import uuid,pybase64

from flask_mail import Mail, Message
# This is main app point
app = Flask(__name__)


# mail configs

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codewithash99@gmail.com'
app.config['MAIL_PASSWORD'] = '012345aB'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

app.secret_key= 'secret4key'
#ROUTES

#Home Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/warehouse_login')
def warehouse_login():
    return  render_template('warehouselogin.html')

@app.route('/warehouse_dashboard', methods = ['GET','POST'] )
def warehouse_dashboard():
    return wdashboard()

@app.route('/outlet_login')
def outlet_login():
    return render_template('outletlogin.html')

@app.route('/outlet_register')
def outlet_register():
    return render_template('outletregister.html')

@app.route('/warehouse_register',methods = ['GET','POST'])
def warehouse_register():
    if request.method =='POST':
        fullkey = uuid.uuid4()
        uid = fullkey.time
        em = request.form['email']
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
                subject = "Your registration successful !"
                msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
                msg.body = "Hey ! you are registered with us. \n Your unique id to access the dashboard is" + str(uid) + "\n Save this key for your future reference !!"
                mail.send(msg) 
                flash('You have succesfully register, You can now login!')
                return redirect(url_for('warehouse_login'))
            else:
                return render_template('warehouseregister.html',failuremsg = "There is error!")
        else:
            return render_template('warehouseregister.html',failuremsg = "User is already registered with same Email or Phone Number!")
    return render_template('warehouseregister.html')




@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/producer')
def producer():
    return render_template('producers.html')

@app.route('/blogs')
def blogs():
    return render_template('blog.html')

@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/blog_post')
def blog_post():
    return render_template('blog_post.html')

@app.route('/faqs')
def faqs():
    return render_template('faq.html')

@app.route('/warehouse_products')
def warehouse_products():
    return render_template('warehouse_products.html')

@app.route('/nearest_warehouses')
def nearest_warehouses():
    return render_template('nearestwarehouses.html')

@app.route('/database_crud')
def database_crud():
    return render_template('databasecrud.html')

@app.route('/staff_crud')
def staff_crud():
    return render_template('staffcrud.html')



@app.route('/outlet_dashboard')
def outlet_dashboard():
    return render_template('outlet_home_1.html')


    # Run from here
if __name__ == "__main__":
    app.run(debug=True)