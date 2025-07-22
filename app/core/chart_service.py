# app/core/chart_service.py (Fixed Glassmorphism Dark Theme Version)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

def generate_chart(df: pd.DataFrame, question: str):
    """
    Generates an interactive Plotly chart spec as a JSON string.
    This version is styled for a dark, glassy, professional UI with proper error handling.
    """
    if df.empty or df.shape[0] <= 1 or df.shape[1] < 2:
        return None

    try:
        x_col, y_col = df.columns[0], df.columns[1]
        
        # Check if we have numeric data for visualization
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            # Try to find a numeric column
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if not numeric_cols:
                return None
            y_col = numeric_cols[0]

        # Limit data points for better performance
        if len(df) > 50:
            df = df.head(50)

        # Determine chart type based on data
        if len(df) <= 20 and df[x_col].dtype == 'object':
            # Bar chart for categorical data
            fig = px.bar(df, x=x_col, y=y_col, text_auto='.2s')
            fig.update_traces(
                marker_color='#22c55e',
                marker_line_color='#16a34a',
                marker_line_width=1,
                textposition='outside',
                textfont=dict(color='#ffffff', size=10)
            )
        else:
            # Line chart for continuous or time-series data
            fig = px.line(df, x=x_col, y=y_col, markers=True)
            fig.update_traces(
                line_color='#22c55e',
                marker_color='#22c55e',
                marker_size=6,
                line_width=3
            )

        # Apply dark glassmorphism theme
        fig.update_layout(
            title={
                'text': f"<b style='color: #22c55e;'>{question}</b>",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 16, 'color': '#ffffff'}
            },
            font=dict(color='#ffffff', family='Inter, sans-serif'),
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
            
            # X-axis styling
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255, 255, 255, 0.1)',
                showline=True,
                linewidth=1,
                linecolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='#ffffff', size=10),
                title_font=dict(color='#22c55e', size=12)
            ),
            
            # Y-axis styling
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255, 255, 255, 0.1)',
                showline=True,
                linewidth=1,
                linecolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='#ffffff', size=10),
                title_font=dict(color='#22c55e', size=12)
            ),
            
            # Layout styling
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            
            # Hover styling
            hoverlabel=dict(
                bgcolor='rgba(34, 197, 94, 0.9)',
                bordercolor='#22c55e',
                font_color='white'
            )
        )

        # Update hover template
        if 'bar' in str(type(fig.data[0])):
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
            )
        else:
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
            )

        return fig.to_json()

    except Exception as e:
        print(f"Plotly chart generation failed: {e}")
        return None


def create_sample_chart():
    """
    Creates a sample chart for testing purposes
    """
    sample_data = {
        'Product': ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones'],
        'Sales': [15000, 25000, 8000, 12000, 6000]
    }
    df = pd.DataFrame(sample_data)
    return generate_chart(df, "Top 5 Products by Sales")


def generate_trend_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    """
    Generates a trend/line chart specifically for time-series data
    """
    try:
        fig = px.line(df, x=x_col, y=y_col, markers=True)
        
        fig.update_traces(
            line=dict(color='#22c55e', width=3),
            marker=dict(color='#22c55e', size=8, line=dict(color='#16a34a', width=2))
        )
        
        fig.update_layout(
            title={
                'text': f"<b style='color: #22c55e;'>{title}</b>",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(color='#ffffff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='#ffffff')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='#ffffff')
            ),
            height=400
        )
        
        return fig.to_json()
    
    except Exception as e:
        print(f"Trend chart generation failed: {e}")
        return None


def generate_pie_chart(df: pd.DataFrame, labels_col: str, values_col: str, title: str):
    """
    Generates a pie chart for distribution data
    """
    try:
        fig = px.pie(df, names=labels_col, values=values_col)
        
        fig.update_traces(
            marker=dict(
                colors=['#22c55e', '#16a34a', '#15803d', '#166534', '#14532d'],
                line=dict(color='#000000', width=2)
            ),
            textfont=dict(color='#ffffff', size=12)
        )
        
        fig.update_layout(
            title={
                'text': f"<b style='color: #22c55e;'>{title}</b>",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(color='#ffffff'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=True,
            legend=dict(
                font=dict(color='#ffffff'),
                bgcolor='rgba(0,0,0,0.5)'
            )
        )
        
        return fig.to_json()
    
    except Exception as e:
        print(f"Pie chart generation failed: {e}")
        return None