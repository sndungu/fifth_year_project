from flask import Flask,render_template,request
from database import MyDatabase,SQLITE, Alerts,Credentials,Train_schedule
import os
import json
import africastalking

dbms = MyDatabase(SQLITE, dbname='mydb.sqlite')

username = 'trainproject'
api_key = '1738901d383ca7e9309783f1581159919b5b2725955e72f071c1a22f7c563a3a'

africastalking.initialize(username, api_key)
sms = africastalking.SMS

app = Flask(__name__)
app.config['START_NGROK'] = os.environ.get('WERKZEUG_RUN_MAIN') != 'true'

@app.route('/create_tables',methods=['POST','GET'])
def create_tables():
    dbms.create_db_tables()
    return ("Done")

@app.route('/sms/',methods=['POST','GET'])
def sms1():
    print(request.data)
    data =json.loads(request.data.decode())
    print(data)
    status = data['status']
    number = '+254746630324'
    response = sms.send(str(status), [number])
    print(response)
    return ''

@app.route('/',methods=['POST','GET'])
def index():
    credentials = dbms.data_query("Credentials")
    alerts = dbms.data_query("Alerts")
    train_schedule = dbms.data_query("Train_schedule")
    LAST_TRAIN, NEXT_TRAIN = None, None

    for _train_schedule in train_schedule:
        if _train_schedule.passing_status == True:
            LAST_TRAIN = _train_schedule
        else:
            NEXT_TRAIN = _train_schedule

    return render_template('index.html',credentials=credentials,alerts=alerts,NEXT_TRAIN=NEXT_TRAIN ,LAST_TRAIN=  LAST_TRAIN)

@app.route('/Alerts',methods=['POST'])
def Alerts():
    print(request.data)
    try:
        data =json.loads(request.data.decode())
        print(data)
        alerts = dbms.data_query("Alerts")
        count = 0
        if len(alerts) >= 16:
            id = alerts[0][0]
            dbms.execute_query(f'DELETE FROM Alerts WHERE id={id}')
        dbms.sample_insert("Alerts",data)
    except Exception as err:
        print(err)
    return ("")

@app.route('/Credentials',methods=['POST'])
def Credentials():
    data =json.loads(request.data.decode())
    dbms.sample_update("Credentials",data)
    return ({"status":"succesful"})

port=4763

def update_alerts():
    dbms.sample_update(Alerts)
    # dbms.sample_delete() # delete data
    # dbms.sample_insert() # insert data

def start_ngrok():
    from pyngrok import ngrok

    # url = ngrok.connect(port).public_url
    # print(' * Tunnel URL:', url)

if __name__ == "__main__":
    if app.config['START_NGROK']:
        start_ngrok()
    app.run(debug=True,port=4763)
