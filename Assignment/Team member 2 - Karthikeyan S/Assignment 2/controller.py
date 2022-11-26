from flask import *   
from flask import *
from model import Hackaholics
app=Flask(__name__)
app.secret_key = "div"

@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        if 'D_email' in session and session['D_email'] in email_addresses:
            email_addresses.remove(session['D_email'])
            del session['D_email']
        return render_template("home.html")

@app.route('/login',methods=["POST","GET"])
def Login():
    obj = Hackaholics()
    if request.method=="GET":
        return render_template("Login.html")
    elif request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        out=obj.get_email_patient(email)
        output=obj.get_email_doctor(email)
        if out:
            if out['Password']==password:
                return render_template("Patient_home.html",id=out['Id'])            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=out['Email'])

        elif output:
            if output['Password']==password:
                if email not in email_addresses:
                    email_addresses.append(email)
                    session['D_email']=email
                    print(email_addresses)
                return render_template("Patient_home.html",id=output['Id'])            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=output['Email'])
        else:
            flash("Email you have entered has not been registered. Please register")
            return render_template("Login.html")
        
        
# Patient_home
@app.route("/Patient_home/<id>",methods=["GET","POST"])
def Patient_home(id):
    return render_template("Patient_home.html",id=id)
    
@app.route('/patient_register',methods=["GET","POST"])
def Patient_register():
    obj=Hackaholics()
    if request.method=="GET":
        return render_template('Patient_register.html')
    elif request.method=="POST":
        patient_id = uuid.uuid4().hex
        data={
            'Id':patient_id,
            'Name': request.form['username'],
            'State': request.form['State'],
            'District':request.form['District'],
            'Age':request.form['age'],
            'Blood_Group':request.form['Blood_Group'],
            'Weight':request.form['Weight'],
            'Email': request.form['email'],
            'Password':request.form['password'],
            'MobileNo':request.form['mobileno']
        }
        out=obj.insert_into_patient(data)
        out = obj.insert_into_diagnostics(data['Id'])
        flash("You've been registered successfully!")
        return render_template("login.html")
        

if(__name__=="__main__"):
    app.run(debug=True)
