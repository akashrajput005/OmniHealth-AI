import streamlit as st
from streamlit_lottie import st_lottie
import requests
from .config import APP_TITLE, APP_THEME_COLOR, FEATURE_DISPLAY_NAMES, CLINICAL_RECOMMENDATIONS, HEALTHY_RECOMMENDATIONS

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def init_session_state():
    """Initializes session state variables for history and demo mode."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'demo_type' not in st.session_state:
        st.session_state.demo_type = None

def track_history(disease, result, probability):
    """Safely updates session history with prediction results."""
    # Ensure history is initialized
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Store result
    st.session_state.history.append({
        "disease": disease,
        "result": int(result),
        "probability": float(probability) if probability is not None else None
    })

def inject_custom_styles():
    """Injects premium CSS for a medical dashboard look."""
    st.markdown(f"""
        <style>
        .main {{
            background-color: #f8f9fa;
        }}
        .stButton>button {{
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background-color: {APP_THEME_COLOR};
            color: white;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #0056b3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,123,255,0.3);
        }}
        .result-card {{
            border-radius: 15px;
            padding: 25px;
            background: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid {APP_THEME_COLOR};
            margin-top: 20px;
        }}
        .risk-high {{
            color: #dc3545;
            font-weight: bold;
        }}
        .risk-low {{
            color: #28a745;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """Renders the main application header."""
    st.title(f"🏥 {APP_TITLE}")
    st.markdown("---")

def render_result_card(title, is_positive, probability=None):
    """Renders a deeply-fixed, premium result dashboard for clinical outcomes."""
    status_text = "HIGH RISK / POSITIVE" if is_positive else "NORMAL / NEGATIVE"
    color = "#dc3545" if is_positive else "#28a745"
    bg_light = "#fff5f5" if is_positive else "#f6fff8"
    icon = "🚨" if is_positive else "✅"
    
    # Map title to recommendation keys
    rec_key = "Heart Disease" if "Heart" in title else "Parkinson's" if "Parkinson" in title else "Diabetes"
    at_risk_recs = CLINICAL_RECOMMENDATIONS.get(rec_key, {})
    healthy_recs = HEALTHY_RECOMMENDATIONS.get(rec_key, {})
    
    with st.container():
        st.markdown(f"""
            <div style="
                background-color: {bg_light};
                padding: 30px;
                border-radius: 20px;
                border: 2px solid {color};
                box-shadow: 0 10px 30px rgba(0,0,0,0.05);
                margin: 20px 0;
            ">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <h4 style="margin: 0; color: #666; text-transform: uppercase; letter-spacing: 1px;">Clinical Analysis: {title}</h4>
                        <h1 style="margin: 10px 0; color: {color}; font-size: 2.5rem;">{icon} {status_text}</h1>
                    </div>
                </div>
                <hr style="border: none; border-top: 1px solid rgba(0,0,0,0.1); margin: 20px 0;">
                <p style="font-size: 1.1rem; line-height: 1.6; color: #444;">
                    <b>Diagnostic Insight:</b> Based on the sophisticated ML analysis of your acoustic and clinical metrics, 
                    the system has detected a signature consistent with <b>{status_text}</b>.
                </p>
                <div style="
                    background: white; 
                    padding: 15px; 
                    border-radius: 12px; 
                    margin-top: 20px;
                    border-left: 5px solid {color};
                ">
                    <p style="margin: 0; font-size: 0.9rem; color: #555;">
                        <b>Recommendation:</b> {"Seek immediate consultation with a healthcare professional to discuss these findings and perform confirmatory diagnostic testing." if is_positive else "Maintain regular health checkups. This analysis is a screening tool and does not replace professional medical diagnosis."}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        recs = at_risk_recs if is_positive else healthy_recs
        expander_title = "📋 VIEW CLINICAL ACTION PLAN" if is_positive else "🌱 VIEW PREVENTIVE WELLNESS PLAN"
        
        if recs:
            with st.expander(expander_title, expanded=is_positive):
                rcol1, rcol2 = st.columns(2)
                with rcol1:
                    st.markdown("#### 🥗 Nutrition Guide")
                    for item in recs.get("Diet", []):
                        st.write(f"- {item}")
                with rcol2:
                    st.markdown("#### 🏃 Exercise Routine")
                    for item in recs.get("Exercise", []):
                        st.write(f"- {item}")

def render_categorized_inputs(categories, demo_data=None):
    """Helper to render inputs with human-readable names and high precision."""
    inputs = {}
    for cat_name, features in categories.items():
        with st.expander(cat_name, expanded=True):
            cols = st.columns(min(len(features), 3))
            for i, feat in enumerate(features):
                display_name = FEATURE_DISPLAY_NAMES.get(feat, feat)
                # Define precision: fundamental frequencies need 2, but jitter/shimmer need 5-6
                precision = 5 if any(x in feat for x in ["Jitter", "Shimmer", "NHR", "PPE", "RPDE", "spread"]) else 2
                
                # Use demo data if provided
                default_val = demo_data.get(feat, 0.0) if demo_data else 0.0
                
                with cols[i % 3]:
                    inputs[feat] = st.number_input(
                        display_name, 
                        value=float(default_val),
                        step=10**-precision, 
                        format=f"%.{precision}f",
                        key=f"inp_{feat}"
                    )
    return inputs

def render_dashboard_stats():
    """Renders high-level stats for the landing page."""
    st.markdown("### 📊 Clinical Overview")
    col1, col2, col3 = st.columns(3)
    
    history = st.session_state.get('history', [])
    total = len(history)
    high_risk = len([h for h in history if h['result'] == 1])
    
    with col1:
        st.metric("Total Screenings", total)
    with col2:
        st.metric("High-Risk Detections", high_risk, delta=f"{high_risk/(total if total > 0 else 1):.0%}", delta_color="inverse")
    with col3:
        # Dynamic Health Analytics Score (Negative / Total)
        score = ((total - high_risk) / total * 100) if total > 0 else 100.0
        status = "Optimal" if score > 80 else "Attention Required" if score > 50 else "Critical"
        st.metric("Health Analytics Score", f"{score:.1f}%", delta=status)

    st.markdown("---")
    if not history:
        st.info("No prediction history available yet. Start a screening from the sidebar!")
    else:
        st.markdown("#### Recent Activity")
        for entry in reversed(history[-3:]):
            prob_val = entry.get('probability')
            prob_str = f"({prob_val:.1%})" if prob_val is not None else ""
            st.write(f"🔍 {entry['disease']} - **{'Positive' if entry['result'] == 1 else 'Negative'}** {prob_str}")

def render_lottie_success():
    """Renders a medical-themed Lottie animation."""
    lottie_medical = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_5njpXm.json")
    if lottie_medical:
        st_lottie(lottie_medical, height=200, key="medical_anim")
