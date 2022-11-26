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


@app.route('/donorsearch/<id>',methods=["POST","GET"])
def Donor_Search(id):
    if request.method=="GET":
        return render_template("Donor_Search.html",id=id)
    elif request.method=="POST":
        obj = PlasmaModel()
        data={
            'BLOOD_GROUP':request.form['bloodgroup'],
            'STATE':request.form['State'],
            'DISTRICT':request.form['District']
        }
        output=obj.get_user_info_bloodgroup(data)
        return render_template("Donor_Filter.html",data=output,id=id,bloodgroup=request.form['bloodgroup'],state=request.form['State'],district=request.form['District'])

@app.route('/DonorFilter/<id>/<filter>/<bloodgroup>/<state>/<district>',methods=["POST","GET"])
def Donor_Filter(id,filter,bloodgroup,state,district):
    obj = PlasmaModel()
    data={
        'BLOOD_GROUP':bloodgroup,
        'STATE':state,
        'DISTRICT':district
    }
    if request.method=="GET":
        output=obj.get_donor_filter(data,filter)
        return render_template("Donor_Filter.html",data=output,id=id,bloodgroup=bloodgroup,state=state,district=district)

@app.route('/Recipient_Filter/<id>/<filter>',methods=["POST","GET"])
def Recipient_Filter(id):
    obj = PlasmaModel()
    if request.method=="GET":
        output=obj.get_pending_requests(id)
        return render_template("Recipient_Filter.html",id=id,data=output)

@app.route('/Donate/<id>',methods=["POST","GET"])
def Donate(id):
    obj = PlasmaModel()
    if request.method=="GET":
        output = obj.get_donations_info_id(id)
        return render_template("Recipient_Filter.html",id=id,data=output)

@app.route('/location_enter/<donor_id>/<donor_name>/<recipient_id>',methods=["POST","GET"])
def Location_enter(donor_id,donor_name,recipient_id):
    obj = PlasmaModel()
    recipient_info=obj.get_user_info_id(recipient_id)
    if request.method=="GET":
        data={
            'DONOR_ID':donor_id,
            'DONOR_NAME':donor_name,
            'RECIPIENT_ID':recipient_id,
            'RECIPIENT_NAME':recipient_info['NAME'],
            'DATE_OF_DONATION':str(date.today()),
            'BLOOD_GROUP':recipient_info['BLOOD_GROUP'],
            'MOBILE_NO':recipient_info['MOBILE_NO'],
            'DISTRICT':recipient_info['DISTRICT'],
            'STATE':recipient_info['STATE'],
            'STATUS':"Pending"
        }
        return render_template("EnterLocation.html",id=recipient_id,data=data)
    if request.method=="POST":
        Id=uuid.uuid1()
        tableData={
            'DONATE_ID':str(Id),
            'DONOR_ID':donor_id,
            'DONOR_NAME':donor_name,
            'RECIPIENT_ID':recipient_id,
            'RECIPIENT_NAME':recipient_info['NAME'],
            'DATE_OF_DONATION':str(date.today()),
            'BLOOD_GROUP':recipient_info['BLOOD_GROUP'],
            'LOCATION':request.form['location'],
            'STATUS':"Pending"
        }
        obj.insert_into_donations(tableData)
        # notify donors about the request
        msg_to_donor=Message('WE4U Plasma Donor Application',sender='19euit046@skcet.ac.in',recipients=['19euit046@skcet.ac.in'])
        msg_to_donor.html="<h2>Hello "+donor_name+",</h2><p>Hope you are doing well!</p><p>We hereby inform you that you have a request for Plasma by <b>  "+recipient_info['NAME']+"</b> residing at <b>"+recipient_info['AREA']+", "+recipient_info['DISTRICT'] +", "+ recipient_info['STATE']+"</b> <h4>We offer you a sincere thanks! <br>Your contribution will help us change lives!</h4><p>If you have any questions or concerns, please don't hesitate to contact us we4u@gmail.com. Thank You</p>"
        mail.send(msg_to_donor)

        return render_template("Thankyou_request.html",id=recipient_id)

