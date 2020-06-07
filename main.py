#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash

# This is main app point
app = Flask(__name__)

#ROUTES

#Home Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/outletlogin')
def warehouselogin():
    return render_template('outletlogin.html')

@app.route('/warehouselogin')
def outletlogin():
    return render_template('warehouselogin.html')

@app.route('/blogs')
def blogs():
    return render_template('blog.html')

@app.route('/faqs')
def faqs():
    return render_template('faq.html')

    # Run from here
if __name__ == "__main__":
    app.run(debug=True)