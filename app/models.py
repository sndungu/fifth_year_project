# app/models.py

from datetime import datetime
from app import db

def save(field):
    db.session.add(field)
    db.session.commit()

def delete(field):
    db.session.delete(field)
    db.session.commit()

class Alert(db.Model):
    __tablename__ = 'Alerts'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    type = db.Column('Alert_Type', db.Text)
    message = db.Column('Alert_Message', db.Text)
    timestamp = db.Column('Alert_Timestamp', db.Text, default=datetime.now().strftime("%d/%b/%Y %H:%M:%S"))

    def __repr__(self):
        return f'<Alert {self.id}. Type: {self.type}.>'

    def save(self):
        save(self)

    def delete(self):
        delete(self)


class TrainSchedule(db.Model):
    __tablename__ = 'Train_schedules'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    number = db.Column('Train_No', db.Text)
    message = db.Column('Expected_timestamp', db.Text)
    timestamp = db.Column('Passing_timestamp', db.Text, default=datetime.now().strftime("%d/%b/%Y %H:%M:%S"))
    passed = db.Column('passing_status', db.Boolean)

    def __repr__(self):
        return f'<Train schedule: {self.id}>'

    def save(self):
        save(self)

    def delete(self):
        delete(self)

class Credential(db.Model):
    __tablename__ = 'Credentials'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    display = db.Column('Lcd_display', db.String, nullable=False)
    status = db.Column('Barrier_status', db.Text)
    phone_number = db.Column('Phone_number', db.Text, default=datetime.now().strftime("%d/%b/%Y %H:%M:%S"))

    def __repr__(self):
        return f'<LCD Display: {self.display}>'

    def save(self):
        save(self)

    def delete(self):
        delete(self)
