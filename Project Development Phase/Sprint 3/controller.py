from flask import *   
from flask_mail import *
from datetime import date
from datetime import datetime
import uuid
from model.model import PlasmaModel

app=Flask(__name__)
app.secret_key = "div"

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = '19euit046@skcet.ac.in'  
app.config['MAIL_PASSWORD'] = 'gauniganesh'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        return render_template("Home.html")

@app.route('/Login',methods=["POST","GET"])
def Login():
    obj = PlasmaModel()
    if request.method=="GET":
        return render_template("Login.html")
    elif request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        out=obj.get_user_info_email(email)
        if out:
            if out['PASSWORD']==password:
                return redirect(url_for("Landing_home",id=out['ID'])  )          
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=out['EMAIL'])
        else:
            flash("Email you have entered has not been registered. Please register")
            return render_template("Login.html")

@app.route('/Register',methods=["POST","GET"])
def Register():
    obj = PlasmaModel()
    if request.method=="GET":
        return render_template("sign_up.html")
    elif request.method=="POST":
        Id=uuid.uuid1()
        if int(request.form['age'])<18: 
            flash("Age is under than 18. Cannot register")
            return render_template("sign_up.html")
        if int(request.form['weight'])<50: 
            flash("Weight is under 50. Cannot register")
            return render_template("sign_up.html")

        data={
            'ID':str(Id),
            'NAME':request.form['username'],
            'AGE':request.form['age'],
            'DATE_OF_BIRTH':request.form['dob'],
            'WEIGHT':request.form['weight'],
            'GENDER':request.form['Gender'],
            'AREA':request.form['area'],
            'DISTRICT':request.form['District'],
            'STATE':request.form['State'],
            'EMAIL':request.form['email'],
            'PASSWORD':request.form['password'],
            'MOBILE_NO':request.form['mobileno'],
            'BLOOD_GROUP':request.form['bloodgroup']
        }
        obj.insert_into_users(data)
        flash("Successfully Registered!!")
        return render_template("Login.html")

@app.route('/Landing_home/<id>',methods=["POST","GET"])
def Landing_home(id):
    if request.method=="GET":
        return render_template("Landing_Home.html",id=id)


@app.route('/DonorSearch',methods=["POST","GET"])
def Donor_Search():
    if request.method=="GET":
        return render_template("Donor_Search.html")

@app.route('/DonorFilter',methods=["POST","GET"])
def Donor_Filter():
    if request.method=="POST" or request.method=="GET":
        return render_template("Donor_Filter.html")

@app.route('/Donate',methods=["POST","GET"])
def Donate():
    if request.method=="GET":
        return render_template("Recipient_Filter.html")

@app.route('/Profile/<id>',methods=["POST","GET"])
def Profile(id):
    if request.method=="GET":
        return render_template("Profile.html",id=id)

@app.route('/Logout',methods=["POST","GET"])
def Logout():
    if request.method=="GET":
        return render_template("Home.html")

if(__name__=="__main__"):
    app.run(debug=True)
