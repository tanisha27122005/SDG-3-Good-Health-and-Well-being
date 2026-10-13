# 🧠 MindCare AI
### SDG 3 – Good Health and Well-being

**Developed by:** Tanisha  
**Academic Year:** 2026–2027  
**Project Domain:** Artificial Intelligence and Machine Learning  
**Application Type:** Web Application

---

## 1. Project Overview

MindCare AI is an educational AI-powered wellness-support web application designed to demonstrate how Artificial Intelligence, Machine Learning, data analysis, and interactive dashboards can support personal wellness awareness.

The application allows users to record daily wellness information, explore wellness patterns, view analytical summaries, and experiment with a trained educational machine-learning model.

This project aligns with **United Nations Sustainable Development Goal 3 (SDG 3): Good Health and Well-being**.

## 2. Project Objectives

- Develop an interactive wellness-support web application.
- Demonstrate machine-learning concepts using a trained Random Forest model.
- Record and analyze daily wellness check-ins.
- Explore patterns involving mood, stress, sleep, energy, and activity.
- Visualize available wellness data through dashboards.
- Provide an administrative interface for authorized access.
- Demonstrate responsible and privacy-conscious use of AI.

## 3. Main Features

### 3.1 Daily Check-in

Users can record daily wellness information, including:
- Mood
- Stress level
- Sleep duration
- Energy level
- Social support
- Physical activity

### 3.2 Dashboard

The dashboard presents summaries of available wellness records, historical information, and visualizations according to the implemented functionality.

### 3.3 AI/ML Lab

The AI/ML Lab demonstrates an educational Random Forest classification model.

- Loads the saved model using Joblib.
- Uses supported input features.
- Demonstrates machine-learning predictions.
- Provides an interface for exploring model outputs.

The model is not a clinically validated diagnostic system.

### 3.4 Wellness Pattern Explorer

Allows users to explore patterns in recorded wellness information, such as sleep, energy, stress, mood, and activity.

Observed patterns do not establish medical causation.

### 3.5 Wellness Chatbot

Provides basic educational wellness information and supportive prompts according to the application's implemented logic.

### 3.6 Insights & Export

Provides access to supported wellness insights, summaries, and data export functionality where implemented.

### 3.7 Admin Portal

Provides administrative functionality for authorized users. Depending on the actual implementation, this may include system statistics, check-in summaries, experiment information, and audit logs.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| SQLite | Local database |
| Pandas | Data processing |
| Scikit-learn | Machine learning |
| Random Forest | Classification model |
| Plotly | Data visualization |
| Joblib | Model persistence |
| Git | Version control |
| GitHub | Source code hosting |
| Visual Studio Code | Development environment |

## 5. Machine-Learning Workflow

The educational ML workflow consists of:

1. Loading the available wellness dataset.
2. Preparing input features.
3. Training the Random Forest model.
4. Evaluating the model using the training script.
5. Saving the trained model when configured.
6. Loading the saved model into the application.
7. Demonstrating predictions through the AI/ML interface.

The project may include `train_model.py`, `synthetic_wellness_data.csv`, and `wellness_model.joblib`.

If synthetic data is used, its results must not be presented as proof of clinical accuracy or real-world effectiveness.

## 6. Database

MindCare AI uses SQLite for local data storage.

**Database file:** `mindcare.db`

The database stores information according to the application's configured schema. Back up the database before deleting or resetting project data.

## 7. Project Structure

```text
MindCare_AI/
├── app.py
├── admin.py
├── train_model.py
├── mindcare.db
├── synthetic_wellness_data.csv
├── wellness_model.joblib
├── requirements.txt
├── README.md
└── pages/
    └── 10_Admin_Portal.py
```

This is an illustrative structure. Keep the actual files and folders present in your project.

## 8. System Requirements

- Windows, Linux, or macOS
- Python
- pip package manager
- Visual Studio Code
- A modern web browser
- Dependencies listed in `requirements.txt`

## 9. Complete Project Setup and Execution

### Step 1: Open the project

Open Visual Studio Code and select **File → Open Folder**.

Choose your `MindCare_AI` project folder.

### Step 2: Open the terminal

Select **Terminal → New Terminal**.

Move to your actual project directory. Example:

