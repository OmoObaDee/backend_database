# ================================
# FASTAPI MODEL DEPLOYMENT
# ================================

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Initialize app
app = FastAPI(title="Easy Visa Case Prediction API", version="1.0")

# Load saved model and features
model = joblib.load("best_model.pkl")
feature_list = pd.read_csv("feature_importance.csv")["0"].tolist()
scaler = joblib.load("scaler.pkl")  # Optional if you saved it earlier

# Define input schema
class easy_visaInput(BaseModel):
    education_of_employee : float
    has_job_experience: float
    requires_job_training: float
    no_of_employees :str
    yr_of_estab:str
    region_of_employment:object
    prevailing_wage:float
    unit_of_wage:object
    full_time_position:object
    case_status:object
    # Add any other features used during training
    # Example:
    # job_title: int
    # region_code: int

@app.get("/")
def home():
    return {"message": "Easy Visa Case Prediction API is live!"}

@app.post("/predict")
def predict(data: easy_visaInput):
    # Convert input data to DataFrame
    df_input = pd.DataFrame([data.dict()])
    
    # Ensure all columns match model training order
    df_input = df_input.reindex(columns=feature_list, fill_value=0)
    
    # Apply same scaler (if used)
    try:
        df_scaled = scaler.transform(df_input)
    except:
        df_scaled = df_input  # fallback if not using scaling
    
    # Make prediction
    pred = model.predict(df_scaled)
    prob = model.predict_proba(df_scaled).max()
    
    return {
        "prediction": str(pred[0]),
        "confidence": round(float(prob), 3)
    }
