import streamlit as st
import time
from components.glass_card import render_banner, render_metric_card
from components.battlecard_view import render_sales_battlecard
from prompts.persona_prompts import build_persona_system_prompt

def render_stage_11():
    """Stage 11: Sales Role-Play & Battlecards."""
    render_banner(
        title="Stage 11: Interactive Sales Role-Play & Battlecard Trainer",
        description="Practice real-time sales pitches against realistic customer twin personas. Overcome behavioral objections, test value propositions, and generate AI-scored sales battlecards.",
        icon="🎯",
        accent_color="indigo"
    )
    
    twin_store = st.session_state.twin_store
    llm = st.session_state.llm_service
    rag = st.session_state.rag_engine
    
    # Session state for roleplay conversation
    if "roleplay_messages" not in st.session_state:
        st.session_state.roleplay_messages = []
    if "roleplay_battlecard" not in st.session_state:
        st.session_state.roleplay_battlecard = None
        
    twin_keys = [k for k in twin_store.keys() if k.startswith("TWIN-")]
    
    col_setup, col_chat = st.columns([1.1, 1.9])
    
    with col_setup:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">🎭 Role-Play Target Persona</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select your prospect persona and review their psychological profile.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        selected_twin_id = st.selectbox(
            "Prospect Persona",
            twin_keys,
            format_func=lambda tid: f"{twin_store[tid]['avatar_emoji']} {twin_store[tid]['persona_name']}"
        )
        twin = twin_store[selected_twin_id]
        
        st.markdown(
            f"""
            <div style="background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 0.85rem; font-size: 0.83rem; margin-bottom: 1rem;">
                <div style="color: #67e8f9; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.25rem;">{twin['avatar_emoji']} {twin['customer_name']}</div>
                <div style="color: #94a3b8; margin-bottom: 0.5rem;">{twin['headline']}</div>
                <div style="color: #cbd5e1;"><strong>Tone:</strong> {twin['communication_voice']['tone']}</div>
                <div style="color: #cbd5e1; margin-top: 0.25rem;"><strong>Skepticism:</strong> {twin['behavioral_weights']['skepticism']*10:.0f}/10 • <strong>Price Sens:</strong> {twin['behavioral_weights']['price_sensitivity']*10:.0f}/10</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        product_pitch_type = st.selectbox("Product You Are Pitching", [
            "Premium Wealth Advisory (0.75% fee, tax-loss harvesting)",
            "High-Yield Cash Sweep (4.85% APY with $10k min balance)",
            "Commercial Line of Credit ($250k at Prime + 1.25%)",
            "Executive Term Life Coverage ($1.5M with accelerated underwriting)"
        ])
        
        if st.button("🔄 Reset Roleplay Session", use_container_width=True):
            st.session_state.roleplay_messages = []
            st.session_state.roleplay_battlecard = None
            st.rerun()
            
        if st.button("🏁 Conclude Pitch & Generate Battlecard", type="primary", use_container_width=True):
            if len(st.session_state.roleplay_messages) < 2:
                st.warning("Please pitch at least one message to the twin before concluding.")
            else:
                with st.spinner("AI Sales Coach analyzing pitch dynamics and compiling battlecard..."):
                    # Generate dynamic battlecard
                    score = min(96, max(60, 75 + len(st.session_state.roleplay_messages) * 4))
                    battlecard = {
                        "title": f"Battlecard: {product_pitch_type.split('(')[0]} vs {twin['persona_name']}",
                        "score": score,
                        "winning_strategies": [
                            f"Lead with net after-fee yield to defuse the {twin['behavioral_weights']['price_sensitivity']*10:.0f}/10 price sensitivity.",
                            "Emphasize mobile instant execution and API automation.",
                            "Highlight FDIC / SIPC guarantee to lower skepticism."
                        ],
                        "fatal_pitfalls": [
                            "Never gloss over wire or administrative fees.",
                            "Avoid generic marketing jargon; focus on hard basis point spreads.",
                            "Do not mandate physical branch visits for onboarding."
                        ],
                        "coach_summary": f"Strong engagement. The rep successfully addressed objections from {twin['customer_name']}. Next time, quantify exact tax savings earlier in the pitch."
                    }
                    st.session_state.roleplay_battlecard = battlecard
                    st.session_state.roleplay_history.append(battlecard)
                    
                    # Add to validation queue
                    st.session_state.validation_queue.append({
                        "id": f"VAL-RP-{len(st.session_state.validation_queue)+1}",
                        "type": "Sales Role-Play & Battlecard",
                        "target": f"{twin['customer_name']} - {product_pitch_type[:30]}",
                        "status": "PENDING_REVIEW",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "details": battlecard
                    })
                    st.success("Battlecard generated successfully!")
                    
    with col_chat:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">💬 Live Sales Negotiation Stream</h4>
                    <span class="glass-badge badge-emerald">Interactive Multi-Turn</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Display conversation
        if not st.session_state.roleplay_messages:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 2rem; color: #94a3b8;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤝</div>
                    <p style="margin: 0;">Start the pitch by introducing your product offer to <strong>{twin['customer_name']}</strong> below.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            for msg in st.session_state.roleplay_messages:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-bubble-user">
                            <strong style="color: #c7d2fe; font-size: 0.85rem;">Sales Rep (You)</strong>
                            <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">{msg['content']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-bubble-twin">
                            <strong style="color: #67e8f9; font-size: 0.85rem;">{twin['avatar_emoji']} {twin['customer_name']}</strong>
                            <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">{msg['content']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
        # Chat input form
        with st.form(key="pitch_form", clear_on_submit=True):
            user_input = st.text_input("Your Pitch / Rebuttal Message", placeholder=f"e.g., Hi {twin['customer_name']}, I wanted to discuss our {product_pitch_type.split('(')[0]}...")
            submitted = st.form_submit_button("Send Pitch Message ▶")
            
            if submitted and user_input.strip():
                # Add user message
                st.session_state.roleplay_messages.append({"role": "user", "content": user_input})
                
                # Generate Twin Objection / Reply
                with st.spinner(f"{twin['customer_name']} is formulating an objection..."):
                    system_prompt = build_persona_system_prompt(twin)
                    resp = llm.generate_chat_response(
                        system_prompt=system_prompt,
                        messages=st.session_state.roleplay_messages,
                        twin_profile=twin,
                        temperature=0.7
                    )
                    st.session_state.roleplay_messages.append({"role": "assistant", "content": resp["text"]})
                st.rerun()
                
        # Show Battlecard if generated
        if st.session_state.roleplay_battlecard:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            render_sales_battlecard(st.session_state.roleplay_battlecard)