```powershell
cd "C:\Users\tanis\Downloads\MindCare_AI\MindCare_AI"
```

Change the path if your project is saved elsewhere.

### Step 3: Verify Python

```powershell
python --version
```

If necessary, use:

```powershell
py --version
```

### Step 4: Create a virtual environment

```powershell
py -m venv .venv
```

### Step 5: Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 6: Install dependencies

Ensure `requirements.txt` exists in the project root.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 7: Check required files

Confirm that the required application files, database, dataset, and model are present according to your implementation.

### Step 8: Train the model if required

If the saved model is missing, check that the dataset and training script are available.

```powershell
python train_model.py
```

Confirm from the terminal output that training completed successfully and the model was saved to the expected location.

### Step 9: Run the application

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL, commonly:

`http://localhost:8501`

Open that URL in your web browser.

**Keep the terminal running while using the application.**

### Step 10: Test the features

Verify the implemented features before submission:

1. Dashboard
2. Daily Check-in
3. AI/ML Lab
4. Wellness Pattern Explorer
5. Wellness Chatbot
6. Insights & Export
7. Admin Portal

### Step 11: Stop the application

Press `Ctrl + C` in the terminal running Streamlit.

### Step 12: Run the application again

Open the project directory in VS Code and run:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## 10. Admin Portal Login

The following credentials are intended for local academic demonstration, provided the administrator account is configured in the application.

- **Username:** `admin`
- **Password:** `MindCare@2026`

### Faculty Evaluation Instructions

1. Start the application using Streamlit.
2. Open the local application URL.
3. Navigate to the Admin Portal.
4. Enter the configured administrator credentials.
5. Review the available administrative features.

**Important:** Writing credentials in this README does not create an administrator account. The authentication code and database must already support the account.

**Security:** If the repository is public, remove the actual password from the README before uploading it. Share credentials with faculty separately.

## 11. Troubleshooting

### Error: `No module named streamlit`

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Error: `requirements.txt` not found

Run commands from the project root containing `requirements.txt`.

### Error: Model file not found

Check the model path configured in the application. Run `train_model.py` if the model needs to be generated.

### Error: Database file not found

Check the SQLite path and database initialization code.

### Error: Circular import involving `admin.py`

Ensure that `admin.py` does not import functions from itself. Move shared functions into a separate module when necessary and correct the Admin Portal imports.

### Error: Port 8501 is already in use

Try another port:

```powershell
python -m streamlit run app.py --server.port 8502
```

Open the URL displayed in the terminal.

## 12. GitHub Setup

Before publishing the project:

- Remove passwords and secrets from public files.
- Avoid uploading private wellness records.
- Verify that all required project files are included.
- Confirm that installation instructions match the actual implementation.

To commit the README:

```bash
git add README.md
git commit -m "Add MindCare AI project documentation"
git push
```

## 13. SDG 3 Alignment

MindCare AI aligns with **SDG 3 – Good Health and Well-being** through its educational exploration of digital wellness check-ins, personal data visualization, and machine-learning concepts.

The application supports awareness and learning rather than medical diagnosis or treatment.

## 14. Privacy and Responsible AI

- Protect administrator credentials.
- Restrict administrative access.
- Avoid publishing sensitive personal wellness data.
- Explain model limitations clearly.
- Do not use model predictions as medical advice.
- Use appropriate authentication and access controls.

## 15. Project Limitations

- Model performance depends on the dataset and evaluation method.
- Synthetic data may not represent real-world populations.
- The application is intended for academic demonstration.
- Features depend on the final implementation.
- The application is not clinically validated for diagnosis or treatment.

## 16. Conclusion

MindCare AI demonstrates the integration of web development, database management, data visualization, and machine learning in an educational wellness-support application.

The project provides practical experience with Python, Streamlit, SQLite, and Scikit-learn while exploring responsible technology use in alignment with SDG 3.

## 17. Project Information

- **Project Name:** MindCare AI
- **Developer:** Tanisha
- **Domain:** Artificial Intelligence and Machine Learning
- **Application Type:** Web Application
- **Technology Stack:** Python, Streamlit, SQLite, Scikit-learn, Pandas, Plotly, Joblib
- **SDG:** SDG 3 – Good Health and Well-being
- **Academic Year:** 2026–2027
- **Project Type:** Academic Project
