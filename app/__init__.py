# app/__init__.py

from flask import Flask,render_template,request
from database import MyDatabase,SQLITE, Alerts,Credentials,Train_schedule
import os
import json
import africastalking
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))
username = 'trainproject'
api_key = '1738901d383ca7e9309783f1581159919b5b2725955e72f071c1a22f7c563a3a'

africastalking.initialize(username, api_key)
sms = africastalking.SMS

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydb.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    START_NGROK = os.environ.get('WERKZEUG_RUN_MAIN') != 'true'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

@app.route('/create_tables',methods=['POST','GET'])
def create_tables():
    db.create_all()
    return ("Done")

@app.route('/sms/<number>/<status>',methods=['POST','GET'])
def sms1(number,status):
    return sms.send(str(status), [number])

@app.route('/',methods=['POST','GET'])
def index():
    credentials = models.Credential.query.all()
    alerts = models.Alert.query.all()[-18:]
    train_schedule = models.TrainSchedule.query.all()

    for _train_schedule in train_schedule:
        if _train_schedule.passing_status == True:
            LAST_TRAIN = _train_schedule
        else:
            NEXT_TRAIN = _train_schedule

    return render_template('index.html',credentials=credentials,alerts=alerts,NEXT_TRAIN=None ,LAST_TRAIN=  None)

@app.route('/Alerts',methods=['POST'])
def Alerts():
    print(request.data)
    data =json.loads(request.data.decode())
    print(data)
    alert = models.Alert(type=f"'{data['Alert_Type']}'",message=f"'{data['Alert_Message']}'")
    alert.save()
    return ("")

@app.route('/Credentials',methods=['POST'])
def Credentials():
    data =json.loads(request.data.decode())
    cred = models.Credential.query.filter_by(id=1).first()
    print(cred)
    return ({"status":"succesful"})
