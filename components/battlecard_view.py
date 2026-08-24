import textwrap
import streamlit as st

def render_sales_battlecard(battlecard: dict):
    """Renders a high-impact sales battlecard for the targeted persona archetype."""
    html = textwrap.dedent(f"""
    <div class="glass-container" style="background: linear-gradient(145deg, rgba(17, 24, 39, 0.85), rgba(30, 41, 59, 0.75)); border-color: rgba(99, 102, 241, 0.35);">
        <div class="glass-header-glow"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <span class="glass-badge badge-amber" style="margin-bottom: 0.25rem;">Generated Sales Intelligence Battlecard</span>
                <h3 style="margin: 0.2rem 0 0 0; font-size: 1.3rem; font-weight: 800; color: #ffffff;">{battlecard.get('title', 'Sales Battlecard')}</h3>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Pitch Score</span>
                <div style="font-size: 1.8rem; font-weight: 800; color: #10b981;">{battlecard.get('score', 85)}/100</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #6ee7b7; font-size: 0.95rem; font-weight: 700;">✅ Winning Rebuttal Strategies</h4>
                <ul style="margin: 0; padding-left: 1.2rem; color: #e2e8f0; font-size: 0.85rem; line-height: 1.6;">
                    {"".join([f'<li>{s}</li>' for s in battlecard.get('winning_strategies', [])])}
                </ul>
            </div>
            
            <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 12px; padding: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #fda4af; font-size: 0.95rem; font-weight: 700;">❌ Fatal Pitfalls & Triggers</h4>
                <ul style="margin: 0; padding-left: 1.2rem; color: #e2e8f0; font-size: 0.85rem; line-height: 1.6;">
                    {"".join([f'<li>{f}</li>' for f in battlecard.get('fatal_pitfalls', [])])}
                </ul>
            </div>
        </div>
        
        <div style="background: rgba(17, 24, 39, 0.5); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 1rem;">
            <h4 style="margin: 0 0 0.35rem 0; color: #67e8f9; font-size: 0.9rem; font-weight: 700;">💡 Executive Coach's Tactical Note</h4>
            <p style="margin: 0; color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">{battlecard.get('coach_summary', 'Tailor pricing directly to asset tier.')}</p>
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

