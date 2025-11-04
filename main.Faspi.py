from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import uvicorn
import os
# ==============================
# 1. Load Environment Variables
# ==============================
load_dotenv()
# ==============================
# 2. Initialize FastAPI App
# ==============================
app = FastAPI(
    title="Loan Approval Prediction API",
    description="A machine learning API that predicts loan approval based on applicant details.",
    version="1.0.0"
)
# ==============================================    
# 3. Loading Model and Scaler pkl Files
# ==============================================
try:
    model = joblib.load("best_model.pkl")
    scaler = joblib.load("scaler.pkl")
    print(":white_check_mark: Model and scaler loaded successfully.")
except Exception as e:
    print(f":x: Error loading model or scaler: {e}")
# ==============================================================
# 4. Define Input Schema Category and Numerical Features
# ==============================================================
class LoanFeatures(BaseModel):
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Gender: int
    Married: int
    Education: int
    Self_Employed: int
    Property_Urban: int
    Property_Semiurban: int
# ============================================
# 5. Important Health Check Endpoint 
# ==============================-=============
@app.get("/")
def home():
    return {
        "message": ":bank: Welcome to the Loan Approval Prediction API!!!",
        "docs_url": "/docs"
    }
# ============================================
# 6. Prediction Endpoint
# ============================================
@app.post("/predict")
def predict_loan_status(features: LoanFeatures):
    try:
        # Convert input to DataFrame
        data = pd.DataFrame([features.dict()])
        # ===================================================================
        # :small_blue_diamond: Recreate Engineered Features (as in training)
        # ====================================================================
        data["TotalIncome"] = data["ApplicantIncome"] + data["CoapplicantIncome"]
        data["Income_Loan_Ratio"] = data["TotalIncome"] / (data["LoanAmount"] + 1)
        # ===================================================================
        # :small_blue_diamond: Align Columns to Match Training
        # ===================================================================
        expected_columns = [
            'Credit_History' , 'Married' , 'Education' , 'TotalIncome' , 'Income_Loan_Ratio'
        ]
        # Add missing columns (with zeros if needed)
        for col in expected_columns:
            if col not in data.columns:
                data[col] = 0
        # Reorder columns to match training
        data = data[expected_columns]
        # =====================================
        # :small_blue_diamond: Apply Scaler
        # =====================================
        try:
            data_scaled = scaler.transform(data)
        except Exception as e:
            return {"error": f"Scaling failed: {e}"}
        # ==============================
        # :small_blue_diamond: Predict
        # ==============================
        prediction = model.predict(data_scaled)[0]
        probability = model.predict_proba(data_scaled)[0][1]
        result = "Approved" if prediction == 1 else "Not Approved"
        return {
            "prediction": result,
            "approval_probability": round(float(probability), 4)
        }
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}
# ===================================================================================================
# 7. Run Server( command uvicorn main:app --reload at terminal use this file name main.Faspi.py)
# ===================================================================================================
if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))