import plotly.graph_objects as go
import json
import os
import streamlit as st
from .config import FEATURE_DISPLAY_NAMES

# Load pre-calculated stats
STATS_PATH = os.path.join(os.path.dirname(__file__), 'dataset_stats.json')
with open(STATS_PATH, 'r') as f:
    DATASET_STATS = json.load(f)

def create_risk_gauge(probability, disease_name):
    """Creates a premium Plotly Gauge chart for risk percentage."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{disease_name} Risk Profile (%)", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#007BFF"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#28a745'},
                {'range': [30, 70], 'color': '#ffc107'},
                {'range': [70, 100], 'color': '#dc3545'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_parkinsons_radar(user_data, features):
    """Creates a radar chart comparing user samples to healthy/positive averages."""
    # Normalize features for radar chart display (0-1 range based on dataset means)
    stats = DATASET_STATS['parkinsons']
    
    # We'll use a subset of features for readability in a radar chart
    display_features = ["MDVP:Fo(Hz)", "MDVP:Jitter(%)", "MDVP:Shimmer", "NHR", "RPDE", "DFA"]
    labels = [FEATURE_DISPLAY_NAMES.get(f, f) for f in display_features]
    
    def get_values(source):
        return [source.get(f, 0) for f in display_features]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=get_values(stats['healthy']),
        theta=labels,
        fill='toself',
        name='Averge Healthy',
        line_color='#28a745'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=get_values(stats['positive']),
        theta=labels,
        fill='toself',
        name='Average Parkinson\'s',
        line_color='#dc3545'
    ))

    fig.add_trace(go.Scatterpolar(
        r=user_data, 
        theta=labels,
        fill='toself',
        name='User Input',
        line_color='#007BFF'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(get_values(stats['positive'])) * 1.5])
        ),
        showlegend=True,
        title="Comparative Acoustic Signature"
    )
    return fig

def create_deviation_chart(user_inputs, disease_key):
    """
    Creates a Plotly horizontal bar chart showing how much the patient's inputs
    deviate from healthy levels toward the high-risk averages.
    """
    stats = DATASET_STATS.get(disease_key.lower())
    if not stats:
        return None
        
    healthy = stats['healthy']
    positive = stats['positive']
    
    deviations = []
    
    for key, val in user_inputs.items():
        if key in healthy and key in positive:
            h_val = healthy[key]
            p_val = positive[key]
            diff = p_val - h_val
            if abs(diff) > 1e-6:
                # Percentage deviation from healthy toward positive
                dev = (val - h_val) / diff * 100
                deviations.append({
                    "feature": FEATURE_DISPLAY_NAMES.get(key, key),
                    "deviation": dev,
                    "val": val,
                    "healthy_avg": h_val,
                    "risk_avg": p_val
                })
                
    # Sort by deviation descending (showing largest risk contributors first)
    deviations = sorted(deviations, key=lambda x: x['deviation'], reverse=True)[:6]
    
    if not deviations:
        return None
        
    features = [d['feature'] for d in deviations]
    values = [d['deviation'] for d in deviations]
    hover_texts = [
        f"Value: {d['val']:.3f}<br>Healthy Avg: {d['healthy_avg']:.3f}<br>At-Risk Avg: {d['risk_avg']:.3f}"
        for d in deviations
    ]
    
    colors = ['#dc3545' if v > 50 else '#ffc107' if v > 20 else '#28a745' for v in values]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation='h',
        marker_color=colors,
        text=[f"{v:.1f}%" for v in values],
        textposition='auto',
        hoverinfo='text',
        hovertext=hover_texts
    ))
    
    fig.update_layout(
        title={
            'text': "Key Biomarker Deviation Analysis",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Deviation from Healthy toward High-Risk (%)",
        yaxis=dict(autorange="reversed"),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig



