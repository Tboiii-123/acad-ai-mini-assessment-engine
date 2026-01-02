
---

# 📝 Online Exam & Assessment API (Django REST)

This project is a **backend API for an online examination / CBT system** built with **Django Rest Framework (DRF)**.
It allows users to take exams, submit answers in bulk, and receive graded results automatically.

The system supports **objective questions** and can be extended to support **text similarity grading (TF-IDF + cosine similarity)**.

---

## 🚀 Features

* User authentication (Register & Login)
* List available exams
* View exam details with questions
* Submit answers **in bulk**
* Automatic grading
* View personal exam results
* Clean RESTful API structure
* Ready for Postman / frontend integration

---

## 🛠 Tech Stack

* **Python**
* **Django**
* **Django Rest Framework**
* **PostgreSQL** (recommended)
* **scikit-learn** (for TF-IDF & cosine similarity – optional grading bonus)

---

## 📂 Project Structure (Simplified)

```
acad_ai_engine/
│
├── acad_ai_engine/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── assessments/             # Main application
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   │
│   ├── grading/
│   │   ├── __init__.py
│   │   └── grader.py        # AI/Text grading logic
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md

```

---

## 🔐 Authentication Endpoints

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| POST   | `/auth/register/` | Register a new user |
| POST   | `/auth/login/`    | Login user          |

---

## 📘 Exam Endpoints

| Method | Endpoint              | Description                  |
| ------ | --------------------- | ---------------------------- |
| GET    | `/exam_list/`             | List all exams               |
| GET    | `/exam_detail/{id}/`  | Get exam details + questions |
| POST   | `/submit_exam/{id}/` | Submit exam answers          |
| GET    | `/view_submission/`    | View user results            |

---

## 📥 Submit Exam (Bulk Answers)

### Request Format

```json
{
  "answers": [
    {
      "question": 1,
      "answer": "A"
    },
    {
      "question": 2,
      "answer": "C"
    }
  ]
}
```

### Why Bulk Submission?

* Faster than multiple requests
* Fewer database hits
* Cleaner and more scalable

---

## 🧠 Grading Logic

* Objective questions are graded instantly
* Optional **text similarity grading** using:

  * **TF-IDF Vectorizer**
  * **Cosine Similarity**
* Can combine:

  * Keyword matching
  * Similarity score

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clonehttps://github.com/Tboiii-123/acad-ai-mini-assessment-engine.git
cd acad-ai-mini-assessment-engine
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Start Server

```bash
python manage.py runserver
```

---

## 🧪 Testing with Postman

* Use **JWT authentication**
* Test bulk answer submission using JSON
* Inspect scores and results via `/view_submission/`

---


## 📌 Future Improvements

* Timed exams
* Question randomization
* Admin analytics dashboard
* Essay grading with NLP
* Frontend integration (React / Next.js)


## 👨‍💻 Author

**Hussein Lawal**
Backend Developer | Python & Django
Focused on scalable APIs and assessment systems

---