import ibm_db

dsn_hostname = "815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid = "yvq16906"
dsn_pwd = "ZMgfXgE7YvDXLbX4"
dsn_security="SSL"
dsn_SSLServerCertificate="DigiCertGlobalRootCA.crt"
dsn_database = "BLUDB"
dsn_port = "30367"

dsn = (
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "SECURITY={3};"
    "SSLServerCertificate={4};"
    "UID={5};"
    "PWD={6};"
).format(dsn_database,dsn_hostname,dsn_port,dsn_security,dsn_SSLServerCertificate,dsn_uid,dsn_pwd)

try:
    conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yvq16906;PWD=ZMgfXgE7YvDXLbX4', '', '')
    print(" Connected to database : ",dsn_database,"as user: ", dsn_uid," on host: ",dsn_hostname)
except:
    print("Unable to connect: ",ibm_db.conn_errormsg())

class PlasmaModel:
    def __init__(self):
        self.users=dsn_uid+".USERS"
        self.donations=dsn_uid+".DONATIONS"
        self.requests=dsn_uid+".REQUESTS"
        self.rewards=dsn_uid+".REWARDS"
        


    def insert_into_users(self,data):
        statement = "insert into "+self.users+" values('"+data['ID']+"','"+data['NAME']+"',"+data['AGE']+",'"+data['DATE_OF_BIRTH']+"',"+data['WEIGHT']+",'"+data['GENDER']+"','"+data['AREA']+"','"+data['DISTRICT']+"','"+data['STATE']+"','"+data['EMAIL']+"','"+data['PASSWORD']+"',"+data['MOBILE_NO']+",'"+data['BLOOD_GROUP']+"')"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        print("inserted---> to table ",self.users )

    def get_user_info_email(self,email):
        statement = "select * from "+self.users+" where EMAIL='"+email+"';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        if result: 
            resultset=ibm_db.fetch_both(result)
            print(resultset)
            return resultset
        else:
            return None

    def get_user_info_id(self,id):
        statement = "select * from "+self.users+" where ID='"+id+"';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        if result: 
            resultset=ibm_db.fetch_both(result)
            print(resultset)
            return resultset
        else:
            return None

    def update_user_info(self,data,id):
        update_value="NAME='"+data['NAME']+"',AGE="+data['AGE']+",DATE_OF_BIRTH='"+data['DATE_OF_BIRTH']+"',WEIGHT="+data['WEIGHT']+",GENDER='"+data['GENDER']+"',AREA='"+data['AREA']+"',DISTRICT='"+data['DISTRICT']+"',STATE='"+data['STATE']+"',EMAIL='"+data['EMAIL']+"',PASSWORD='"+data['PASSWORD']+"',MOBILE_NO="+data['MOBILE_NO']+",BLOOD_GROUP='"+data['BLOOD_GROUP']+"'"
        statement = "update "+self.users+" set "+update_value+"where ID='"+id+"';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        if result: 
            resultset=self.get_user_info_id(id)
            print(resultset)
            return resultset
        else:
            return None

    def get_user_info_bloodgroup(self,data):
        statement = "select * from "+self.users+" where BLOOD_GROUP='"+data['BLOOD_GROUP']+"' and STATE='"+data['STATE']+"' and DISTRICT='"+data['DISTRICT']+"'"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None

    def insert_into_donations(self,data):
        statement = "insert into "+self.donations+" values('"+data['DONATE_ID']+"','"+data['DONOR_ID']+"','"+data['DONOR_NAME']+"','"+data['RECIPIENT_ID']+"','"+data['RECIPIENT_NAME']+"','"+data['DATE_OF_DONATION']+"','"+data['BLOOD_GROUP']+"','"+data['LOCATION']+"','"+data['STATUS']+"')"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        print("inserted---> to table ",self.donations )

    def get_donor_filter(self,data,filter):
        if filter == "agelth":
            statement = "select * from "+self.users+" where BLOOD_GROUP='"+data['BLOOD_GROUP']+"' and STATE='"+data['STATE']+"' and DISTRICT='"+data['DISTRICT']+"' order by AGE desc"
        elif filter == "agehtl":
            statement = "select * from "+self.users+" where BLOOD_GROUP='"+data['BLOOD_GROUP']+"' and STATE='"+data['STATE']+"' and DISTRICT='"+data['DISTRICT']+"' order by AGE asc"
        elif filter == "genderm":
            statement = "select * from "+self.users+" where BLOOD_GROUP='"+data['BLOOD_GROUP']+"' and STATE='"+data['STATE']+"' and DISTRICT='"+data['DISTRICT']+"' and GENDER = 'Male'"
        elif filter == "genderf":
            statement = "select * from "+self.users+" where BLOOD_GROUP='"+data['BLOOD_GROUP']+"' and STATE='"+data['STATE']+"' and DISTRICT='"+data['DISTRICT']+"' and GENDER = 'Female'"
        else:
            statement = "select * from "+self.users+" where BLOOD_GROUP='"+data['BLOOD_GROUP']+"' and STATE='"+data['STATE']+"' and DISTRICT='"+data['DISTRICT']+"'"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None

    def get_donations_info_id(self,id):
        statement = "select * from "+self.donations+" where DONOR_ID='"+id+"';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None

    def get_donations_info_donateid(self,donate_id):
        statement = "select * from "+self.donations+" where DONATE_ID='"+donate_id+"';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None

    def update_status_accepted(self,donate_id):
        statement = "update "+self.donations+" set STATUS='Completed' where DONATE_ID='"+donate_id+"'"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        print("Updated-->"+self.donations)

    def insert_into_rewards(self,data):
        statement = "insert into "+self.rewards+" values('"+data['REWARD_ID']+"','"+data['DONOR_ID']+"','"+data['DONOR_NAME']+"','"+data['REWARD_NAME']+"')"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        print("inserted---> to table ",self.rewards )

    def get_completed_donations(self,id):
        statement = "select * from "+self.donations+" where DONOR_ID='"+id+"' and STATUS = 'Completed';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None

    def get_pending_requests(self,id):
        statement = "select * from "+self.donations+" where DONOR_ID='"+id+"' and STATUS = 'Pending';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None

    def get_rewards(self,id):
        statement = "select * from "+self.rewards+" where DONOR_ID='"+id+"';"
        print(statement)
        result = ibm_db.exec_immediate(conn,statement)
        result_fetch=ibm_db.fetch_both(result)
        resultset=[]
        if result_fetch: 
            resultset.append(result_fetch)
            resultset=[dict(r) for r in resultset] if resultset else None
            print(resultset)
            return resultset
        else:
            return None
# statement = "create table "+ dsn_uid + ".sample(Id int primary key not null, name varchar(10));"
# create_table=ibm_db.exec_immediate(conn,statement)
# print("Created table")
# statement = "insert into "+dsn_uid+".sample values(1, 'gauni');"
# result = ibm_db.exec_immediate(conn,statement)
    # statement = "select * from"+dsn_uid+".sample;"
    # stmt = ibm_db.exec_immediate(conn, statement)
    # print("statement---->",stmt)
    # dictionary = ibm_db.fetch_both(stmt)
    # while dictionary != False:
        # print("The ID is : ",  dictionary["ID"])
    
# print("cannot create table",ibm_db.conn_errormsg())