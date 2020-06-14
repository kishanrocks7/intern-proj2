#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app

#importing database library
from databaselibrary import getdbcur



#universal unique ID package
import uuid,pybase64

from flask_mail import Mail, Message
# This is main app point
app = Flask(__name__)

#upload Folder config
app.config['UPLOAD_FOLDER']='./static/photos'
# mail configs

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codewithash99@gmail.com'
app.config['MAIL_PASSWORD'] = '12345@aB'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#warehouse functions
from warehouse import wdashboard,wreg,wareforget,respass,wareprofile,lgout,changepass
# producer functions
from producer import producerhome,addproducer,changeproducer,deleteproducer,searchproducer

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
    return respass()

@app.route('/producer')
def producer():
    return producerhome()


@app.route('/change_producer_details',methods = ['GET','POST'])
def change_producer_details():
    return changeproducer()

@app.route('/delete_producer_details',methods = ['GET','POST'])
def delete_producer_details():
    return deleteproducer()

@app.route('/search_producer',methods = ['GET','POST'])
def search_producer():
    return searchproducer()

@app.route('/add_producer', methods = ['GET','POST'])
def add_producer():
    return addproducer()

@app.route('/blogs')
def blogs():
    return render_template('blog.html')


@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/warehouse_profile', methods = ['GET','POST'])
def warehouse_profile():
    return wareprofile()

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

@app.route('/change_password',methods = ['GET','POST'])
def change_password():
    return changepass()

@app.route('/logout')
def logout():
    return lgout()


    # Run from here
if __name__ == "__main__":
    app.run(debug=True)