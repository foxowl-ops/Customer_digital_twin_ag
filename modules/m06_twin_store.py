import streamlit as st
from components.glass_card import render_banner, render_metric_card
from components.twin_card import render_twin_profile_card

def render_stage_06():
    """Stage 06: Twin Profile Store."""
    render_banner(
        title="Stage 06: Digital Twin Profile Store",
        description="Core behavioral repository maintaining structured generative twin profiles, psychographic postures, behavioral weight matrices, and version tags across the customer base.",
        icon="👥",
        accent_color="cyan"
    )
    
    twin_store = st.session_state.twin_store
    df = st.session_state.customers_df
    
    # Summary Metrics
    distinct_twins = len([k for k in twin_store.keys() if k.startswith("TWIN-")])
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Active Twin Profiles", f"{distinct_twins}", "Compiled & Live", "positive")
    with m2:
        render_metric_card("Active Twin Version", "v1.0 Baseline", "Current Registry", "neutral")
    with m3:
        render_metric_card("Psychographic Dimensions", "5 Attributes", "Calibrated Vectors", "positive")
    with m4:
        render_metric_card("Profile Integrity", "100% Verified", "Ground Truth Grounded", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Twin Selector
    twin_keys = [k for k in twin_store.keys() if k.startswith("TWIN-")]
    
    col_sel1, col_sel2 = st.columns([1.5, 1])
    with col_sel1:
        selected_twin_id = st.selectbox(
            "Select Digital Twin to Inspect",
            twin_keys,
            format_func=lambda tid: f"{twin_store[tid]['avatar_emoji']} {twin_store[tid]['persona_name']} ({tid})"
        )
    with col_sel2:
        seg_filter = st.selectbox("Filter by Segment Archetype", ["All"] + list(df["segment_name"].unique()))
        
    selected_twin = twin_store[selected_twin_id]
    
    # Render Profile Inspector Card
    render_twin_profile_card(selected_twin)
    
    # Deep dive tabs: Psychographics, System Prompt Blueprint, Version History
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    tab_psy, tab_prompt, tab_history = st.tabs(["🧠 Psychographic Posture & Drivers", "📜 Compiled System Prompt Blueprint", "🏷️ Version Registry"])
    
    with tab_psy:
        psy = selected_twin.get("psychographics", {})
        voice = selected_twin.get("communication_voice", {})
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f"""
                <div class="glass-container" style="padding: 1.1rem;">
                    <h5 style="margin: 0 0 0.5rem 0; color: #67e8f9; font-size: 0.95rem;">🎯 Financial Goals & Priorities</h5>
                    <ul style="margin: 0 0 1rem 0; padding-left: 1.2rem; color: #e2e8f0; font-size: 0.85rem; line-height: 1.6;">
                        {"".join([f'<li>{g}</li>' for g in psy.get('financial_goals', [])])}
                    </ul>
                    
                    <h5 style="margin: 0 0 0.5rem 0; color: #fda4af; font-size: 0.95rem;">⛔ Critical Dealbreakers</h5>
                    <ul style="margin: 0; padding-left: 1.2rem; color: #e2e8f0; font-size: 0.85rem; line-height: 1.6;">
                        {"".join([f'<li>{d}</li>' for d in psy.get('dealbreakers', [])])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f"""
                <div class="glass-container" style="padding: 1.1rem;">
                    <h5 style="margin: 0 0 0.5rem 0; color: #a5b4fc; font-size: 0.95rem;">🗣️ Communication Tone & Style</h5>
                    <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 1rem;">{voice.get('tone')}</p>
                    
                    <h5 style="margin: 0 0 0.5rem 0; color: #6ee7b7; font-size: 0.95rem;">📱 Preferred Engagement Channel</h5>
                    <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">{voice.get('preferred_channel')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with tab_prompt:
        st.markdown(
            f"""
            <div class="glass-container" style="background: rgba(10, 15, 26, 0.75);">
                <div class="glass-header-glow"></div>
                <h5 style="margin: 0 0 0.5rem 0; color: #67e8f9; font-size: 0.95rem;">Active Generative Persona Prompt</h5>
                <pre style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; color: #a5b4fc; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; white-space: pre-wrap;">{selected_twin.get('system_prompt_blueprint')}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with tab_history:
        history = selected_twin.get("version_history", [])
        for h in history:
            st.markdown(
                f"""
                <div style="background: rgba(17, 24, 39, 0.6); border-left: 3px solid #06b6d4; padding: 0.75rem 1rem; border-radius: 0 8px 8px 0; margin-bottom: 0.6rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #67e8f9;">Version {h.get('version')}</strong>
                        <span style="color: #94a3b8; font-size: 0.8rem;">{h.get('timestamp')}</span>
                    </div>
                    <p style="margin: 0.35rem 0 0 0; color: #e2e8f0; font-size: 0.85rem;">{h.get('notes')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
