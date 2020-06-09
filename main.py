#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash
#importing database library
import uuid
from warehouse import wreg
from databaselibrary import getdbcur

# This is main app point
app = Flask(__name__)
app.secret_key= 'secret4key'
#ROUTES

#Home Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/warehouselogin')
def warehouselogin():
    return render_template('warehouselogin.html')

@app.route('/outlet_login')
def outlet_login():
    return render_template('outletlogin.html')

@app.route('/outlet_register')
def outlet_register():
    return render_template('outletregister.html')

@app.route('/warehouse_register',methods = ['GET','POST'])
def warehouse_register():
    return wreg()

@app.route('/warehouse_login')
def warehouse_login():
    return render_template('warehouselogin.html')

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

@app.route('/warehouse_dashboard')
def warehouse_dashboard():
    return render_template('warehouse_dashboard.html')

@app.route('/outlet_dashboard')
def outlet_dashboard():
    return render_template('outlet_home_1.html')


    # Run from here
if __name__ == "__main__":
    app.run(debug=True)