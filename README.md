# 📉 Customer Churn Prediction System

An end-to-end Machine Learning web application that predicts whether a customer is likely to churn (leave a service) or stay. This project demonstrates how data science, machine learning, and web technologies can be combined to solve a real-world business problem.

---

## 🧠 Introduction

Customer churn refers to the situation where customers stop using a company’s service. High churn rates directly impact revenue and growth. Companies such as telecom providers, banks, and SaaS platforms rely heavily on churn prediction systems to retain customers proactively.

This project builds a complete churn prediction system using Machine Learning and deploys it through a Flask-based web application with a simple frontend interface.

---

## 🎯 Problem Statement

Businesses struggle to identify customers who are likely to leave their services. Manual analysis is inefficient and error-prone. Hence, an automated churn prediction system is required to:

- Analyze customer behavior
- Predict churn in advance
- Enable data-driven retention strategies

---

## 🧩 Solution Overview

The solution uses historical customer data to train a machine learning model. The trained model is integrated with a Flask backend API and exposed through a web-based UI where users can input customer details and receive churn predictions instantly.

---

## 🏗️ System Architecture

User / Browser
   ↓
Frontend
   - HTML
   - CSS
   - JS
   ↓
Flask Backend
   - API & Validation
   ↓
ML Model (.pkl)
   - Churn Prediction
   ↓
Dataset
   - CSV / Features


## 🔄 Working Process

1. User enters customer information through the frontend UI  
2. Frontend sends data to the Flask backend using HTTP requests  
3. Backend validates and preprocesses the input data  
4. Trained ML model predicts churn outcome  
5. Prediction result is returned to frontend  
6. Result is displayed to the user  

---

## 🧪 Machine Learning Theory

Customer churn prediction is treated as a **binary classification problem** where:
- `1` → Customer will churn  
- `0` → Customer will not churn  

### ML Pipeline:
- Data Cleaning
- Feature Encoding
- Feature Scaling
- Model Training
- Model Evaluation
- Model Serialization (`.pkl`)

Algorithms used:
- Logistic Regression
- LightGBM (for better performance)

---
## 🔄 Working Theory / Machine Learning Workflow

The **Customer Churn Prediction System** works by analyzing historical customer data and predicting the likelihood of a customer leaving the service. Here's how it works under the hood:

### 1️⃣ Problem Type
- **Binary Classification:** Predicts if a customer will churn (`1`) or stay (`0`)  
- **Goal:** Minimize revenue loss by identifying high-risk customers early

### 2️⃣ Data Preprocessing
Before training the model, the raw data is cleaned and transformed:

- **Missing Value Handling:** Fill or remove incomplete records (e.g., `TotalCharges` sometimes empty)  
- **Categorical Encoding:** Convert categorical features like `Contract`, `PaymentMethod`, `InternetService` into numerical values using **Label Encoding or One-Hot Encoding**  
- **Feature Scaling:** Normalize numerical features (`Tenure`, `MonthlyCharges`, `TotalCharges`) using **StandardScaler** to ensure all features are on the same scale  
- **Feature Selection:** Select important features that strongly influence churn (e.g., `Contract`, `MonthlyCharges`, `InternetService`)  

### 3️⃣ Model Training
- **Algorithms used:**  
  - **Logistic Regression** → Simple and interpretable baseline model  
  - **LightGBM** → Gradient boosting tree model that handles categorical variables well and gives high predictive accuracy  
- **Train-Test Split:** Data is divided into training and testing sets (e.g., 80% train, 20% test)  
- **Cross-Validation:** Ensures the model performs well on unseen data  

### 4️⃣ Model Evaluation
- **Metrics:**  
  - **Accuracy:** Overall correctness of predictions  
  - **Precision & Recall:** Especially for churned customers (positive class)  
  - **F1-Score:** Balance between precision and recall  
  - **ROC-AUC:** Measures model’s ability to distinguish churn vs non-churn  

### 5️⃣ Model Serialization
- The trained model is saved as a **`.pkl` file** using Python’s `pickle` module  
- This allows the Flask backend to **load the model and make predictions** without retraining  

### 6️⃣ Backend Prediction Logic
- **Input:** Customer details from frontend (tenure, charges, contract, etc.)  
- **Processing:**  
  - Encode categorical inputs  
  - Scale numeric inputs  
- **Output:**  
  - **Churn Probability (%)**  
  - **Risk Level:** Low / Medium / Critical  
  - **Suggested Action:** e.g., offer discount, recommend upgrade, or engagement tips  

### 7️⃣ Business Insight
- High-risk customers can be targeted for **retention strategies**:  
  - Personalized discounts  
  - Upgrades to better plans  
  - Loyalty programs  
- Helps companies reduce churn and maximize revenue


## 🧰 Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- LightGBM
- Pandas
- NumPy

### Tools
- Git & GitHub
- VS Code

---

## 📁 Project Structure

customer-churn-prediction/
- data/                  # Dataset (added later)
- notebooks/             # EDA & experiments
- backend/               # Flask API
  - app.py
  - model_loader.py
  - requirements.txt
- frontend/              # UI
  - index.html
  - style.css
  - script.js
- model/                 # Saved ML models
  - churn_model.pkl
- screenshots/           # Output screenshots
- README.md              # Documentation
- .gitignore


## 📊 Dataset Description

The project uses the **Telco Customer Churn Dataset**, which includes features such as:

- Customer tenure
- Monthly charges
- Contract type
- Payment method
- Internet services
- Total charges

*Dataset will be added in later phases.*

