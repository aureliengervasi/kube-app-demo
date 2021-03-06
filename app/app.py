import time 

from flask import Flask
from http import HTTPStatus
from werkzeug.exceptions import HTTPException

from threading import Thread
from prometheus_client import start_http_server, Counter


app = Flask(__name__)
num_requests = Counter("num_requests", "Example counter")


def compute():
    app.logger.info("Starting CPU-consuming thread")
    timeNow = int(round(time.time()))      
    timeToStop = timeNow + 200            
    while timeToStop > timeNow:          
        99 * 99                          
        timeNow = int(round(time.time()))
    app.logger.info("Ending CPU-consuming thread")

@app.route("/")
def hello():
    app.logger.info("this is a log line to the default route")
    num_requests.inc()                                    
    return "Hello Kubernetes!"

@app.route("/config")
def config():
    num_requests.inc()                                 
    with open('/etc/config/message', 'r') as f:
        return f.read()

@app.route("/healthz")
def healthz():
    return "Tutto bene!"

@app.route("/slow")                
def slow():                        
    t = Thread(target=compute)     
    t.start()                      
    return "CPU is going to heat"  

@app.errorhandler(HTTPException)
def handle_http_exception(exception: HTTPException):
    app.logger.error(f"Raised Exception: {exception}")
    return exception.description, exception.code

@app.errorhandler(Exception)
def handle_exception(exception: Exception):
    app.logger.error(f"Raised Exception: {exception}")
    return HTTPStatus.INTERNAL_SERVER_ERROR.description, HTTPStatus.INTERNAL_SERVER_ERROR

start_http_server(9001)                                   

