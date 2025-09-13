import firebase_admin
from firebase_admin import credentials

from firebase_admin import db
cred = credentials.Certificate("faceattendance-7493e-firebase-adminsdk-fbsvc-918b07cdfc.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendance-7493e-default-rtdb.firebaseio.com/"})


ref=db.reference('Students')

data={
    "E23CSEU1092":{
        "name":"Akagra",
        "major":"Computer Science",
        "starting_year":2023,
        "total_attendance":0,
        "standing":"A",
        "year":3,
        "last_attendance_time":"2025-09-9 10:39:00"
    },
    "E23CSEU1099":{
        "name":"Gaurav Yadav",
        "major":"Computer Science",
        "starting_year":2023,
        "total_attendance":0,
        "standing":"A",
        "year":3,
        "last_attendance_time":"2025-09-9 10:39:00"
    },
    "E23CSEU1131":{
        "name":"Abhibhava Raj Singh",
        "major":"Computer Science",
        "starting_year":2023,
        "total_attendance":0,
        "standing":"A",
        "year":3,
        "last_attendance_time":"2025-09-9 10:39:00"
    },
    "321654": { 
        "name": "Murtaza Hassan",
        "major": "Robotics",
        "starting_year": 2017, 
        "total_attendance": 7, 
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2025-09-9 10:39:00" 
        },
    "852741": { 
        "name": "Emly Blunt",
        "major": "Economics", 
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B", "year": 1,
        "last_attendance_time": "2025-09-9 10:39:00" 
        },
    "963852":{
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7, 
        "standing": "G",
        "year": 2, 
        "last_attendance_time": "2025-09-9 10:39:00"
        }
    }
for key, value in data.items():
    ref.child(key).set(value)
    