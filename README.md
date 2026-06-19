# 🏥 OmniHealth AI: Clinical Intelligence Suite

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://omnihealth-ai-aawphkdjhm3bzgwfab3rnk.streamlit.app/)

**OmniHealth AI** is a next-generation clinical diagnostic platform designed to provide interactive, accurate, and high-fidelity disease prediction. Transform raw medical data into actionable clinical insights with our state-of-the-art diagnostic suite.

## 🚀 Key Features
- **🔬 Explainable AI (XAI)**: Visualizes the **Biomarker Risk Deviation Index** using horizontal Plotly bar charts, comparing patient measurements against clinical datasets' healthy and positive population averages.
- **🎙️ Acoustic Voice Analyzer Simulator**: Mock waveform processing and vocal feature extraction interface for Parkinson's screening (simulates extraction of Jitter, Shimmer, NHR, and Non-Linear Dynamics).
- **📋 Allowed/Avoid Patient Action Plans**: Detailed clinical guide tables mapping out exactly **What to Eat (Allowed)**, **Limit / Avoid (Do Not Eat)**, **Recommended Activity (Do)**, and **Precautions (Do Not Do)**.
- **📈 Longitudinal Patient Ledger**: Supports named patient profiles (e.g. pre-loaded profiles Aarav Sharma, Priya Patel, Amit Kumar) and tracks risk level trends across multiple screening sessions on line charts.
- **🏥 Clinical Command Center**: A centralized dashboard tracking session-based patient screening logs and overall health score metrics.
- **One-Click Clinical Hub**: Instantly load pre-verified "Healthy" or "At-Risk" profiles inside an interactive expander panel.
- **Premium Medical UX**: Sleek, modern interface with categorized inputs, Lottie animations, and custom styling.

## 🛠️ Technology Stack
- **Engine**: Python 3.12+
- **Frontend**: Streamlit (Advanced UI Customization)
- **Analytics**: Plotly (Radar, Gauges)
- **ML Models**: SVM, Logistic Regression 
- **Animations**: Streamlit-Lottie 

## 📦 Installation & Setup
1. **Clone the Suite**:
   ```bash
   git clone https://github.com/akashrajput005/OmniHealth-AI.git
   cd OmniHealth-AI
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch the Suite**:
   ```bash
   streamlit run app.py
   ```

## 🏥 Clinical Diagnostic Modules
### 🔗 Cardiac Screening (Heart Disease)
Uses clinical markers like chest pain type, major vessels, and ST segment analysis to predict cardiac risk with high precision.

### 🔗 Metabolic Screening (Diabetes)
Analyzes glucose concentration, genetic history, and metabolic factors to identify early-stage risk profiles.

### 🔗 Neurological Screening (Parkinson's)
Features a **Vocal Signature Analysis** hub that maps acoustic metrics (Jitter, Shimmer, HNR) to a comparative diagnostic radar.

---
*Developed for future-ready healthcare.*
