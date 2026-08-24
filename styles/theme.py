import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Theme Colors
THEME = {
    "bg_dark": "#090d16",
    "bg_card": "rgba(17, 24, 39, 0.65)",
    "border_glass": "rgba(255, 255, 255, 0.08)",
    "accent_indigo": "#6366f1",
    "accent_cyan": "#06b6d4",
    "accent_violet": "#8b5cf6",
    "accent_fuchsia": "#d946ef",
    "accent_emerald": "#10b981",
    "accent_amber": "#f59e0b",
    "accent_rose": "#f43f5e",
    "text_primary": "#f8fafc",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
}

def inject_custom_css():
    """Injects the liquid glass design system CSS into the Streamlit app."""
    css_path = os.path.join(os.path.dirname(__file__), "liquid_glass.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <style>
            .stApp { background-color: #090d16; color: #f8fafc; }
            </style>
            """,
            unsafe_allow_html=True,
        )

def apply_plotly_theme(fig: go.Figure) -> go.Figure:
    """Applies modern obsidian glass aesthetics to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(17, 24, 39, 0.0)",
        plot_bgcolor="rgba(17, 24, 39, 0.35)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc", size=12),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94a3b8"),
            title_font=dict(color="#f8fafc", size=13),
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94a3b8"),
            title_font=dict(color="#f8fafc", size=13),
        ),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.65)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            borderwidth=1,
            font=dict(color="#f8fafc"),
        ),
    )
    return fig
