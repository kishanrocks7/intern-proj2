#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash

# This is main app point
app = Flask(__name__)

#ROUTES

#Home Route
@app.route('/')
def home():
    return render_template('index.html')



    # Run from here
if __name__ == "__main__":
    app.run(debug=True)