
# 📌 Face Recognition Attendance System

This project is a **Face Recognition-based Smart Attendance System** built using **Python, OpenCV, and Firebase Realtime Database**.

It detects student faces using a webcam, matches them with pre-stored encodings, and automatically **marks attendance in Firebase Database** while displaying student details on a custom background.

---

## ✨ Features

* 🎥 **Real-time face detection** using `face_recognition`
* 🔑 **Student authentication** by comparing face encodings
* 🖼️ **Custom UI background** for clean display
* 📊 **Attendance stored in Firebase Realtime Database**
* 📂 **Student images stored locally** (no Firebase Storage needed → avoids paid plan)
* 🔄 Updates:

  * Student **total attendance count**
  * **Last attendance timestamp**
* 🎓 Displays student info (Name, Major, Year, Attendance) with profile image

---

## 🏗️ Project Structure

```
📂 Face-Recognition-Attendance
│── EncodeGenerator.py         # Generates face encodings from local images
│── Main.py                    # Main script to detect faces & mark attendance
│── AddDatatoDatabase.py       # Add student details into Firebase Database
│── EncodeFile.p               # Pickle file storing encodings + student IDs
│── Images/                    # Student images (ID.png / ID.jpg)
│── Resources/
│   ├── background.png         # Main background UI
│   ├── Modes/                 # UI modes (default, loading, success, etc.)
│── serviceAccountKey.json     # Firebase Admin SDK key
│── requirements.txt           # Required dependencies
│── README.md                  # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```

### 2️⃣ Install Dependencies

Create a virtual environment (recommended) and install packages:

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Firebase

* Create a **Firebase project** at [Firebase Console](https://console.firebase.google.com/).
* Enable **Realtime Database**.
* Download `serviceAccountKey.json` and place it in the project root.
* Database structure example:

```json
"Students": {
  "321654": {
    "name": "Elon Musk",
    "major": "Robotics",
    "year": 3,
    "total_attendance": 7,
    "last_attendance_time": "2025-09-01 10:00:00"
  }
}
```

### 4️⃣ Add Student Images

* Place student images inside `Images/` folder.
* Name them by **student ID** (e.g., `321654.png`).

### 5️⃣ Generate Encodings

```bash
python EncodeGenerator.py
```

This will create `EncodeFile.p` with encodings + IDs.

### 6️⃣ Run Attendance System

```bash
python Main.py
```

✅ The system will open webcam → detect face → verify student → update Firebase → show info on screen.

---

## 🖥️ Demo Workflow

1. Webcam detects a student face.
2. Encodings compared with pre-stored encodings.
3. If match → draw bounding box, fetch student data, mark attendance.
4. Display student details (Name, Major, Year, Attendance).
5. Save updated attendance in Firebase Database.

---

## 📚 Requirements

* Python 3.8+
* OpenCV
* face\_recognition
* numpy
* cvzone
* firebase-admin

Install via:

```bash
pip install opencv-python face-recognition numpy cvzone firebase-admin
```

---



---

## 🤝 Contribution

Feel free to fork this repo, raise issues, and submit PRs to improve the system.

---
