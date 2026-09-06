# 🎬 Movie Recommendation System

## 📌 Project Overview

This project is an AI-based Movie Recommendation System that recommends movies to users based on their movie preferences and ratings.

The system uses **User-Based Collaborative Filtering** and **Cosine Similarity** to identify users with similar movie preferences and recommend movies that the target user has not yet watched.

---

## 🚀 Features

- Load and analyze movie ratings data
- Clean and preprocess movie datasets
- Analyze movie ratings and genres
- Find the most popular movies
- Generate data visualizations
- Build a User-Movie Rating Matrix
- Find similar users using Cosine Similarity
- Recommend movies using Collaborative Filtering
- Generate personalized movie recommendations

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

---

## 📂 Dataset

This project uses the **MovieLens Dataset**.

The main dataset files are:

- `movies.csv`
- `ratings.csv`

The dataset contains information about movies, genres, users, and movie ratings.

---

## 🤖 Recommendation Algorithm

The system uses **User-Based Collaborative Filtering**.

### How It Works

```text
User Ratings
      ↓
User-Movie Rating Matrix
      ↓
Cosine Similarity
      ↓
Find Users With Similar Preferences
      ↓
Analyze Movies Rated by Similar Users
      ↓
Recommend Unwatched Movies

The system compares users based on their movie ratings and finds users with similar preferences.

Movies liked by similar users, but not yet watched by the target user, are recommended.

📊 Data Visualizations

The project generates visualizations such as:

📈 Top 10 Most Popular Movies
⭐ Movie Rating Distribution
🎭 Movie Genre Distribution
📁 Project Structure
Movie-Recommendation-System/
│
├── data/
│   ├── movies.csv
│   └── ratings.csv
│
├── output/
│   ├── popular_movies.png
│   ├── rating_distribution.png
│   ├── genre_distribution.png
│   └── movie_recommendations.csv
│
├── movie_recommendation.py
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation
1️⃣ Clone the Repository
git clone YOUR_REPOSITORY_URL
2️⃣ Navigate to the Project Folder
cd Movie-Recommendation-System
3️⃣ Create a Virtual Environment
python -m venv venv
4️⃣ Activate the Virtual Environment
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate
5️⃣ Install Required Libraries
pip install -r requirements.txt
▶️ Run the Project

Run the following command:

python movie_recommendation.py

The system will analyze the dataset, generate visualizations, and provide movie recommendations.

🧠 Concepts Used
Data Preprocessing
Exploratory Data Analysis (EDA)
User-Movie Rating Matrix
Collaborative Filtering
Cosine Similarity
Recommendation Systems
Data Visualization
🎯 Conclusion

This project successfully implements a Movie Recommendation System using User-Based Collaborative Filtering.

The system analyzes user ratings, identifies users with similar movie preferences using Cosine Similarity, and recommends movies that the target user has not already watched.

👨‍💻 Developer

Karthikeyan N G

Aspiring AI Engineer | Computer Science & Engineering (Cyber Security)

⭐ If you like this project, consider giving the repository a star!


## 📄 Also make sure your `requirements.txt` contains:

```text
pandas
numpy
matplotlib
seaborn
scikit-learn

This README is specifically for your Movie Recommendation System, so keep it in that project's folder—not inside your Karthikeyan AI Chatbot project.

no in this chatbot project

Ah, understood 👍 You mean what should be inside the README.md file for your Karthikeyan AI Chatbot project.

Create this file:

📄 README.md

Copy and paste this entire content:

# 🤖 Karthikeyan AI – Personal AI Assistant

A personalized AI chatbot and web application developed to provide information about **Karthikeyan N G** through an interactive and user-friendly chat interface.

The chatbot can answer questions related to education, academic information, skills, projects, career goals, hobbies, interests, family, CGPA, and professional profiles.

---

## ✨ Features

- 🤖 Interactive Personal AI Chatbot
- 👤 Personal Information
- 🎓 Education Details
- 🏫 School and College Information
- 📊 Academic Marks Information
- 📈 CGPA Information
- 💻 Technical Skills
- 🚀 Project Information
- 🎯 Career Goals
- 🎨 Hobbies and Interests
- 👨‍👩‍👦 Family Information
- 🔗 Clickable Professional Profile Links
- 🌙 Dark Mode
- ☀️ Light Mode
- 📱 Fully Responsive Design
- 💬 Modern Chat Interface

---

## 🛠️ Technologies Used

### Backend

- Python
- Flask

### Frontend

- HTML5
- CSS3
- JavaScript

### Other Technologies

- Google Fonts
- Responsive Web Design

---

## 📁 Project Structure

```text
AI-Chatbot-NLP/
│
├── app.py
├── chatbot.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
🤖 Chatbot Capabilities

The chatbot can answer questions about:

👤 Personal Information
Who is Karthikeyan?
Full Name
Preferred Name
Date of Birth
Age
City
🎓 Education
10th Standard Details
11th Standard Details
12th Standard Details
School Names
College Name
Department
Current Year of Study
Computer Science Group
📊 Academic Information
10th Marks
11th Marks
12th Marks
Subject-wise Marks
Mathematics Marks
Computer Science Marks
CGPA
💻 Technical Skills
Python
Java
C
JavaScript
HTML
CSS
React
Node.js
Git
GitHub
n8n
Vercel
Data Structures and Algorithms
🚀 Projects
Government Scheme Navigator
AI Movie Recommendation System
Hangman Game
🎯 Career

The chatbot can provide information about Karthikeyan's career goal of becoming an AI Engineer.

🎨 Hobbies and Interests

The chatbot can answer questions about hobbies and areas of interest.

👨‍👩‍👦 Family

The chatbot can provide information about family members.

🔗 Professional Profiles
LinkedIn
GitHub
LeetCode
⚙️ Installation
1. Clone the Repository
git clone YOUR_REPOSITORY_URL
2. Navigate to the Project Folder
cd AI-Chatbot-NLP
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt
▶️ Run the Application

Start the Flask application:

python app.py

Then open your browser and visit:

http://127.0.0.1:5000
🌙 User Interface

The website includes:

Premium AI chatbot interface
Royal and modern design
Dark mode as the default theme
Light/Dark theme toggle
Responsive design for mobile devices
Modern chat bubbles
Clickable hyperlinks
Clean and professional layout
📱 Responsive Design

The application is designed to work on:

📱 Mobile Phones
📱 Tablets
💻 Laptops
🖥️ Desktop Computers
🔮 Future Improvements

Future improvements for this project may include:

🧠 Advanced NLP Integration
🤖 Machine Learning Based Responses
🎤 Voice Assistant Support
💾 Database Integration
👤 User Authentication
🌐 Online Deployment
🔍 Improved Natural Language Understanding
💬 Conversation History
👨‍💻 Developer

Karthikeyan N G

Computer Science and Engineering (Cyber Security) Student
Aspiring AI Engineer

🔗 Connect With Me
LinkedIn: https://www.linkedin.com/in/karthikeyan-n-g-493b52323/
GitHub: https://github.com/karthikeyanng4-hash
LeetCode: https://leetcode.com/u/Karthi_keyan_007/
📄 License

This project was created for educational and personal portfolio purposes.

⭐ If you like this project, consider giving the repository a star!