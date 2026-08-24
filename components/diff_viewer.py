import textwrap
import streamlit as st
import plotly.graph_objects as go
from styles.theme import apply_plotly_theme

def render_version_diff_radar(v1_weights: dict, v2_weights: dict, v1_label: str = "v1.0", v2_label: str = "v2.0") -> go.Figure:
    """Renders an overlapping dual radar chart highlighting parameter drift between versions."""
    categories = [
        "Price Sensitivity",
        "Brand Loyalty",
        "Tech Adoption",
        "Risk Tolerance",
        "Skepticism"
    ]
    
    v1_vals = [v1_weights.get(k.lower().replace(" ", "_"), 0.5) * 10 for k in categories]
    v2_vals = [v2_weights.get(k.lower().replace(" ", "_"), 0.5) * 10 for k in categories]
    
    cat_closed = categories + [categories[0]]
    v1_closed = v1_vals + [v1_vals[0]]
    v2_closed = v2_vals + [v2_vals[0]]
    
    fig = go.Figure()
    
    # Version 1 Trace
    fig.add_trace(go.Scatterpolar(
        r=v1_closed,
        theta=cat_closed,
        fill='toself',
        fillcolor='rgba(148, 163, 184, 0.2)',
        line=dict(color='#94a3b8', width=2, dash='dash'),
        name=f"Baseline ({v1_label})"
    ))
    
    # Version 2 Trace
    fig.add_trace(go.Scatterpolar(
        r=v2_closed,
        theta=cat_closed,
        fill='toself',
        fillcolor='rgba(6, 182, 212, 0.35)',
        line=dict(color='#06b6d4', width=2.5),
        name=f"Recalibrated ({v2_label})"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255, 255, 255, 0.1)"),
            angularaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)", tickfont=dict(color="#f8fafc", size=10)),
            bgcolor="rgba(17, 24, 39, 0.2)"
        ),
        margin=dict(l=30, r=30, t=30, b=30),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return apply_plotly_theme(fig)

def render_diff_table(v1_profile: dict, v2_profile: dict):
    """Renders a side-by-side comparison table of attributes."""
    v1_w = v1_profile.get("behavioral_weights", {})
    v2_w = v2_profile.get("behavioral_weights", {})
    
    keys = ["price_sensitivity", "brand_loyalty", "tech_adoption", "risk_tolerance", "skepticism"]
    
    rows_html = ""
    for k in keys:
        v1_val = v1_w.get(k, 0.5)
        v2_val = v2_w.get(k, 0.5)
        delta = v2_val - v1_val
        delta_str = f"+{delta*10:.1f}" if delta > 0 else (f"{delta*10:.1f}" if delta < 0 else "No Change")
        delta_color = "#10b981" if delta > 0 else ("#f43f5e" if delta < 0 else "#94a3b8")
        
        rows_html += f"""
        <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.06);">
            <td style="padding: 0.6rem 0.75rem; color: #f8fafc; font-weight: 600;">{k.replace('_', ' ').title()}</td>
            <td style="padding: 0.6rem 0.75rem; color: #94a3b8;">{v1_val*10:.1f} / 10</td>
            <td style="padding: 0.6rem 0.75rem; color: #67e8f9; font-weight: 700;">{v2_val*10:.1f} / 10</td>
            <td style="padding: 0.6rem 0.75rem; color: {delta_color}; font-weight: 700;">{delta_str}</td>
        </tr>
        """
        
    html = textwrap.dedent(f"""
    <div class="glass-container" style="padding: 0.75rem;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.12); color: #94a3b8; text-transform: uppercase; font-size: 0.75rem; text-align: left;">
                    <th style="padding: 0.5rem 0.75rem;">Parameter</th>
                    <th style="padding: 0.5rem 0.75rem;">Baseline ({v1_profile.get('version', 'v1.0')})</th>
                    <th style="padding: 0.5rem 0.75rem;">New ({v2_profile.get('version', 'v2.0')})</th>
                    <th style="padding: 0.5rem 0.75rem;">Net Drift</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

