#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash

# This is main app point
app = Flask(__name__)

#ROUTES

#Home Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/warehouselogin')
def warehouselogin():
    return render_template('outletlogin.html')

@app.route('/outletlogin')
def outletlogin():
    return render_template('warehouselogin.html')


@app.route('/outletregister')
def outletregister():
    return render_template('outletregister.html')

@app.route('/warehouseregister')
def warehouseregister():
    return render_template('warehouseregister.html')

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

@app.route('/database_crud')
def database_crud():
    return render_template('databasecrud.html')

    # Run from here
if __name__ == "__main__":
    app.run(debug=True)