#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
from random import randint
#secure Filename
from werkzeug.utils import secure_filename
#importing mail
from flask_mail import Mail, Message
from geopy.distance import geodesic 
from databaselibrary import getdbcur , getoutletcur
from producer import countbar
def getnearestwarehouse(id):
    sql = 'select latitude,longitude,id from warehouse '
    cur = getdbcur()
    cur.execute(sql)
    waredata = cur.fetchall()
    print(waredata)
    sql = 'select latitude,longitude from outlet where id = %s '
    cur = getoutletcur()
    cur.execute(sql,id)
    outdata = cur.fetchone()
    print(outdata)
    mind = 9999999999999
    warehouseid = 0
    for i in waredata:
        print(geodesic((i[0],i[1]),outdata).km)
        distance = geodesic((i[0],i[1]),outdata)
        if distance < mind :
            mind = distance
            warehouseid=i[2]
    print("minimum")
    print(warehouseid)
    print(mind)
    return warehouseid


def nearestone():
    if 'outlet_id' in session:
        warehouseid = getnearestwarehouse(session['outlet_id'])
        cbar = countbar(warehouseid)
        return render_template('Outlet/warehouse_products.html',cbar=cbar)
    flash('You must login first to view This page!')
    return redirect(url_for('outlet_login'))