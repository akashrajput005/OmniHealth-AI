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


