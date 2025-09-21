
import plotly.graph_objects as go

def create_score_gauge(score, color):
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
