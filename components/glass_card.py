import textwrap
import streamlit as st

def glass_card_start(title: str = None, subtitle: str = None, badge_text: str = None, badge_type: str = "indigo"):
    """Starts a frosted glass container with optional glowing title and badge."""
    badge_html = f'<span class="glass-badge badge-{badge_type}">{badge_text}</span>' if badge_text else ""
    header_html = ""
    if title:
        header_html = f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #f8fafc;">{title}</h3>
                {f'<p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #94a3b8;">{subtitle}</p>' if subtitle else ''}
            </div>
            {badge_html}
        </div>
        """
    return textwrap.dedent(f"""
    <div class="glass-container">
        <div class="glass-header-glow"></div>
        {header_html}
    """).strip()

def glass_card_end():
    return "</div>"

def render_glass_card(title: str, content_html: str, subtitle: str = None, badge_text: str = None, badge_type: str = "indigo"):
    """Renders a complete glass card from an HTML string."""
    html = f"""
    {glass_card_start(title, subtitle, badge_text, badge_type)}
    <div>{content_html}</div>
    {glass_card_end()}
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def render_metric_card(label: str, value: str, delta: str = None, delta_type: str = "positive"):
    """Renders an obsidian glass metric stat box."""
    delta_html = ""
    if delta:
        delta_symbol = "▲" if delta_type == "positive" else ("▼" if delta_type == "negative" else "●")
        delta_html = f'<div class="stat-delta {delta_type}"><span>{delta_symbol}</span> <span>{delta}</span></div>'
    
    html = f"""
    <div class="glass-stat-card">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def render_banner(title: str, description: str, icon: str = "✨", accent_color: str = "indigo"):
    """Renders a top hero banner with glowing glass gradient."""
    html = f"""
    <div class="glass-container" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(6, 182, 212, 0.08)); border-color: rgba(99, 102, 241, 0.3);">
        <div class="glass-header-glow"></div>
        <div style="display: flex; align-items: center; gap: 1.25rem;">
            <div style="font-size: 2.2rem; background: rgba(99, 102, 241, 0.2); width: 64px; height: 64px; border-radius: 16px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(99, 102, 241, 0.4);">
                {icon}
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800; background: linear-gradient(90deg, #ffffff, #c7d2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h2>
                <p style="margin: 0.35rem 0 0 0; color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">{description}</p>
            </div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

