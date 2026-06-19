import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'saved models')

# Model Filenames
DIABETES_MODEL_PATH = os.path.join(MODELS_DIR, 'diabetes_model.sav')
HEART_MODEL_PATH = os.path.join(MODELS_DIR, 'heart_disease_model.sav')
PARKINSONS_MODEL_PATH = os.path.join(MODELS_DIR, 'parkinsons_model.sav')

# Feature Definitions
DIABETES_FEATURES = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]

HEART_FEATURES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

# Parkinson's Feature Categorization
PARKINSONS_CATEGORIES = {
    "Vocal Fundamentals": ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)"],
    "Pitch Stability (Jitter)": ["MDVP:Jitter(%)", "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP"],
    "Amplitude Stability (Shimmer)": ["MDVP:Shimmer", "MDVP:Shimmer(dB)", "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA"],
    "Tonal Quality (Noise-to-Harmonics)": ["NHR", "HNR"],
    "Non-Linear Dynamics": ["RPDE", "DFA", "spread1", "spread2", "D2", "PPE"]
}

# Flattened list for model input
PARKINSONS_FEATURES = [f for cat in PARKINSONS_CATEGORIES.values() for f in cat]

# Clinical Demo Data (Healthy/At-Risk Profiles)
DEMO_DATA = {
    "diabetes": {
        "healthy": {"Pregnancies": 1, "Glucose": 95, "BloodPressure": 70, "SkinThickness": 20, "Insulin": 79, "BMI": 23.5, "DiabetesPedigreeFunction": 0.25, "Age": 25},
        "at_risk": {"Pregnancies": 6, "Glucose": 160, "BloodPressure": 90, "SkinThickness": 35, "Insulin": 150, "BMI": 38.2, "DiabetesPedigreeFunction": 0.85, "Age": 55}
    },
    "heart": {
        "healthy": {"age": 30.0, "sex": 1.0, "cp": 3.0, "trestbps": 120.0, "chol": 190.0, "fbs": 0.0, "restecg": 0.0, "thalach": 180.0, "exang": 0.0, "oldpeak": 0.0, "slope": 2.0, "ca": 0.0, "thal": 2.0},
        "at_risk": {"age": 65.0, "sex": 1.0, "cp": 0.0, "trestbps": 160.0, "chol": 290.0, "fbs": 1.0, "restecg": 2.0, "thalach": 90.0, "exang": 1.0, "oldpeak": 4.0, "slope": 0.0, "ca": 3.0, "thal": 3.0}
    },
    "parkinsons": {
        "healthy": {
            "MDVP:Fo(Hz)": 181.94, "MDVP:Fhi(Hz)": 223.64, "MDVP:Flo(Hz)": 145.21,
            "MDVP:Jitter(%)": 0.003, "MDVP:Jitter(Abs)": 0.00002, "MDVP:RAP": 0.001, "MDVP:PPQ": 0.002, "Jitter:DDP": 0.005,
            "MDVP:Shimmer": 0.017, "MDVP:Shimmer(dB)": 0.16, "Shimmer:APQ3": 0.009, "Shimmer:APQ5": 0.010, "MDVP:APQ": 0.013, "Shimmer:DDA": 0.028,
            "NHR": 0.011, "HNR": 24.68, "RPDE": 0.44, "DFA": 0.69, "spread1": -6.76, "spread2": 0.16, "D2": 2.15, "PPE": 0.12
        },
        "at_risk": {
            "MDVP:Fo(Hz)": 115.0, "MDVP:Fhi(Hz)": 130.0, "MDVP:Flo(Hz)": 85.0,
            "MDVP:Jitter(%)": 0.015, "MDVP:Jitter(Abs)": 0.0001, "MDVP:RAP": 0.01, "MDVP:PPQ": 0.011, "Jitter:DDP": 0.03,
            "MDVP:Shimmer": 0.08, "MDVP:Shimmer(dB)": 0.8, "Shimmer:APQ3": 0.04, "Shimmer:APQ5": 0.05, "MDVP:APQ": 0.07, "Shimmer:DDA": 0.12,
            "NHR": 0.07, "HNR": 12.0, "RPDE": 0.68, "DFA": 0.82, "spread1": -3.2, "spread2": 0.38, "D2": 3.5, "PPE": 0.45
        }
    }
}

