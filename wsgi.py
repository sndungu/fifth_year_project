from app import app
from database import dbms

if __name__ == "__main__":
    dbms.create_db_tables()
    app.run(debug=True)