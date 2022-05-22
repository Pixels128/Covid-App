from flask import Flask, abort, request, jsonify
import sqlite3
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def flagWithCovid(id, hasCovid=True):
    con = sqlite3.connect('cases.db')
    cur = con.cursor()
    time = datetime.now()
    cur.execute("INSERT OR REPLACE INTO Cases (UserID, hasCovid, ReportedOn) VALUES (?, ?, ?) ", (id, hasCovid, time))
    con.commit()
    con.close()

def hasCovid(id):
    con = sqlite3.connect('cases.db')
    cur = con.cursor()
    cur.execute("SELECT hasCovid FROM Cases WHERE UserID = :userID", {"userID":id})
    data = cur.fetchall()
    con.close()
    if not data: return False
    return bool(data[0][0])

def dateReported(id):
    con = sqlite3.connect('cases.db')
    cur = con.cursor()
    cur.execute("SELECT ReportedOn FROM Cases WHERE UserID = :userID", {"userID":id})
    data = cur.fetchall()
    con.close()
    if not data: return None
    return str(data[0][0])

@app.get("/api/v2")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v2/{user_uuid}")
async def read_item(user_uuid: str):
    userHasCovid = hasCovid(user_uuid)
    covidReportedDate = dateReported(user_uuid)
    if userHasCovid and covidReportedDate:
        try:
            d1 = datetime.strptime(covidReportedDate, "%Y-%m-%d %H:%M:%S.%f")
            d2 = datetime.now()
            if d2 - d1 > timedelta(weeks=2):
                print("set with no covid")
                flagWithCovid(user_uuid, False)
        except ValueError:
            print("Bad value to compare times")

    rsp = {
        "hasCovid": hasCovid(user_uuid),
        "reportedOn": dateReported(user_uuid)
    }
    return rsp


@app.post("/api/v2/{user_uuid}")
async def post_user(user_uuid, hasCovid: bool):
    print(user_uuid, hasCovid)
    flagWithCovid(user_uuid)
    return {"OK": True}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info")


# app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def hello():
#     return "Endpoint: /api/v1/[ID]"



# @app.route("/api/v1/<id>", methods=["GET", "POST"])
# def show(id):
#     print(uuid)
#     response = jsonify({'some': 'data'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     # try:
#     uuid=str(uuid)
#     # except ValueError:
#         # return abort(404)
#     print(request.method)
#     if request.method == "POST":
#         print("Got POST", uuid)
#         flagWithCovid(uuid)
#     return {"hasCovid":hasCovid(uuid)}

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=80)