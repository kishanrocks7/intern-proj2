#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app

#importing database library
from databaselibrary import getdbcur



#universal unique ID package
import uuid,pybase64

from flask_mail import Mail, Message
# This is main app point
app = Flask(__name__)


# mail configs

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codewithash99@gmail.com'
app.config['MAIL_PASSWORD'] = '12345@aB'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#warehouse functions
from warehouse import wdashboard,wreg,wareforget  #,wresest

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
    return wreg()

@app.route('/forgot_password',methods = ['GET','POST'])
def forgot_password():
    return wareforget()

@app.route('/reset_password',methods = ['GET','POST'])
def reset_password():
    if request.method == 'POST':
        user_id =  request.form['id']
        verifcode =  request.form['verifcode']
        passwd = str(pybase64.b64encode((request.form['pass']).encode("utf-8")),"utf-8")
        cur = getdbcur()
        idquery = 'select managerName from warehouse where id= "'+user_id+'" AND passwordResetCode = "'+verifcode+'"  '
        cur.execute(idquery)
        m =cur.rowcount
        if m == 1:
            resquery = ' update warehouse set password = %s  where (id = %s  AND passwordResetCode = %s) '
            cur.execute(resquery,(passwd, user_id, verifcode))
            n = cur.rowcount
            if n ==1 :
                flash('Your password is Changed ..You can now Login!')
                return redirect(url_for('warehouse_login'))
            else:
                return render_template('reset_password.html', samepassmsg ="You password is same as previous One..login from below")
        else:
                return render_template('reset_password.html', rmsg ="Either unique Id or verification code is incorrect.. please try again!")
    return render_template('reset_password.html')

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