# Clinical Recommendations for At-Risk Patients
CLINICAL_RECOMMENDATIONS = {
    "Diabetes": {
        "Eat": [
            "Leafy greens, spinach, broccoli, kale.",
            "Whole grains (quinoa, brown rice, oats).",
            "Lean proteins (fish, chicken breast, tofu, beans)."
        ],
        "DoNotEat": [
            "Sugary beverages, sodas, sweetened juices.",
            "Refined carbs (white bread, white pasta, pastries).",
            "High-trans-fat fried foods and processed meats."
        ],
        "Do": [
            "Engage in 150 minutes of moderate aerobic activity per week.",
            "Perform strength training at least twice a week.",
            "Monitor blood sugar levels regularly before and after meals."
        ],
        "DoNotDo": [
            "Avoid sitting for prolonged periods; stand/stretch every hour.",
            "Do not skip meals or let your glucose drop excessively.",
            "Avoid strenuous workouts if your blood sugar is extremely high (>250 mg/dl)."
        ]
    },
    "Heart Disease": {
        "Eat": [
            "Mediterranean fats (olive oil, avocados, nuts, seeds).",
            "Omega-3 rich foods (salmon, mackerel, walnuts).",
            "High-fiber oats, barley, and colorful berries."
        ],
        "DoNotEat": [
            "Excessive table salt (sodium limit under 1,500mg/day).",
            "Saturated fats, butter, lard, heavy creams.",
            "Ultra-processed packaged snacks and high-cholesterol foods."
        ],
        "Do": [
            "Prioritize daily low-impact cardio like walking, swimming, or cycling.",
            "Monitor blood pressure and resting heart rate.",
            "Practice stress-relief methods (deep breathing, meditation)."
        ],
        "DoNotDo": [
            "Do not engage in sudden, high-intensity heavy weightlifting.",
            "Avoid tobacco, smoking, and heavy alcohol consumption.",
            "Do not ignore symptoms like chest tightness, jaw pain, or shortness of breath."
        ]
    },
    "Parkinson's": {
        "Eat": [
            "Antioxidant-rich foods (blueberries, dark chocolate, green tea).",
            "High-fiber foods to support gut motility and prevent constipation.",
            "Adequate fluids (at least 8 glasses of water daily)."
        ],
        "DoNotEat": [
            "Excessive protein right before taking Levodopa medication (interferes with absorption).",
            "Hard-to-chew dry foods that pose choking risks.",
            "Highly processed sugars that exacerbate fatigue."
        ],
        "Do": [
            "Focus on exercises improving balance, posture, and flexibility (Tai Chi, Yoga).",
            "Practice daily loud reading or singing to preserve vocal strength.",
            "Take big-stepping gait exercises to prevent freezing."
        ],
        "DoNotDo": [
            "Do not rush while walking or turn around quickly (prone to falls).",
            "Avoid walking in dark or cluttered rooms.",
            "Do not push through physical exhaustion; prioritize scheduled rests."
        ]
    }
}

