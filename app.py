import streamlit as st
from streamlit_option_menu import option_menu

from src.config import (
    APP_TITLE, DIABETES_FEATURES, HEART_FEATURES, PARKINSONS_CATEGORIES, PARKINSONS_FEATURES,
    FEATURE_DISPLAY_NAMES, DEMO_DATA
)
from src.models import load_models, safe_predict
from src.ui_components import (
    inject_custom_styles, render_header, render_result_card, 
    render_categorized_inputs, render_dashboard_stats, render_lottie_success,
    init_session_state, track_history
)

# Page Configuration
st.set_page_config(page_title=APP_TITLE, page_icon="🏥", layout="wide")
inject_custom_styles()
init_session_state()

# Load Models
models = load_models()

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        APP_TITLE,
        ['Dashboard', 'Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"],
        icons=['grid', 'activity', 'heart', 'person'],
        default_index=0
    )
    

render_header()

# --- Dashboard Home ---
if selected == 'Dashboard':
    st.subheader("Welcome to the Clinical Command Center")
    render_dashboard_stats()
    
    st.markdown("### 🧪 Quick-Start Clinic Samples")
    st.write("Instant-populate screening forms with pre-set clinical data.")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        if st.button("🟢 Load Healthy Patient", key="btn_healthy"):
            st.session_state.demo_type = "healthy"
            st.rerun()
    with col_d2:
        if st.button("🔴 Load At-Risk Patient", key="btn_risk"):
            st.session_state.demo_type = "at_risk"
            st.rerun()
    with col_d3:
        if st.button("🧹 Clear All Data", key="btn_clear"):
            st.session_state.history = []
            st.session_state.demo_type = None
            st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.info("The system uses cross-validated SVM and Logistic Regression models trained on peer-reviewed clinical datasets. All predictions should be interpreted by medical professionals.")
    with col2:
        render_lottie_success()

# --- Diabetes Prediction ---
elif selected == 'Diabetes Prediction':
    st.subheader("Diabetes Screening")
    
    col1, col2, col3 = st.columns(3)
    inputs = []
    demo_type = st.session_state.get('demo_type')
    for i, feat in enumerate(DIABETES_FEATURES):
        display_name = FEATURE_DISPLAY_NAMES.get(feat, feat)
        default_val = DEMO_DATA['diabetes'][demo_type].get(feat, 0.0) if demo_type else 0.0
        with [col1, col2, col3][i % 3]:
            inputs.append(st.number_input(display_name, value=float(default_val), step=0.01, format="%.2f", key=f"diab_{feat}"))
            
    if st.button('Predict Diabetes Risk'):
        from src.analytics import create_risk_gauge
        prediction, prob = safe_predict(models['diabetes'], inputs)
        if prediction is not None:
            render_result_card("Diabetes", prediction == 1, prob)
            # Result 1 is At-Risk for Diabetes
            track_history("Diabetes", 1 if prediction == 1 else 0, prob)
            if prob is not None:
                st.plotly_chart(create_risk_gauge(prob, "Diabetes"), use_container_width=True)

# --- Heart Disease Prediction ---
elif selected == 'Heart Disease Prediction':
    st.subheader("Cardiac Screening")
    
    col1, col2, col3 = st.columns(3)
    inputs = []
    demo_type = st.session_state.get('demo_type')
    for i, feat in enumerate(HEART_FEATURES):
        display_name = FEATURE_DISPLAY_NAMES.get(feat, feat)
        default_val = DEMO_DATA['heart'][demo_type].get(feat, 0.0) if demo_type else 0.0
        with [col1, col2, col3][i % 3]:
            inputs.append(st.number_input(display_name, value=float(default_val), step=0.1, format="%.1f", key=f"heart_{feat}"))
            
    if st.button('Predict Heart Condition'):
        from src.analytics import create_risk_gauge
        prediction, prob = safe_predict(models['heart'], [float(i) for i in inputs])
        if prediction is not None:
            # For this Heart model, 0 is High Risk / Positive
            is_risk = (prediction == 0)
            render_result_card("Heart Disease", is_risk, prob)
            track_history("Heart Disease", 1 if is_risk else 0, prob)
            if prob is not None:
                st.plotly_chart(create_risk_gauge(prob, "Heart Disease"), use_container_width=True)

# --- Parkinson's Prediction ---
elif selected == "Parkinson's Prediction":
    st.subheader("Neurological Screening (Parkinson's)")
    
    demo_type = st.session_state.get('demo_type')
    parkinsons_demo = DEMO_DATA['parkinsons'][demo_type] if demo_type else None
    inputs_dict = render_categorized_inputs(PARKINSONS_CATEGORIES, demo_data=parkinsons_demo)
    
    # Flatten inputs in the correct order as defined in config
    ordered_inputs = [inputs_dict[f] for f in PARKINSONS_FEATURES]
    
    if st.button("Predict Parkinson's Risk"):
        from src.analytics import create_risk_gauge, create_parkinsons_radar
        prediction, prob = safe_predict(models['parkinsons'], ordered_inputs)
        if prediction is not None:
            render_result_card("Parkinson's Disease", prediction == 1, prob)
            # Result 1 is At-Risk for Parkinson's
            track_history("Parkinson's", 1 if prediction == 1 else 0, prob)
            
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                if prob is not None:
                    st.plotly_chart(create_risk_gauge(prob, "Parkinson's"), use_container_width=True)
            with pcol2:
                # Radar Chart for comparative analysis
                radar_data = [inputs_dict[f] for f in ["MDVP:Fo(Hz)", "MDVP:Jitter(%)", "MDVP:Shimmer", "NHR", "RPDE", "DFA"]]
                st.plotly_chart(create_parkinsons_radar(radar_data, None), use_container_width=True)
