import pickle
import os
import numpy as np

MODELS_DIR = 'saved models'

def test_model(name, input_size):
    path = os.path.join(MODELS_DIR, name)
    try:
        with open(path, 'rb') as f:
            model = pickle.load(f)
            dummy_input = np.zeros((1, input_size))
            pred = model.predict(dummy_input)
            prob = model.predict_proba(dummy_input) if hasattr(model, 'predict_proba') else 'N/A'
            print(f"{name}: Success. Pred={pred}, Prob={prob}")
    except Exception as e:
        print(f"{name}: Failed with {e}")

test_model('diabetes_model.sav', 8)
test_model('heart_disease_model.sav', 13)
test_model('parkinsons_model.sav', 22)
