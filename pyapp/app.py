from flask import Flask
from flask import Response
from flask import request
from metrics.metrics import setup_metrics
from models.client import GuestbookClient
from models.entry import Entry
import os
import json
import atexit
import platform

# Load environment vars
DB_USERAME = os.getenv('DB_USERNAME')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
CONNECTED = None
CLIENT = None

# Initialize flask app
app = Flask(__name__)
setup_metrics(app)

# Function to initialize db connection
@app.before_first_request
def init():
    global CLIENT
    global CONNECTED
    try:
        CLIENT = GuestbookClient(
            DB_NAME, DB_USERAME, DB_PASSWORD, DB_HOST, DB_PORT)
        CONNECTED = True
    except Exception as e:
        print(f"{e}")
        CONNECTED = False


# Function to teardown database connection
def teardown():
    global CLIENT
    if CLIENT is not None:
        CLIENT.disconnect()


# Set teardown to trigger on exit so that the database connection is destroyed
atexit.register(teardown)

# Get status of the db connection
@app.route("/dbhealth")
def db_connection_health():
    # Platform.node just added as a sanity check when running multiple replicas
    if CONNECTED:
        return Response(f"Database connection healthy on {platform.node()}", mimetype='text/plain', status=200)
    else:
        return Response(f"Database connection unhealthy {platform.node()}", mimetype='text/plain', status=500)

# Get status of the db connection
@app.route("/")
def get_main_guest_log():
    global CLIENT
    try:
        result = CLIENT.fetch_all_entries()
        return Response(json.dumps(result, default=str), mimetype='application/json')
    except Exception as e:
        return Response(f"Exception: {e}", mimetype='text/plain')

# Post method to add new guestbook entries
@app.route("/", methods=['POST'])
def post_entry_to_guest_log():
    global CLIENT
    try:
        content = request.get_json()
        # Create Entry object from request
        entry = Entry(content["firstname"],
                      content["lastname"], content["message"])
        result = CLIENT.insert_entry(entry)
        if result:
            # Row affected
            return Response(f"Created", mimetype='text/plain', status=201)
        else:
            # Row not affected
            return Response(f"Request not processed", mimetype='text/plain', status=422)
    except Exception as e:
        return Response(f"Exception: {e}", mimetype='text/plain', status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
