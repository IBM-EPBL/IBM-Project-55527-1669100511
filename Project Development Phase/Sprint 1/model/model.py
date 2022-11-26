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