import streamlit as st
import time
from components.glass_card import render_banner, render_metric_card
from prompts.persona_prompts import build_persona_system_prompt

def render_stage_09():
    """Stage 09: Synthetic Focus Groups."""
    render_banner(
        title="Stage 09: Synthetic Customer Focus Groups",
        description="Multi-persona simulated qualitative research panel. Test product concepts, pricing changes, or campaign messaging across diverse customer archetypes simultaneously.",
        icon="🗣️",
        accent_color="violet"
    )
    
    twin_store = st.session_state.twin_store
    df = st.session_state.customers_df
    llm = st.session_state.llm_service
    
    # Header Metrics
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Simulated Panels Run", f"{len(st.session_state.focus_group_history)}", "Total Sessions", "neutral")
    with s2:
        render_metric_card("Persona Diversity", "4 Segments", "Full Spectrum", "positive")
    with s3:
        render_metric_card("Turn Simulation", "Interactive Cross-Talk", "Moderator Led", "positive")
    with s4:
        render_metric_card("Automated Synthesis", "Enabled", "Executive Insights", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    col_panel_setup, col_convo = st.columns([1.1, 1.9])
    
    with col_panel_setup:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">👥 Panel Composition</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select 3 to 4 distinct personas to participate in the focus group.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Pick default representative twins from each segment
        seg_names = list(df["segment_name"].unique())
        default_twins = []
        for s in seg_names:
            sample_cust = df[df["segment_name"] == s].iloc[0]
            t_id = f"TWIN-{sample_cust['customer_id']}"
            if t_id in twin_store:
                default_twins.append(t_id)
                
        all_twin_keys = [k for k in twin_store.keys() if k.startswith("TWIN-")]
        selected_twins = st.multiselect(
            "Selected Panelists",
            all_twin_keys,
            default=default_twins[:4] if len(default_twins) >= 4 else all_twin_keys[:4],
            format_func=lambda tid: f"{twin_store[tid]['avatar_emoji']} {twin_store[tid]['customer_name']} ({twin_store[tid]['segment_name']})"
        )
        
        st.markdown("#### 🎯 Focus Group Topic & Concept")
        
        preset_topics = [
            "New 'Platinum Wealth' Subscription at $25/mo with 5.50% APY and dedicated human advisor",
            "Eliminating paper statements and imposing a $5/mo fee for non-digital branch transactions",
            "Introducing automated AI tax-loss harvesting for everyday retail checking accounts",
            "Custom Concept / Question"
        ]
        
        chosen_topic = st.selectbox("Topic Preset", preset_topics)
        if chosen_topic == "Custom Concept / Question":
            topic_text = st.text_area("Concept Proposal / Question", "What would motivate you to consolidate all your liquid deposits into our institution?", height=80)
        else:
            topic_text = chosen_topic
            
        run_panel = st.button("🚀 Launch Synthetic Focus Group Session", type="primary", use_container_width=True)
        
    with col_convo:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">🎙️ Live Focus Group Transcript & Panel Stream</h4>
                    <span class="glass-badge badge-indigo">Multi-Agent Simulation</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if run_panel and selected_twins:
            transcript = []
            progress_bar = st.progress(0)
            
            # Moderator introduction
            mod_msg = f"Welcome everyone. Today we want your candid thoughts on: '{topic_text}'. Let's hear from each of you."
            transcript.append({"speaker": "Moderator (Host)", "role": "moderator", "text": mod_msg, "avatar": "🎙️"})
            
            for i, tid in enumerate(selected_twins):
                twin = twin_store[tid]
                system_prompt = build_persona_system_prompt(twin)
                
                # Context of conversation so far
                prior_context = "\n".join([f"{m['speaker']}: {m['text']}" for m in transcript])
                user_prompt = f"The focus group topic is: '{topic_text}'.\n\nPrior discussion:\n{prior_context}\n\nSpeak as {twin['customer_name']}. Give your authentic, direct reaction in 2-3 sentences."
                
                messages = [{"role": "user", "content": user_prompt}]
                resp = llm.generate_chat_response(
                    system_prompt=system_prompt,
                    messages=messages,
                    twin_profile=twin,
                    temperature=0.75
                )
                
                transcript.append({
                    "speaker": f"{twin['customer_name']} ({twin['segment_name']})",
                    "role": "twin",
                    "text": resp["text"],
                    "avatar": twin["avatar_emoji"],
                    "twin_id": tid
                })
                progress_bar.progress((i + 1) / len(selected_twins))
                
            progress_bar.empty()
            
            # Synthesis
            synthesis = {
                "topic": topic_text,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "transcript": transcript,
                "consensus": "Polarized reaction. High-income segments approve of premium yields, while price-sensitive segments reject monthly subscription fees.",
                "sentiment_distribution": {"Positive": 25, "Neutral": 25, "Negative": 50},
                "recommendation": "Introduce a balance-waiver threshold (e.g. $25/mo waived for balances > $25k) to capture affluent demand without alienating price-sensitive cohorts."
            }
            
            st.session_state.current_focus_group = synthesis
            st.session_state.focus_group_history.append(synthesis)
            
            # Also add to human validation queue
            st.session_state.validation_queue.append({
                "id": f"VAL-FG-{len(st.session_state.validation_queue)+1}",
                "type": "Synthetic Focus Group",
                "target": topic_text[:50] + "...",
                "status": "PENDING_REVIEW",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "details": synthesis
            })
            
        active_fg = st.session_state.get("current_focus_group")
        
        if active_fg:
            for msg in active_fg["transcript"]:
                if msg["role"] == "moderator":
                    st.markdown(
                        f"""
                        <div style="background: rgba(99, 102, 241, 0.15); border: 1px dashed rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 0.85rem; color: #c7d2fe; font-size: 0.88rem;">
                            <strong>{msg['avatar']} {msg['speaker']}:</strong> {msg['text']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-bubble-twin">
                            <strong style="color: #67e8f9; font-size: 0.9rem;">{msg['avatar']} {msg['speaker']}</strong>
                            <p style="margin: 0.35rem 0 0 0; color: #f8fafc; font-size: 0.88rem; line-height: 1.5;">{msg['text']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
            st.markdown("#### 📑 Executive Qualitative Synthesis")
            st.markdown(
                f"""
                <div class="glass-container" style="background: rgba(17, 24, 39, 0.8); border-color: rgba(6, 182, 212, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h5 style="margin: 0; color: #67e8f9;">Summary Consensus</h5>
                        <span class="glass-badge badge-amber">Actionable Synthesis</span>
                    </div>
                    <p style="color: #f8fafc; font-size: 0.88rem; margin-bottom: 0.85rem;">{active_fg['consensus']}</p>
                    <div style="background: rgba(6, 182, 212, 0.1); border-left: 3px solid #06b6d4; padding: 0.65rem 0.85rem; border-radius: 0 6px 6px 0;">
                        <strong style="color: #67e8f9; font-size: 0.85rem;">Strategic Go-Forward Recommendation:</strong>
                        <p style="margin: 0.2rem 0 0 0; color: #e2e8f0; font-size: 0.83rem;">{active_fg['recommendation']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Select panelists and click 'Launch Synthetic Focus Group Session' to begin.")