@app.route('/accept_request/<id>/<donate_id>/<recipient_id>',methods=["POST","GET"])
def Accept_request(id,donate_id,recipient_id):
    obj = PlasmaModel()
    if request.method == "GET":
        obj.update_status_accepted(donate_id)
        donor_info=obj.get_user_info_id(id)
        reward_id=uuid.uuid1()
        data={
            'REWARD_ID':str(reward_id),
            'DONOR_ID':id,
            'DONOR_NAME':donor_info['NAME'],
            'REWARD_NAME':'20 Rs CashBack!!'
        }
        obj.insert_into_rewards(data)
        recipient_info=obj.get_user_info_id(recipient_id)
        donate_info=obj.get_donations_info_donateid(donate_id)

        # send mobile number of donor to recipient
        msg_to_recepient=Message('WE4U Plasma Donor Application',sender='19euit046@skcet.ac.in',recipients=['19euit046@skcet.ac.in'])
        msg_to_recepient.html="<h2>Hello "+recipient_info['NAME']+",</h2><p>Hope you are doing well!</p><p>We hereby inform you that the Donor you have requested for Plasma has accepted your request. </p><br><b>Here is the Mobile no of the donor - "+str(donor_info['MOBILE_NO'])+"</b><br><h4>We offer you a sincere thanks and gratitude for choosing our service!</h4><p>If you have any questions or concerns, please don't hesitate to contact us we4u@gmail.com. Thanks</p>"
        mail.send(msg_to_recepient)

        # send recipient information to donor
        msg_to_donor=Message('WE4U Plasma Donor Application',sender='19euit046@skcet.ac.in',recipients=['19euit046@skcet.ac.in'])
        msg_to_donor.html="<h2>Hello "+donor_info['NAME']+",</h2><p>Hope you are doing well!</p><p>Thank you coming forward to donate your blood.<b><b>Below mentioned is the address and contact number of the recepient</b><i>Location: "+donate_info[0]['LOCATION']+"  Mobile No: "+str(recipient_info['MOBILE_NO'])+"<br><h4>We offer you a sincere thanks and gratitude for choosing our service!</h4><p>If you have any questions or concerns, please don't hesitate to contact us we4u@gmail.com. Thanks</p>"
        mail.send(msg_to_donor)

        # send rewards to donor
        msg_to_donor=Message('WE4U Plasma Donor Application',sender='19euit046@skcet.ac.in',recipients=['19euit046@skcet.ac.in'])
        msg_to_donor.html="<h2>Hello "+donor_info['NAME']+",</h2><p>Thank you for your kind action</p><p>We hereby inform you that we have added a reward <br><b>"+data['REWARD_NAME']+"</b><h4>We offer you a sincere thanks for coming forward in donating plasma!</h4><p>If you have any questions or concerns, please don't hesitate to contact us we4u@gmail.com. Thanks</p>"
        mail.send(msg_to_donor)
        return render_template("Thankyou_request_accepted.html",id=id)

@app.route('/Profile/<id>',methods=["POST","GET"])
def Profile(id):
    obj=PlasmaModel()
    if request.method=="GET":
        output=obj.get_user_info_id(id)
        return render_template("Profile.html",id=id,data=output)
    
    elif request.method=="POST":
        data={
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
        data=obj.update_user_info(data,id)
        return render_template("Profile.html",id=id,data=data)

@app.route('/donate_history/<id>',methods=["POST","GET"])
def Donated_history(id):
    obj=PlasmaModel()
    if request.method == "GET":
        output=obj.get_completed_donations(id)
        return render_template("Donated_History.html",id=id,data=output)
    
@app.route('/Recipient_request/<id>',methods=["POST","GET"])
def Recipient_request(id):
    obj = PlasmaModel()
    if request.method=="GET":
        output=obj.get_pending_requests(id)
        return render_template("Recipient_requests.html",id=id,data=output)

@app.route('/Get_rewards/<id>',methods=["POST","GET"])
def Get_rewards(id):
    obj=PlasmaModel()
    if request.method=="GET":
        output = obj.get_rewards(id)
        return render_template("Rewards.html",id=id,data=output)


@app.route('/Logout',methods=["POST","GET"])
def Logout():
    if request.method=="GET":
        return render_template("Home.html")

if(__name__=="__main__"):
    app.run(debug=True)
