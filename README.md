# 🎓 Attendance Tracking System

A simple, beginner-friendly **Attendance Tracking System** built with **Python**, **Tkinter**, and **MySQL**.
This project was created as a second-year B.Tech (Artificial Intelligence & Data Science) academic project.

It allows a teacher/admin to:
- Add student details
- Mark daily attendance (Present/Absent)
- View all attendance records
- Search attendance by student ID/roll number or name
- Generate attendance reports
- Automatically calculate attendance percentage


## 🛠️ Tech Stack

| Component        | Technology              |
|-------------------|--------------------------|
| Programming Language | Python 3.x           |
| GUI Library       | Tkinter (built into Python) |
| Database          | MySQL                   |
| DB Connector      | `mysql-connector-python` |

---

## 📁 Project Structure

```
attendance_system/
│
├── gui.py                  # Main GUI file – run this file to start the app
├── attendance_logic.py     # All business logic (add/search/report functions)
├── db_connection.py        # MySQL connection handling
├── schema.sql              # Database schema (run this in MySQL first)
├── requirements.txt        # Python dependencies
├── generate_screenshots.py # (optional) regenerates the mockup screenshots
├── screenshots/            # GUI screenshots used in this README
└── README.md
```

Each file has a single, clear responsibility:
- **gui.py** → only handles what the user *sees* and *clicks*
- **attendance_logic.py** → only handles the *rules* (calculations, validations)
- **db_connection.py** → only handles *talking to MySQL*

This separation makes the project much easier to debug and extend.

