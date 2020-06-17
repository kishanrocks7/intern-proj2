#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app

#importing database library
from databaselibrary import getdbcur



#universal unique ID package
import uuid,pybase64,os
#secure Filename
from werkzeug.utils import secure_filename

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
    cur = getdbcur()
    sql = 'select * from team'
    cur.execute(sql)
    n = cur.rowcount
    teamdata = cur.fetchall()
    cur = getdbcur()
    sql = 'select * from flex'
    cur.execute(sql)
    flexdata = cur.fetchall()
    sql = 'select * from testimonial'
    cur.execute(sql)
    reviewdata = cur.fetchall()
    return render_template('index.html',teamdata = teamdata,flexdata = flexdata, reviewdata = reviewdata)
    

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

@app.route('/add_member',methods = ['GET','POST'])
def add_member():
    cur =getdbcur()
    if request.method == 'POST':
        if 'user_id' in session:
            name = request.form['name']
            position = request.form['position']
            msg = request.form['msg'].replace('\r\n','<br>')
            img = request.files['memberimg']
            path=os.path.basename(img.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            memberimg = secure_filename(imgfilename)
            addquery ='insert into team values (%s,%s,%s,%s) '
            cur.execute(addquery,(name,position,msg,memberimg))
            n = cur.rowcount
            if n == 1:
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],memberimg))
                flash('Member Added Successully !')
                return redirect(url_for('add_member'))
            flash('There is error while adding Member !')
            return redirect(url_for('add_member'))
        flash('You must Login first to add Team Member !')
        return redirect(url_for('warehouse_login')) #Tempo put this until Admin Dash is created
    return render_template('add_teammember.html')

@app.route('/add_flex',methods = ['GET','POST'])
def add_flex():
    cur =getdbcur()
    if request.method == 'POST':
        
            imageno = int(request.form['imageno'])
            heading = request.form['heading']
            body = request.form['body']
            img = request.files['fleximg']
            path=os.path.basename(img.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            fleximg = secure_filename(imgfilename)
            addquery = "update flex SET heading = %s , body = %s , image = %s WHERE id = %s"
            cur.execute(addquery,(heading,body,fleximg,imageno))
            n = cur.rowcount
            if n == 1:
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],fleximg))
                flash('Image Added Successully !')
                return redirect(url_for('add_flex'))
            flash('There is error while adding image !')
            return redirect(url_for('add_flex'))
        #flash('You must Login first to add image !')
        #return redirect(url_for('warehouse_login')) #Tempo put this until Admin Dash is created
    return render_template('flex.html')

@app.route('/client_review',methods = ['GET','POST'])
def client_review():
    if 'user_id' in session:
        id = session['user_id']
        checksql = "select name from testimonial where clientId='"+id+"'  "
        cur =getdbcur()
        cur.execute(checksql)
        m = cur.rowcount
        if m == 0:
            if request.method == 'POST':
                name = request.form['name']
                review = request.form['review'].replace('\r\n','<br>')
                rating = request.form['rating']
                img = request.files['img']
                path=os.path.basename(img.filename)
                file_ext=os.path.splitext(path)[1][1:]
                imgfilename=str(uuid.uuid4())+'.'+file_ext
                clientimg = secure_filename(imgfilename)
                addquery ='insert into testimonial values (%s,%s,%s,%s,%s) '
                cur.execute(addquery,(id,name,clientimg,rating,review))
                n = cur.rowcount
                if n == 1:
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'],clientimg))
                    flash('Review added Successfully..Thankyou for using Our services!')
                    return render_template('client_review.html')
                flash('There is error while adding review Please!')
                return redirect(url_for('add_member'))
            return render_template('client_review.html')
        flash('You have already give your review..!')
        return render_template('client_review.html')
    flash('You must Login first to give your review !')
    return redirect(url_for('warehouse_login')) #Tempo put this until Admin Dash is created

    # Run from here
if __name__ == "__main__":
    app.run(debug=True)