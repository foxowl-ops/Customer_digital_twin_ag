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

_original_st_markdown = st.markdown

def _flatten_html(html: str) -> str:
    """Strips per-line leading whitespace from a multi-line HTML string.

    Every glass card / stat / chat-bubble block in this app is written as
    an f-string indented to match its surrounding Python code, often with
    blank lines left in for readability. Once a blank line appears inside
    an `unsafe_allow_html=True` block, Streamlit's Markdown renderer treats
    whatever follows as a *new* CommonMark block — and if that next line
    still carries 4+ spaces of leftover source indentation, it gets parsed
    as an indented code block and shown as literal text instead of being
    rendered as HTML. Since whitespace is not meaningful in HTML, it's
    always safe to strip it per line before handing the string to
    Streamlit.
    """
    return "\n".join(line.lstrip() for line in html.strip("\n").split("\n")).strip()

def _patched_markdown(body, *args, **kwargs):
    if kwargs.get("unsafe_allow_html") and isinstance(body, str):
        body = _flatten_html(body)
    return _original_st_markdown(body, *args, **kwargs)

st.markdown = _patched_markdown

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
