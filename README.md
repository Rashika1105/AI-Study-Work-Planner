# AI Study & Work Planner

A complete, fully functional AI-powered planner with performance prediction, analytics, and a modern UI. Built with Python Flask and Machine Learning.

## 🚀 Features

- **Secure Authentication**: Register and login to manage your personal dashboard.
- **Smart Task Management**: Add, track, and complete study or work tasks with deadlines and hours spent.
- **ML Performance Prediction**: AI model predicts your future performance score based on your productivity patterns.
- **Burnout Detection**: Smart logic detects burnout risk based on work hours, sleep, and completion rates.
- **AI Suggestion Engine**: Rule-based smart suggestions to improve your productivity and well-being.
- **Interactive Analytics**: Visualize your progress with Plotly-powered charts and statistics.
- **PDF Report Generation**: Download a comprehensive performance report with analytics and AI suggestions.
- **Modern UI**: Dark/Light mode, Glassmorphism design, and fully responsive layout.

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Pandas, Scikit-learn, Joblib
- **Frontend**: Jinja2, Bootstrap 5, FontAwesome, Plotly.js, CSS3 (Glassmorphism)
- **Database**: SQLite

## 📦 Setup Instructions

1.  **Clone the project**:
    ```bash
    cd planner_ai_app
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Train the ML Model**:
    ```bash
    python models/train_model.py
    ```

4.  **Run the Application**:
    ```bash
    python app.py
    ```

5.  **Access the app**:
    Open `http://127.0.0.1:5000` in your web browser.

## 📂 Project Structure

- `app.py`: Main Flask application and routes.
- `models/`: ML model training script and the saved `.pkl` model.
- `utils/`: Logic for predictions, burnout detection, suggestions, and PDF generation.
- `templates/`: HTML templates with modern glassmorphism design.
- `static/`: CSS, JS, and generated reports.

## 📝 License
This project is open-source and ready for portfolio use.