# Wellness Maintenance for Healthy Patients
HEALTHY_RECOMMENDATIONS = {
    "Diabetes": {
        "Eat": [
            "A colorful variety of fresh vegetables.",
            "Whole fruits instead of processed juices.",
            "Legumes, nuts, and healthy complex carbs."
        ],
        "DoNotEat": [
            "Excessive sugary treats and desserts.",
            "Processed snack foods high in sodium and simple sugars.",
            "Sugary energy drinks and sweet mixers."
        ],
        "Do": [
            "Maintain at least 30 minutes of physical activity daily.",
            "Stay active throughout the day (take stairs, short walks).",
            "Track annual preventive metabolic checkups."
        ],
        "DoNotDo": [
            "Avoid skipping breakfast, which can throw off glucose stability.",
            "Do not lead a sedentary lifestyle; stand or stretch regularly."
        ]
    },
    "Heart Disease": {
        "Eat": [
            "Vibrant, leafy vegetables and colorful berries.",
            "Whole grains and lean poultry/fish.",
            "Heart-healthy nuts like almonds and walnuts."
        ],
        "DoNotEat": [
            "Processed deli meats with high preservatives/sodium.",
            "Excessive fast food and deep-fried dishes.",
            "Drinks containing high amounts of added sugars."
        ],
        "Do": [
            "Incorporate a mix of cardio and endurance exercises.",
            "Maintain a consistent sleep cycle (7-8 hours per night).",
            "Check cholesterol and blood pressure levels annually."
        ],
        "DoNotDo": [
            "Do not stay seated for hours without breaks.",
            "Avoid high chronic stress without pursuing coping techniques."
        ]
    },
    "Parkinson's": {
        "Eat": [
            "Diverse, nutrient-dense diet rich in vitamins.",
            "Healthy omega-3 fatty fats (avocados, walnuts).",
            "Adequate daily hydration (water, herbal teas)."
        ],
        "DoNotEat": [
            "Too much saturated fat and processed meats.",
            "Highly refined flour products."
        ],
        "Do": [
            "Challenge cognitive and motor skills (riddles, coordination sports).",
            "Engage in routine stretching to maintain range of motion.",
            "Stay socially connected and active in the community."
        ],
        "DoNotDo": [
            "Do not neglect fine motor practice (writing, drawing).",
            "Avoid a passive daily routine; stay intellectually stimulated."
        ]
    }
}

# Feature Display Names (Human-Readable)
FEATURE_DISPLAY_NAMES = {
    # Diabetes
    'Pregnancies': 'Total Pregnancies',
    'Glucose': 'Glucose Concentration',
    'BloodPressure': 'Diastolic Blood Pressure',
    'SkinThickness': 'Skin Fold Thickness (mm)',
    'Insulin': 'Serum Insulin (mu U/ml)',
    'BMI': 'Body Mass Index (BMI)',
    'DiabetesPedigreeFunction': 'Diabetes Genetic History',
    'Age': 'Age (Years)',
    
    # Heart
    'age': 'Patient Age',
    'sex': 'Gender (1=M, 0=F)',
    'cp': 'Chest Pain Type (0-3)',
    'trestbps': 'Resting Blood Pressure',
    'chol': 'Serum Cholesterol',
    'fbs': 'Fasting Blood Sugar (>120 mg/dl)',
    'restecg': 'Resting ECG Results',
    'thalach': 'Max Heart Rate Achieved',
    'exang': 'Exercise Induced Angina',
    'oldpeak': 'ST Depression (Slope)',
    'slope': 'ST Segment Peak Slope',
    'ca': 'Number of Major Vessels',
    'thal': 'Thalassemia Type',
    
    # Parkinson's
    "MDVP:Fo(Hz)": "Avg. Vocal Frequency (Fo)",
    "MDVP:Fhi(Hz)": "Max. Vocal Frequency (Fhi)",
    "MDVP:Flo(Hz)": "Min. Vocal Frequency (Flo)",
    "MDVP:Jitter(%)": "Vocal Pitch Variation (%)",
    "MDVP:Jitter(Abs)": "Vocal Pitch Var. (Abs)",
    "MDVP:RAP": "Relative Amplitude Perturbation",
    "MDVP:PPQ": "Period Perturbation Quotient",
    "Jitter:DDP": "Average Pitch Jitter",
    "MDVP:Shimmer": "Vocal Amplitude Variation",
    "MDVP:Shimmer(dB)": "Amplitude Var. (dB)",
    "Shimmer:APQ3": "3-Point Amplitude Pert.",
    "Shimmer:APQ5": "5-Point Amplitude Pert.",
    "MDVP:APQ": "11-Point Amplitude Pert.",
    "Shimmer:DDA": "Avg. Amplitude Shimmer",
    "NHR": "Noise-to-Harmonics Ratio",
    "HNR": "Harmonics-to-Noise Ratio",
    "RPDE": "Recurrence Period Density",
    "DFA": "Detrended Fluctuation Analysis",
    "spread1": "Freq. Variation Spread (1)",
    "spread2": "Freq. Variation Spread (2)",
    "D2": "Correlation Dimension (D2)",
    "PPE": "Pitch Period Entropy"
}

# UI Constants
APP_TITLE = "OmniHealth AI: Clinical Intelligence Suite"
APP_THEME_COLOR = "#007BFF"  # Healthcare Blue
