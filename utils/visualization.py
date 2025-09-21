# utils/visualization.py
import plotly.graph_objects as go

def create_gauge_chart(score):
    """Create a gauge chart for the relevance score."""

   """Create score visualization"""
    try:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Relevance Score"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
                'threshold': {'line': {'color': "red", 'width': 4},
                             'thickness': 0.75, 'value': 90}
            }
        ))
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        return None
"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Relevance Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(width=400, height=300)
    return fig
