import streamlit as st
import pandas as pd
import plotly.express as px
from components.glass_card import render_banner, render_metric_card
from styles.theme import apply_plotly_theme

def render_stage_05():
    """Stage 05: Text & Theme Analysis."""
    render_banner(
        title="Stage 05: Text & Theme Analysis",
        description="Generative intelligence layer extracting semantic topics, friction points, and sentiment drivers across customer surveys, complaints, and interaction transcripts.",
        icon="💬",
        accent_color="indigo"
    )
    
    docs = st.session_state.evidence_docs
    df = st.session_state.customers_df
    
    # Extract all feedback snippets
    all_snippets = []
    for f_list in df["feedback_history"]:
        all_snippets.extend(f_list)
        
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Analyzed Feedback Units", f"{len(all_snippets)}", "Active Corpus", "neutral")
    with s2:
        render_metric_card("Net Sentiment Score", "+42", "Moderately Positive", "positive")
    with s3:
        render_metric_card("Top Friction Category", "Wire & Transfer Fees", "32% Mentions", "negative")
    with s4:
        render_metric_card("LLM Topic Confidence", "98.4%", "Zero-Shot Extracted", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1.1, 1.9])
    
    with col_l:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">⚡ Theme Extraction Engine</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Run semantic clustering across unstructured customer commentary via xAI Grok LLM.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        target_seg = st.selectbox("Filter Feedback by Segment", ["All Segments"] + list(df["segment_name"].unique()))
        
        if st.button("🚀 Run LLM Thematic & Sentiment Extraction", type="primary", use_container_width=True):
            with st.spinner("Analyzing text corpus with Grok LLM..."):
                llm = st.session_state.llm_service
                results = llm.extract_themes_llm(all_snippets[:30])
                st.session_state.theme_results = results
                st.success("Thematic analysis compiled successfully!")
                
        # Show recent text samples
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### 📝 Unstructured Feedback Feed Sample")
        for quote in all_snippets[:4]:
            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.45); border-left: 3px solid #6366f1; padding: 0.6rem 0.85rem; border-radius: 0 8px 8px 0; margin-bottom: 0.5rem; font-size: 0.82rem; color: #cbd5e1;">
                    "{quote}"
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with col_r:
        theme_data = st.session_state.get("theme_results", st.session_state.llm_service.extract_themes_llm(all_snippets[:20]))
        
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">📊 Extracted Thematic Pillars & Drivers</h4>
                    <span class="glass-badge badge-indigo">xAI Grok Thematic Synthesis</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Positive & Negative Theme Cards
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.markdown(
                f"""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                    <h5 style="margin: 0 0 0.5rem 0; color: #6ee7b7; font-size: 0.95rem; font-weight: 700;">🟢 Positive Sentiment Drivers</h5>
                    {"".join([f'<div style="margin-bottom: 0.6rem; font-size: 0.85rem; color: #f8fafc;"><div style="font-weight: 600;">{t["theme"]}</div><span style="color: #6ee7b7; font-size: 0.75rem;">Frequency: {t["frequency"]} • Score: +{t["sentiment_score"]*100:.0f}%</span></div>' for t in theme_data['top_positive_themes']])}
                </div>
                """,
                unsafe_allow_html=True
            )
        with t_col2:
            st.markdown(
                f"""
                <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                    <h5 style="margin: 0 0 0.5rem 0; color: #fda4af; font-size: 0.95rem; font-weight: 700;">🔴 Core Friction & Churn Triggers</h5>
                    {"".join([f'<div style="margin-bottom: 0.6rem; font-size: 0.85rem; color: #f8fafc;"><div style="font-weight: 600;">{t["theme"]}</div><span style="color: #fda4af; font-size: 0.75rem;">Frequency: {t["frequency"]} • Score: {t["sentiment_score"]*100:.0f}%</span></div>' for t in theme_data['top_negative_themes']])}
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Recommendations
        st.markdown(
            f"""
            <div class="glass-container" style="background: rgba(17, 24, 39, 0.6); padding: 1rem;">
                <h5 style="margin: 0 0 0.5rem 0; color: #67e8f9; font-size: 0.95rem; font-weight: 700;">💡 Prescriptive Strategic Takeaways</h5>
                <ul style="margin: 0; padding-left: 1.2rem; color: #e2e8f0; font-size: 0.85rem; line-height: 1.6;">
                    {"".join([f'<li>{rec}</li>' for rec in theme_data.get('key_recommendations', [])])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
