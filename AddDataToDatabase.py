import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountsKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-7397d-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2023-07-11 01:04:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-07-11 00:04:34"
        },
    "123456":
        {
            "name": "Nidhi Joshi",
            "major": "Computer",
            "starting_year": 2020,
            "total_attendance": 234,
            "standing": "BCA",
            "year": 6,
            "last_attendance_time": "2023-07-11 00:04:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
