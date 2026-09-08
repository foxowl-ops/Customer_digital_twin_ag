import os
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

# Theme Colors (dark-mode reference palette; kept for backwards compatibility)
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

def inject_theme_attribute():
    """Stamps the active light/dark theme onto <html data-theme="..."> so
    liquid_glass.css's [data-theme="light"] rules can take over.

    Streamlit's own `<style>` injection (via st.markdown) can't set an
    attribute on an ancestor element it doesn't itself render, and a plain
    <script> tag inserted through unsafe_allow_html is inert (scripts
    added via innerHTML never execute in browsers). st.components.v1.html
    renders in a real iframe whose script *does* execute, and since that
    iframe is same-origin we can reach back into window.parent.document.
    """
    theme = st.session_state.get("theme", "dark")
    components.html(
        f"""
        <script>
            const doc = window.parent.document;
            doc.documentElement.setAttribute('data-theme', '{theme}');
        </script>
        """,
        height=0,
    )

def _current_theme() -> str:
    return st.session_state.get("theme", "dark")

def get_chart_palette() -> dict:
    """Returns the Plotly-facing color set for the active theme. Plotly
    renders its own SVG/canvas and has no notion of CSS custom properties,
    so unlike the HTML components, its colors have to be picked in Python."""
    if _current_theme() == "light":
        return {
            "grid": "rgba(15, 23, 42, 0.08)",
            "zeroline": "rgba(15, 23, 42, 0.16)",
            "font": "#0f172a",
            "tick": "#475569",
            "plot_bg": "rgba(255, 255, 255, 0.55)",
            "legend_bg": "rgba(255, 255, 255, 0.88)",
            "legend_border": "rgba(15, 23, 42, 0.1)",
            "scene_bg": "rgba(226, 232, 240, 0.55)",
        }
    return {
        "grid": "rgba(255, 255, 255, 0.06)",
        "zeroline": "rgba(255, 255, 255, 0.1)",
        "font": "#f8fafc",
        "tick": "#94a3b8",
        "plot_bg": "rgba(17, 24, 39, 0.35)",
        "legend_bg": "rgba(17, 24, 39, 0.65)",
        "legend_border": "rgba(255, 255, 255, 0.08)",
        "scene_bg": "rgba(17, 24, 39, 0.3)",
    }

def apply_plotly_theme(fig: go.Figure) -> go.Figure:
    """Applies theme-matched (light or dark) glass aesthetics to a Plotly figure."""
    p = get_chart_palette()
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0.0)",
        plot_bgcolor=p["plot_bg"],
        font=dict(family="Plus Jakarta Sans, sans-serif", color=p["font"], size=12),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor=p["grid"],
            zerolinecolor=p["zeroline"],
            tickfont=dict(color=p["tick"]),
            title_font=dict(color=p["font"], size=13),
        ),
        yaxis=dict(
            gridcolor=p["grid"],
            zerolinecolor=p["zeroline"],
            tickfont=dict(color=p["tick"]),
            title_font=dict(color=p["font"], size=13),
        ),
        legend=dict(
            bgcolor=p["legend_bg"],
            bordercolor=p["legend_border"],
            borderwidth=1,
            font=dict(color=p["font"]),
        ),
    )
    return fig
