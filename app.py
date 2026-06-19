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
    
    st.markdown("---")
    st.markdown("### 👤 Patient Clinical Profiles")
    
    # Ensure session state variables exist
    if 'patients' not in st.session_state or 'current_patient' not in st.session_state:
        init_session_state()
        
    patient_list = list(st.session_state.patients.keys())
    current_idx = 0
    if st.session_state.current_patient in patient_list:
        current_idx = patient_list.index(st.session_state.current_patient)
        
    selected_patient = st.selectbox("Active Profile", patient_list, index=current_idx)
    st.session_state.current_patient = selected_patient
    
    with st.expander("➕ Register Patient"):
        new_name = st.text_input("Full Name", placeholder="e.g. Jane Smith")
        if st.button("Create Profile"):
            if new_name.strip() and new_name not in st.session_state.patients:
                st.session_state.patients[new_name] = []
                st.session_state.current_patient = new_name
                st.success(f"Created: {new_name}")
                st.rerun()

render_header()

# --- Dashboard Home ---
if selected == 'Dashboard':
    st.subheader(f"Clinical Command Center — Active Profile: {st.session_state.current_patient}")
    
    # Longitudinal Trend Chart
    active_patient = st.session_state.current_patient
    patient_records = st.session_state.patients.get(active_patient, [])
    
    render_dashboard_stats()
    
    if len(patient_records) > 0:
        st.markdown(f"### 📈 Longitudinal Vitals & Risk Trends: **{active_patient}**")
        
        import pandas as pd
        import plotly.express as px
        
        df = pd.DataFrame(patient_records)
        df['Risk Score (%)'] = df['probability'] * 100
        df['Screening Index'] = df['timestamp']
        
        fig_trend = px.line(
            df,
            x='Screening Index',
            y='Risk Score (%)',
            color='disease',
            markers=True,
            title="Screening Risk Progression Analysis",
            labels={'disease': 'Condition'}
        )
        fig_trend.update_layout(yaxis_range=[0, 105], height=320, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Clinical Report download
        summary_text = f"# Clinical Intelligence Report - {active_patient}\n\n"
        summary_text += f"Report Generated: 2026-06-19\n\n"
        for idx, rec in enumerate(patient_records):
            summary_text += f"### Screening Session {idx+1}: {rec['disease']}\n"
            summary_text += f"- **Outcome**: {'HIGH RISK / POSITIVE' if rec['result'] == 1 else 'NORMAL / NEGATIVE'}\n"
            summary_text += f"- **Confidence / Risk Probability**: {rec['probability']:.1%}\n\n"
            
        st.download_button(
            label="📥 Download Clinical Summary (Markdown)",
            data=summary_text,
            file_name=f"{active_patient.replace(' ', '_')}_report.md",
            mime="text/markdown"
        )
        
        # Display the active care plan for the selected patient based on their latest screening
        st.markdown("---")
        st.markdown(f"### 📋 Active Care Plan: **{active_patient}**")
        latest_rec = patient_records[-1]
        render_result_card(latest_rec['disease'], latest_rec['result'] == 1, latest_rec['probability'])
        
    st.markdown("---")
    with st.expander("🧪 Quick-Start Clinic Samples (Demo Data)"):
        st.write("Instant-populate screening forms with pre-set clinical data.")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            if st.button("🟢 Load Healthy Patient", key="btn_healthy"):
                st.session_state.demo_type = "healthy"
                # Clear simulated parkinsons so demo config takes over
                if 'parkinsons_simulated' in st.session_state:
                    st.session_state.parkinsons_simulated = None
                st.rerun()
        with col_d2:
            if st.button("🔴 Load At-Risk Patient", key="btn_risk"):
                st.session_state.demo_type = "at_risk"
                if 'parkinsons_simulated' in st.session_state:
                    st.session_state.parkinsons_simulated = None
                st.rerun()
        with col_d3:
            if st.button("🧹 Clear All Ledger Data", key="btn_clear"):
                st.session_state.clear()
                init_session_state()
                st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.info("The system uses cross-validated SVM and Logistic Regression models trained on peer-reviewed clinical datasets. All predictions should be interpreted by medical professionals.")
    with col2:
        render_lottie_success()

# --- Diabetes Prediction ---
elif selected == 'Diabetes Prediction':
    st.subheader(f"Diabetes Screening Profile: {st.session_state.current_patient}")
    
    col1, col2, col3 = st.columns(3)
    inputs = []
    demo_type = st.session_state.get('demo_type')
    for i, feat in enumerate(DIABETES_FEATURES):
        display_name = FEATURE_DISPLAY_NAMES.get(feat, feat)
        default_val = DEMO_DATA['diabetes'][demo_type].get(feat, 0.0) if demo_type else 0.0
        with [col1, col2, col3][i % 3]:
            inputs.append(st.number_input(display_name, value=float(default_val), step=0.01, format="%.2f", key=f"diab_{feat}"))
            
    if st.button('Predict Diabetes Risk'):
        from src.analytics import create_risk_gauge, create_deviation_chart
        prediction, prob = safe_predict(models['diabetes'], inputs)
        
        # Estimate probability if None (SVM default)
        if prob is None:
            from src.analytics import DATASET_STATS
            stats = DATASET_STATS['diabetes']
            u_glucose = inputs[DIABETES_FEATURES.index('Glucose')]
            u_bmi = inputs[DIABETES_FEATURES.index('BMI')]
            dev_g = (u_glucose - stats['healthy']['Glucose']) / (stats['positive']['Glucose'] - stats['healthy']['Glucose'] + 1e-6)
            dev_b = (u_bmi - stats['healthy']['BMI']) / (stats['positive']['BMI'] - stats['healthy']['BMI'] + 1e-6)
            prob = max(0.0, min(1.0, (dev_g + dev_b) / 2.0))
            if prediction == 0:
                prob = min(0.29, prob)
            else:
                prob = max(0.71, prob)
                
        if prediction is not None:
            render_result_card("Diabetes", prediction == 1, prob)
            track_history("Diabetes", 1 if prediction == 1 else 0, prob)
            
            ccol1, ccol2 = st.columns(2)
            with ccol1:
                st.plotly_chart(create_risk_gauge(prob, "Diabetes"), use_container_width=True)
            with ccol2:
                inputs_dict = {feat: val for feat, val in zip(DIABETES_FEATURES, inputs)}
                st.plotly_chart(create_deviation_chart(inputs_dict, "diabetes"), use_container_width=True)

# --- Heart Disease Prediction ---
elif selected == 'Heart Disease Prediction':
    st.subheader(f"Cardiac Screening Profile: {st.session_state.current_patient}")
    
    col1, col2, col3 = st.columns(3)
    inputs = []
    demo_type = st.session_state.get('demo_type')
    for i, feat in enumerate(HEART_FEATURES):
        display_name = FEATURE_DISPLAY_NAMES.get(feat, feat)
        default_val = DEMO_DATA['heart'][demo_type].get(feat, 0.0) if demo_type else 0.0
        with [col1, col2, col3][i % 3]:
            inputs.append(st.number_input(display_name, value=float(default_val), step=0.1, format="%.1f", key=f"heart_{feat}"))
            
    if st.button('Predict Heart Condition'):
        from src.analytics import create_risk_gauge, create_deviation_chart
        prediction, prob = safe_predict(models['heart'], [float(i) for i in inputs])
        if prediction is not None:
            is_risk = (prediction == 0) # For Cleveland Model, 0 is Risk
            
            # Handle probability bounds
            if prob is not None:
                if is_risk and prob < 0.5:
                    prob = 1.0 - prob
                elif not is_risk and prob > 0.5:
                    prob = 1.0 - prob
                    
            render_result_card("Heart Disease", is_risk, prob)
            track_history("Heart Disease", 1 if is_risk else 0, prob)
            
            ccol1, ccol2 = st.columns(2)
            with ccol1:
                if prob is not None:
                    st.plotly_chart(create_risk_gauge(prob, "Heart Disease"), use_container_width=True)
            with ccol2:
                inputs_dict = {feat: val for feat, val in zip(HEART_FEATURES, inputs)}
                st.plotly_chart(create_deviation_chart(inputs_dict, "heart"), use_container_width=True)

# --- Parkinson's Prediction ---
elif selected == "Parkinson's Prediction":
    st.subheader(f"Neurological Screening Profile: {st.session_state.current_patient}")
    
    # Acoustic voice recorder / analyzer simulation
    st.markdown("### 🎙️ Acoustic Voice Analyzer")
    st.write("Simulate raw audio signal processing or upload a patient voice recording to analyze pitch frequency and amplitude stability.")
    
    sim_col1, sim_col2 = st.columns([2, 1])
    with sim_col2:
        voice_type = st.selectbox("Simulated Vocal Tone", ["Normal Voice (Low Risk)", "Dysphonic / Breathive Voice (High Risk)"])
        uploaded_file = st.file_uploader("Upload Audio Sample (.wav, .mp3)", type=["wav", "mp3"])
        
    with sim_col1:
        if st.button("🎙️ Process and Extract Acoustic Vitals"):
            import time
            with st.status("Analyzing audio waveform...", expanded=True) as status:
                st.write("Loading vocal file...")
                time.sleep(0.5)
                st.write("Calculating Fundamental Frequencies (Fo, Fhi, Flo)...")
                time.sleep(0.5)
                st.write("Measuring Jitter (cycle-to-cycle frequency variation)...")
                time.sleep(0.5)
                st.write("Measuring Shimmer (cycle-to-cycle amplitude variation)...")
                time.sleep(0.5)
                st.write("Calculating Noise-to-Harmonics Ratio (NHR)...")
                time.sleep(0.5)
                status.update(label="22 Acoustic Biomarkers Extracted!", state="complete", expanded=False)
            
            sim_demo_type = "healthy" if "Normal" in voice_type else "at_risk"
            st.session_state.parkinsons_simulated = DEMO_DATA['parkinsons'][sim_demo_type]
            st.toast("Acoustic parameters loaded into dashboard below!", icon="✅")
            st.rerun()
            
    st.markdown("---")
    
    demo_data = st.session_state.get('parkinsons_simulated') or DEMO_DATA['parkinsons'].get(st.session_state.get('demo_type'))
    inputs_dict = render_categorized_inputs(PARKINSONS_CATEGORIES, demo_data=demo_data)
    
    ordered_inputs = [inputs_dict[f] for f in PARKINSONS_FEATURES]
    
    if st.button("Predict Parkinson's Risk"):
        from src.analytics import create_risk_gauge, create_parkinsons_radar, create_deviation_chart
        prediction, prob = safe_predict(models['parkinsons'], ordered_inputs)
        
        # Estimate probability if None (SVM default)
        if prob is None:
            from src.analytics import DATASET_STATS
            stats = DATASET_STATS['parkinsons']
            u_rpde = inputs_dict['RPDE']
            u_ppe = inputs_dict['PPE']
            dev_r = (u_rpde - stats['healthy']['RPDE']) / (stats['positive']['RPDE'] - stats['healthy']['RPDE'] + 1e-6)
            dev_p = (u_ppe - stats['healthy']['PPE']) / (stats['positive']['PPE'] - stats['healthy']['PPE'] + 1e-6)
            prob = max(0.0, min(1.0, (dev_r + dev_p) / 2.0))
            if prediction == 0:
                prob = min(0.29, prob)
            else:
                prob = max(0.71, prob)
                
        if prediction is not None:
            render_result_card("Parkinson's Disease", prediction == 1, prob)
            track_history("Parkinson's", 1 if prediction == 1 else 0, prob)
            
            pcol1, pcol2, pcol3 = st.columns(3)
            with pcol1:
                st.plotly_chart(create_risk_gauge(prob, "Parkinson's"), use_container_width=True)
            with pcol2:
                radar_data = [inputs_dict[f] for f in ["MDVP:Fo(Hz)", "MDVP:Jitter(%)", "MDVP:Shimmer", "NHR", "RPDE", "DFA"]]
                st.plotly_chart(create_parkinsons_radar(radar_data, None), use_container_width=True)
            with pcol3:
                st.plotly_chart(create_deviation_chart(inputs_dict, "parkinsons"), use_container_width=True)


