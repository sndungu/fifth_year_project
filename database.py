from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from datetime import datetime

SQLITE = 'sqlite'
Alerts = 'Alerts'
Credentials = 'Credentials'
Train_schedule = 'Train_schedule'


class MyDatabase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()

        alerts = Table(Alerts, metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       Column('Alert_Type', String),
                       Column('Alert_Message', String),
                       Column('Alert_Timestamp', String)
                       )
        train_schedule = Table(Train_schedule, metadata,
                               Column('id', Integer, primary_key=True, autoincrement=True),
                               Column('Train_No', String),
                               Column('Expected_timestamp', String),
                               Column('Passing_timestamp', String),
                               Column('passing_status', Boolean)
                               )
        credentials = Table(Credentials, metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('Lcd_display', String, nullable=False),
                            Column('Barrier_status', String),
                            Column('Phone_number', String)
                            )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def execute_query(self, query=''):
        if query == '': return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        output = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    output.append(row)
                result.close()
        return (output)

    # crud
    def data_query(self, table):
        if table == "Credentials":
            query = "SELECT Lcd_display, Barrier_status,Phone_number FROM {TBL_USR} WHERE id LIKE '1';".format(
                TBL_USR=table)
        if table == "Alerts":
            query = "SELECT id, Alert_Type,Alert_Message,Alert_Timestamp FROM {TBL_USR};".format(TBL_USR=table)
        if table == "Train_schedule":
            query = "SELECT Train_No,Expected_timestamp,Passing_timestamp,passing_status FROM {TBL_USR}; ".format(
                TBL_USR=table)
        return (self.print_all_data(query=query))

    def sample_delete(self, table):
        # Delete Data by Id
        query = "DELETE FROM {} WHERE id=3".format(table)
        self.execute_query(query)
        self.print_all_data(table)

    def sample_insert(self, table, r):
        # Insert Data
        if table == "Alerts":
            print(r)
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d/%b/%Y %H:%M:%S")
            query = "INSERT INTO {}(Alert_Type,Alert_Message,Alert_Timestamp) VALUES ({},{},{});".format(table, "'" + str(r['Alert_Type']) + "'","'" + str(r['Alert_Message']) + "'", "'" + str(timestampStr) + "'")

        self.execute_query(query)
        self.print_all_data(table)

    def sample_update(self, table):
        # Update Data
        query = "UPDATE {} set first_name='XXXX' WHERE id={id}" \
            .format(table, id=1)
        self.execute_query(query)
        self.print_all_data(table)


dbms = MyDatabase(SQLITE, dbname='mydb.sqlite')
