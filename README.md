# 🤖 AI Call Center Dashboard

This is a fully functional, AI-powered call center simulation built using **Streamlit** (frontend) and **Twilio Voice API** (backend). It simulates real-time user interactions, tracks agent availability, and fetches live call data & recordings via Twilio APIs.

---

## 🚀 Live Project

👉 [Click here to view the deployed Streamlit dashboard](https://ai-call-center-dashboard-eezagb4bq7bar2fghegcc4.streamlit.app/)

---

## 📞 How It Works

- User calls the AI Call Center via a Twilio number
- The bot collects user details (e.g., name and age)
- System routes the call to the first available human agent (from a JSON agent pool)
- Logs, recordings, and agent data are displayed on a real-time dashboard

---

## 📊 Features

- 🔄 Real-time Twilio call logs
- 📁 Call recordings viewer with play/download options
- 👥 Agent status tracker (Available / Busy)
- 📈 Bar and Line charts for call metrics
- 🌑 Fully responsive dark theme UI
- 🔒 Secure credential handling using environment variables

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **Backend/API:** Twilio Voice API
- **Data:** JSON & Live API calls
- **Deployment:** Streamlit Cloud
- **Extras:** Python-dotenv, Chart components, Ngrok (for local testing)
