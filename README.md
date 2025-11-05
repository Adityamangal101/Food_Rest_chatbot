# 🍛 Aadi's Eatery — AI-Powered Food Ordering Chatbot

**Aadi’s Eatery** is a smart restaurant website that integrates an **AI-powered chatbot named Aadi**, built using **Dialogflow** and connected to a **FastAPI backend**.  
The chatbot allows customers to place food orders seamlessly through natural conversation and automatically sends order details to the backend database.

---

## 🚀 Live Demo

🔗 **Website:** [https://aadis-eatery.onrender.com/](#)  
💬 **Chatbot:** Integrated on the website (powered by Dialogflow)  
⚙️ **Backend API:** Hosted on Render using FastAPI  
🗃️ **Database:** MySQL (hosted remotely)

---

## 🧠 Project Overview

This project combines:
- A **static restaurant website** (HTML, CSS, JavaScript)
- A **Dialogflow chatbot** named *Aadi* for conversational food ordering
- A **FastAPI backend** that handles orders, menu queries, and database operations
- A **MySQL database** that stores food item details and order history

Aadi interacts naturally with users, processes their order requests, and automatically communicates with the backend through webhooks to insert order details.

---

## 🏗️ Architecture

User → Dialogflow Chatbot (Aadi) → FastAPI Backend → MySQL Database
↑
│
Website (Frontend UI)

yaml
Copy code

### **Flow**
1. User interacts with Aadi chatbot on the restaurant website.
2. Chatbot extracts food item details and order quantity.
3. Dialogflow webhook sends structured JSON to FastAPI endpoint.
4. FastAPI verifies food item → inserts order → responds with confirmation.
5. Chatbot displays success message to user.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Chatbot** | Google Dialogflow |
| **Backend** | FastAPI (Python) |
| **Database** | MySQL (Remote Connection - Deployed on Railways) |
| **Hosting** | Render (Backend,Frontend), GitHub Pages |

---

## 📦 Features

✅ Interactive restaurant website with modern design  
✅ Fully automated chatbot ordering system  
✅ FastAPI backend connected to MySQL database  
✅ Handles order insertion and menu validation  
✅ Deployed API integrated with Dialogflow webhook  
✅ Mobile-responsive and optimized hero section  
✅ Secure environment variable management for API keys  

---

## 🔍 Example Chat Flow

> 👤 **User:** I’d like to order a Pizza.  
> 🤖 **Aadi:** Great choice! How many pizzas would you like?  
> 👤 **User:** Just one.  
> 🤖 **Aadi:** Your order for 1 Pizza has been successfully placed. ✅  
> (Order details automatically saved to backend database.)

---

## 🗂️ Folder Structure

FOOD_RESTAURANT_CHATBOT/
│
├── backend/
│ ├── db_helper.py # Database helper functions
│ ├── genric_fun.py # Utility functions
│ ├── main.py # FastAPI application entry point
│ ├── Dockerfile # Deployment configuration
│ ├── ngrok.exe # Local tunneling (for Dialogflow testing)
│ ├── pandeyji_eatery.db # SQLite/Database file
│ ├── requirements.txt # Dependencies for backend
│
├── frontend/
│ └── index.html # Static website with integrated chatbot
│
├── .env # Environment variables (DB credentials, API keys)
├── .gitignore # Git ignore rules
├── venv/ # Virtual environment
└── pycache/ # Compiled cache files

yaml
Copy code

---

## 🧑‍💻 How to Run Locally

1. **Clone the repository**
 
git clone https://github.com/your-username/Food_Rest_chatbot.git
cd Food_Rest_chatbot/backend

2. **Create a virtual environment**

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate (on Windows)

3. **Install dependencies**

pip install -r requirements.txt

Set up environment variables

DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database

Run FastAPI server

uvicorn main:app --reload

Open frontend

Open frontend/index.html in your browser and test chatbot.

🧩 Future Improvements
1.Add live order tracking

2.Integrate payment gateway

3.Add admin dashboard for restaurant staff

4.Support voice-based ordering

👨‍💻 Developer
Aditya Mangal
💼 Full Stack Developer | AI Chatbot Enthusiast
📍 India
🔗 LinkedIn:https://www.linkedin.com/in/adityamangalai/

