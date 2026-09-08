import textwrap
import streamlit as st
import plotly.graph_objects as go
from styles.theme import apply_plotly_theme, get_chart_palette
from core.currency import format_inr

def render_twin_radar_chart(behavioral_weights: dict) -> go.Figure:
    """Generates a glass-styled radar chart for persona behavioral attributes."""
    categories = [
        "Price Sensitivity",
        "Brand Loyalty",
        "Tech Adoption",
        "Risk Tolerance",
        "Skepticism"
    ]
    
    values = [
        behavioral_weights.get("price_sensitivity", 0.5) * 10,
        behavioral_weights.get("brand_loyalty", 0.5) * 10,
        behavioral_weights.get("tech_adoption", 0.5) * 10,
        behavioral_weights.get("risk_tolerance", 0.5) * 10,
        behavioral_weights.get("skepticism", 0.5) * 10
    ]
    # Close the polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.35)',
        line=dict(color='#06b6d4', width=2),
        name='Persona Profile'
    ))
    
    _p = get_chart_palette()
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                gridcolor=_p["grid"],
                tickfont=dict(color=_p["tick"], size=9)
            ),
            angularaxis=dict(
                gridcolor=_p["grid"],
                tickfont=dict(color=_p["font"], size=11, family="Plus Jakarta Sans")
            ),
            bgcolor=_p["scene_bg"]
        ),
        margin=dict(l=30, r=30, t=25, b=25),
        height=280,
        showlegend=False
    )
    
    return apply_plotly_theme(fig)

def render_twin_profile_card(twin: dict):
    """Renders a comprehensive digital twin inspector card."""
    demo = twin.get("demographics", {})
    psy = twin.get("psychographics", {})
    weights = twin.get("behavioral_weights", {})
    
    col_l, col_r = st.columns([1.1, 1])
    
    with col_l:
        html = textwrap.dedent(f"""
        <div class="glass-container" style="margin-bottom: 0.5rem;">
            <div class="glass-header-glow"></div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 2.2rem; background: rgba(99, 102, 241, 0.2); width: 52px; height: 52px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        {twin.get('avatar_emoji', '👤')}
                    </span>
                    <div>
                        <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: var(--text-main);">{twin.get('customer_name')}</h3>
                        <span style="color: var(--text-muted); font-size: 0.85rem;">{twin.get('headline')}</span>
                    </div>
                </div>
                <span class="glass-badge badge-indigo">Twin {twin.get('version', 'v1.0')}</span>
            </div>
            
            <hr style="border: none; border-top: 1px solid rgba(var(--edge-rgb), 0.08); margin: 0.85rem 0;" />
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.65rem; font-size: 0.85rem;">
                <div><span style="color: var(--text-dim);">Segment:</span> <strong style="color: var(--accent-cyan-text);">{twin.get('segment_name')}</strong></div>
                <div><span style="color: var(--text-dim);">Decision Style:</span> <strong style="color: var(--text-main);">{psy.get('decision_style')}</strong></div>
                <div><span style="color: var(--text-dim);">Income / Insured Assets:</span> <strong style="color: var(--text-main);">{format_inr(demo.get('annual_income', 0))} / {format_inr(demo.get('insured_asset_value', 0))}</strong></div>
                <div><span style="color: var(--text-dim);">Credit / Insurance Score:</span> <strong style="color: #10b981;">{demo.get('credit_score')}</strong></div>
                <div><span style="color: var(--text-dim);">Claims Filed:</span> <strong style="color: var(--text-main);">{demo.get('num_claims_filed', 0)}</strong></div>
                <div><span style="color: var(--text-dim);">Last Claim Status:</span> <strong style="color: var(--text-main);">{demo.get('last_claim_status', 'No Claims Filed')}</strong></div>
            </div>
            
            <div style="margin-top: 0.85rem;">
                <span style="color: var(--text-dim); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;">Policies Held:</span>
                <div style="display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.35rem;">
                    {"".join([f'<span class="glass-badge badge-cyan" style="font-size: 0.75rem;">{h}</span>' for h in twin.get('holdings', [])])}
                </div>
            </div>
        </div>
        """).strip()
        st.markdown(html, unsafe_allow_html=True)
        
    with col_r:
        st.markdown('<span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); font-weight: 700;">Behavioral Calibration Radar</span>', unsafe_allow_html=True)
        fig = render_twin_radar_chart(weights)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
