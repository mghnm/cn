from flask import Flask
from flask import Response
from flask import request
import psycopg2
from psycopg2.extras import RealDictCursor
from metrics.metrics import setup_metrics
import os
import json

#Load environment vars
DB_USERAME = os.getenv('DB_USERNAME')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
CONNECTED = False
CONNECTION = None

# Initialize flask app
app = Flask(__name__)
setup_metrics(app)

# Function to initialize db connection
@app.before_first_request
def init():
    try:
        global CONNECTION 
        CONNECTION = psycopg2.connect(dbname=DB_NAME, user=DB_USERAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        # Sql results are returned as a true dictionary format like json
        cur = CONNECTION.cursor(cursor_factory=RealDictCursor)
        print(f"Connected with following: dbname={DB_NAME}, user={DB_USERAME}, password=*******, host={DB_HOST}, port={DB_PORT}")
        global CONNECTED
        CONNECTED = True
        # Run query to create table if not exist
        cur.execute("CREATE TABLE IF NOT EXISTS guestbook( \
           firstname varchar(100), \
           lastname varchar(100), \
           message varchar(280), \
           entrytime timestamptz NOT NULL DEFAULT now() \
           )")
        CONNECTION.commit()
        cur.close()
    except Exception as e: 
        print(f"Exception: {e} params list \n dbname={DB_NAME}, user={DB_USERAME}, password={DB_PASSWORD}, host={DB_HOST}, port={DB_PORT}")


#Get status of the db connection
@app.route("/dbcon")
def dbconnhealth():
    if CONNECTED:
        return Response("Connected", mimetype='text/plain')
    else:
        return Response(f"Disconnected", mimetype='text/plain')


#Get status of the db connection
@app.route("/")
def getmainguestlog():
    cur = None
    try:
        cur = CONNECTION.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM guestbook")
        return Response(json.dumps(cur.fetchall(), default=str), mimetype='application/json')
    except Exception as e:
        return Response(f"Exception: {e}", mimetype='text/plain')
    finally:
        if cur:
            cur.close()

#Post method to add new guestbook entries
@app.route("/", methods = ['POST'])
def postguestlog():
    cur = None
    try:
        cur = CONNECTION.cursor(cursor_factory=RealDictCursor)
        #Got cursor to db now we can investigate request
        if True:
            content = request.get_json()
            #We need firstname, lastname and message
            cur.execute("INSERT INTO guestbook(firstname, lastname, message) \
                VALUES (%s, %s, %s)", (content["firstname"], content["lastname"], content["message"]))
            CONNECTION.commit()
            if cur.rowcount:
                # Row affected
                return Response(f"Created", mimetype='text/plain', status=201)
            else:
                #Row not affected
                return Response(f"Request not processed", mimetype='text/plain', status=422)
        else:
            #Bad request
            return Response(f"Bad request", mimetype='text/plain', status=400)
    except Exception as e:
        return Response(f"Exception: {e}", mimetype='text/plain')
    finally:
        if cur:
            cur.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)