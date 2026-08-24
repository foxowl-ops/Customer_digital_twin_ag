import streamlit as st

STAGES = [
    {"id": 1, "key": "ingestion", "title": "Data Ingestion", "icon": "📥", "module": "m01_ingestion"},
    {"id": 2, "key": "consent", "title": "Consent & PII", "icon": "🛡️", "module": "m02_consent_pii"},
    {"id": 3, "key": "lakehouse", "title": "CDP / Lakehouse", "icon": "🗄️", "module": "m03_lakehouse"},
    {"id": 4, "key": "segmentation", "title": "Segmentation", "icon": "📊", "module": "m04_segmentation"},
    {"id": 5, "key": "theme_analysis", "title": "Theme & Sentiment", "icon": "💬", "module": "m05_theme_analysis"},
    {"id": 6, "key": "twin_store", "title": "Twin Profile Store", "icon": "👥", "module": "m06_twin_store"},
    {"id": 7, "key": "knowledge_base", "title": "Evidence RAG", "icon": "🧠", "module": "m07_knowledge_base"},
    {"id": 8, "key": "orchestration", "title": "LLM Orchestration", "icon": "⚡", "module": "m08_orchestration"},
    {"id": 9, "key": "focus_groups", "title": "Focus Groups", "icon": "🗣️", "module": "m09_focus_groups"},
    {"id": 10, "key": "competitor_sim", "title": "Competitor Sims", "icon": "⚔️", "module": "m10_competitor_sim"},
    {"id": 11, "key": "sales_roleplay", "title": "Sales Roleplay", "icon": "🎯", "module": "m11_sales_roleplay"},
    {"id": 12, "key": "validation", "title": "Human Validation", "icon": "⚖️", "module": "m12_validation"},
    {"id": 13, "key": "recalibration", "title": "Recalibration", "icon": "🔄", "module": "m13_recalibration"},
]

def render_pipeline_stepper():
    """Renders the top interactive visual pipeline stepper with stage selection."""
    if "current_stage_idx" not in st.session_state:
        st.session_state.current_stage_idx = 0

    current_idx = st.session_state.current_stage_idx
    
    # Render quick stage navigator pill buttons
    st.markdown('<div style="margin-bottom: 0.5rem;"><span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; font-weight: 700;">Architecture Pipeline Stepper</span></div>', unsafe_allow_html=True)
    
    # We display a 13-stage scrollable bar or columns
    cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    for i, stage in enumerate(STAGES):
        with cols[i]:
            is_active = (i == current_idx)
            btn_type = "primary" if is_active else "secondary"
            btn_label = f"{stage['icon']} {stage['id']:02d}"
            if st.button(btn_label, key=f"stepper_btn_{i}", help=f"Stage {stage['id']}: {stage['title']}", use_container_width=True, type=btn_type):
                st.session_state.current_stage_idx = i
                st.rerun()

    # Active Stage Indicator Card
    active_stage = STAGES[current_idx]
    prev_disabled = (current_idx == 0)
    next_disabled = (current_idx == len(STAGES) - 1)
    
    nav_c1, nav_c2, nav_c3 = st.columns([1, 6, 1])
    with nav_c1:
        if st.button("◀ Prev Stage", disabled=prev_disabled, use_container_width=True):
            st.session_state.current_stage_idx -= 1
            st.rerun()
    with nav_c2:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 0.25rem 0;">
                <span class="glass-badge badge-cyan" style="font-size: 0.85rem; padding: 0.35rem 0.85rem;">
                    Stage {active_stage['id']:02d} of 13: <strong>{active_stage['title']}</strong>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with nav_c3:
        if st.button("Next Stage ▶", disabled=next_disabled, use_container_width=True):
            st.session_state.current_stage_idx += 1
            st.rerun()
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 0.85rem 0 1.25rem 0;' />", unsafe_allow_html=True)
    return active_stage
