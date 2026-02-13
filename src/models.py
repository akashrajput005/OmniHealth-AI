import streamlit as st
import pickle
import numpy as np
from .config import DIABETES_MODEL_PATH, HEART_MODEL_PATH, PARKINSONS_MODEL_PATH

@st.cache_resource
def load_models():
    """Loads all models with caching for better performance."""
    models = {
        "diabetes": pickle.load(open(DIABETES_MODEL_PATH, 'rb')),
        "heart": pickle.load(open(HEART_MODEL_PATH, 'rb')),
        "parkinsons": pickle.load(open(PARKINSONS_MODEL_PATH, 'rb'))
    }
    return models

def safe_predict(model, features):
    """
    Performs prediction and returns binary result + probability if available.
    """
    try:
        data = np.array(features).reshape(1, -1)
        prediction = model.predict(data)
        
        prob = None
        if hasattr(model, "predict_proba"):
            try:
                prob_data = model.predict_proba(data)
                # Handle cases where it returns [[prob_neg, prob_pos]]
                if len(prob_data.shape) > 1 and prob_data.shape[1] > 1:
                    prob = float(prob_data[0][1])
                else:
                    prob = float(prob_data[0])
            except:
                prob = None
            
        return int(prediction[0]), prob
    except Exception as e:
        st.error(f"Prediction Error: {e}")
        return None, None
