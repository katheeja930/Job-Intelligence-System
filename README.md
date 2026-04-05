# Job Intelligence System

## Project Overview
This project predicts suitable tech career roles based on user-entered skills and provides job market insights such as top roles, top skills, fresher opportunities, top companies, and locations.

##  Features
- Career role prediction using Machine Learning
- Skill gap analysis
- Top in-demand skills
- Top hiring roles
- Fresher opportunities
- Skills required per role
- Top companies and locations

##  Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit

## Machine Learning Workflow
- Data Collection
- Data Cleaning
- Feature Engineering
- TF-IDF Vectorization
- Classification Model Training
- Prediction + Dashboard Deployment

##  How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
## 🌐 Live Demo
[Click here to use the app](https://job-intelligence-system-j9kysxwdoudy4wekbqd3or.streamlit.app)

##  Files
- `app.py` → Streamlit dashboard
- `career_role_model.pkl` → trained ML model
- `tfidf_vectorizer.pkl` → TF-IDF vectorizer
- `role_wise_skills.csv` → role-wise skill mapping
- `top_skills_frequency.csv` → top market skills
- `fresher_jobs_dataset.csv` → fresher job data

##  Future Improvements
- Salary prediction
- Resume matching
- Course recommendations
- Job recommendation engine
