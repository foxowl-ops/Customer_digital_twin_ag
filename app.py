import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Generative AI Digital Twin of a Customer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System & CSS Injection
from styles.theme import inject_custom_css
inject_custom_css()

# Central Session State Initialization
from core.state import init_session_state
init_session_state()

# Components & Navigation
from components.stepper import render_pipeline_stepper, STAGES
from modules.m01_ingestion import render_stage_01
from modules.m02_consent_pii import render_stage_02
from modules.m03_lakehouse import render_stage_03
from modules.m04_segmentation import render_stage_04
from modules.m05_theme_analysis import render_stage_05
from modules.m06_twin_store import render_stage_06
from modules.m07_knowledge_base import render_stage_07
from modules.m08_orchestration import render_stage_08
from modules.m09_focus_groups import render_stage_09
from modules.m10_competitor_sim import render_stage_10
from modules.m11_sales_roleplay import render_stage_11
from modules.m12_validation import render_stage_12
from modules.m13_recalibration import render_stage_13

# Sidebar Configuration
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="font-size: 2rem; background: rgba(99, 102, 241, 0.25); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(99, 102, 241, 0.4);">
                🧬
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800; color: #ffffff;">TwinEngine AI</h3>
                <span style="font-size: 0.75rem; color: #94a3b8;">Customer Digital Twin Platform</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 0.75rem 0;' />", unsafe_allow_html=True)
    
    # LLM Engine & API Configuration
    st.markdown("#### ⚡ Generative AI Engine")
    llm_service = st.session_state.llm_service
    
    current_xai_key = os.environ.get("XAI_API_KEY", "")
    api_key_input = st.text_input(
        "xAI Grok API Key",
        value=current_xai_key,
        type="password",
        help="xAI Grok API key for live grok-2 / grok-beta reasoning. If uncredited or empty, high-fidelity persona simulation is used."
    )
    
    if api_key_input:
        llm_service.update_key(api_key_input)
        
    if llm_service.is_live and llm_service.provider == "xAI Grok":
        engine_status = "🟢 xAI Grok (grok-2 / beta)"
    elif llm_service.is_live and llm_service.provider == "Anthropic Claude":
        engine_status = "🟢 Live Claude 3.5 Sonnet"
    else:
        engine_status = "🔵 High-Fidelity Simulation"
        
    st.markdown(f"<span style='font-size: 0.8rem; color: #94a3b8;'>Engine: <strong style='color: #67e8f9;'>{engine_status}</strong></span>", unsafe_allow_html=True)
    if llm_service.last_error and "permission-denied" in str(llm_service.last_error):
        st.markdown("<span style='font-size: 0.72rem; color: #f59e0b;'>Note: xAI key recognized. Ensure credits are added at console.x.ai for live tokens. Simulation engine active.</span>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 0.75rem 0;' />", unsafe_allow_html=True)
    
    # Direct Navigation
    st.markdown("#### 🧭 Pipeline Stages (1-13)")
    stage_titles = [f"{s['id']:02d}. {s['title']}" for s in STAGES]
    selected_stage_str = st.selectbox(
        "Navigate directly to stage",
        stage_titles,
        index=st.session_state.current_stage_idx
    )
    new_idx = stage_titles.index(selected_stage_str)
    if new_idx != st.session_state.current_stage_idx:
        st.session_state.current_stage_idx = new_idx
        st.rerun()
        
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 0.75rem 0;' />", unsafe_allow_html=True)
    
    # Quick Demo Presets
    st.markdown("#### 🚀 Quick Demo Presets")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("🗣️ Focus Group", use_container_width=True):
            st.session_state.current_stage_idx = 8 # Stage 9
            st.rerun()
    with col_p2:
        if st.button("🎯 Sales Pitch", use_container_width=True):
            st.session_state.current_stage_idx = 10 # Stage 11
            st.rerun()
            
    col_p3, col_p4 = st.columns(2)
    with col_p3:
        if st.button("📊 3D Clusters", use_container_width=True):
            st.session_state.current_stage_idx = 3 # Stage 4
            st.rerun()
    with col_p4:
        if st.button("🔄 Version Diff", use_container_width=True):
            st.session_state.current_stage_idx = 12 # Stage 13
            st.rerun()
            
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: rgba(17, 24, 39, 0.5); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; padding: 0.75rem; font-size: 0.75rem; color: #64748b;">
            <strong>TwinEngine Architecture v2.0</strong><br/>
            GDPR & CCPA Compliant • xAI Grok & Claude 3.5 • Obsidian Glass UI
        </div>
        """,
        unsafe_allow_html=True
    )

# Render Top Stepper & Get Active Stage
active_stage = render_pipeline_stepper()

# Stage View Routing Dispatcher
STAGE_ROUTERS = {
    "m01_ingestion": render_stage_01,
    "m02_consent_pii": render_stage_02,
    "m03_lakehouse": render_stage_03,
    "m04_segmentation": render_stage_04,
    "m05_theme_analysis": render_stage_05,
    "m06_twin_store": render_stage_06,
    "m07_knowledge_base": render_stage_07,
    "m08_orchestration": render_stage_08,
    "m09_focus_groups": render_stage_09,
    "m10_competitor_sim": render_stage_10,
    "m11_sales_roleplay": render_stage_11,
    "m12_validation": render_stage_12,
    "m13_recalibration": render_stage_13,
}

render_func = STAGE_ROUTERS.get(active_stage["module"])
if render_func:
    render_func()
else:
    st.error(f"Module {active_stage['module']} not found.")
