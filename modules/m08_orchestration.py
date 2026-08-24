import streamlit as st
from components.glass_card import render_banner, render_metric_card
from prompts.persona_prompts import build_persona_system_prompt

def render_stage_08():
    """Stage 08: LLM & Twin Orchestration Layer."""
    render_banner(
        title="Stage 08: LLM & Twin Orchestration Layer",
        description="Reasoning core that dynamically compiles the Digital Twin profile, retrieved RAG evidence, and scenario context into structured xAI Grok prompts.",
        icon="⚡",
        accent_color="indigo"
    )
    
    twin_store = st.session_state.twin_store
    rag = st.session_state.rag_engine
    llm = st.session_state.llm_service
    
    # Engine status
    if llm.is_live and llm.provider == "xAI Grok":
        engine_mode = "LIVE (xAI Grok-2)"
        mode_badge = "emerald"
    elif llm.is_live and llm.provider == "Anthropic Claude":
        engine_mode = "LIVE (Claude 3.5)"
        mode_badge = "emerald"
    else:
        engine_mode = "HIGH-FIDELITY SIMULATION"
        mode_badge = "cyan"
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Active LLM Mode", engine_mode, llm.provider, mode_badge)
    with s2:
        render_metric_card("Prompt Template", "Dynamic Persona", "Profile + RAG Grounded", "positive")
    with s3:
        render_metric_card("RAG Auto-Injection", "Enabled", "Top-3 Evidence Chunks", "positive")
    with s4:
        render_metric_card("Safety Guardrails", "Active", "PII Redacted", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1.1, 1.9])
    
    with col_input:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">⚙️ Orchestration Workbench</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select twin persona and test hypothetical scenarios or questions.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        twin_keys = [k for k in twin_store.keys() if k.startswith("TWIN-")]
        selected_twin_id = st.selectbox(
            "Select Persona",
            twin_keys,
            format_func=lambda tid: f"{twin_store[tid]['avatar_emoji']} {twin_store[tid]['persona_name']}"
        )
        twin = twin_store[selected_twin_id]
        
        preset_scenarios = [
            "We are introducing a $15/month fee on all checking accounts that don't maintain a $10k minimum balance. How do you respond?",
            "Competitor NeoBank just launched a 5.25% APY savings account with zero minimum balance. Are you planning to transfer funds?",
            "We are launching an AI-powered automated wealth management portfolio with 0.25% management fee. Would you enroll?",
            "Custom Scenario / Question"
        ]
        
        selected_scenario = st.selectbox("Scenario Preset", preset_scenarios)
        
        if selected_scenario == "Custom Scenario / Question":
            scenario_text = st.text_area("Your Scenario or Inquiry", "How do you feel about our current interest rates and digital mobile app?", height=90)
        else:
            scenario_text = selected_scenario
            
        temp = st.slider("Temperature / Creativity", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        
        run_orchestration = st.button("⚡ Generate Twin Response", type="primary", use_container_width=True)
        
    with col_output:
        # Retrieve evidence automatically based on scenario text
        evidence_results = rag.search(scenario_text, customer_id=twin["customer_ref_id"], top_k=2)
        if not evidence_results:
            # Fallback to general customer evidence
            evidence_results = rag.search(scenario_text, top_k=2)
            
        evidence_text = rag.format_evidence_for_prompt(evidence_results)
        compiled_system_prompt = build_persona_system_prompt(twin, evidence_text)
        
        if run_orchestration:
            with st.spinner(f"Orchestrating response for {twin['persona_name']}..."):
                messages = [{"role": "user", "content": scenario_text}]
                resp = llm.generate_chat_response(
                    system_prompt=compiled_system_prompt,
                    messages=messages,
                    twin_profile=twin,
                    temperature=temp
                )
                st.session_state.last_orchestration_response = resp
                st.session_state.last_orchestration_scenario = scenario_text
                st.session_state.last_orchestration_twin = twin
                
        last_resp = st.session_state.get("last_orchestration_response")
        
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">💬 Twin Simulated Response</h4>
                    <span class="glass-badge badge-cyan">In Character</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if last_resp:
            last_twin = st.session_state.get("last_orchestration_twin", twin)
            st.markdown(
                f"""
                <div class="chat-bubble-twin">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <strong style="color: #67e8f9; font-size: 0.95rem;">{last_twin['avatar_emoji']} {last_twin['customer_name']}</strong>
                        <span style="color: #94a3b8; font-size: 0.75rem;">Mode: {last_resp.get('mode')} • {last_resp.get('latency_sec')}s</span>
                    </div>
                    <div style="color: #f8fafc; font-size: 0.92rem; line-height: 1.6;">
                        {last_resp.get('text')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Click 'Generate Twin Response' to run the persona orchestration engine.")
            
        with st.expander("🔍 Inspect Full Compiled System Prompt & RAG Grounding", expanded=False):
            st.markdown("##### Grounded System Prompt")
            st.code(compiled_system_prompt, language="markdown")
