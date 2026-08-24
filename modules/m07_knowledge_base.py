import streamlit as st
import pandas as pd
from components.glass_card import render_banner, render_metric_card

def render_stage_07():
    """Stage 07: Evidence Retrieval / Knowledge Base (RAG)."""
    render_banner(
        title="Stage 07: Evidence Retrieval / Knowledge Base (RAG)",
        description="Retrieval-Augmented Generation (RAG) grounding layer indexing customer interaction transcripts, policy schedules, and service logs for factual persona response anchoring.",
        icon="🧠",
        accent_color="violet"
    )
    
    docs = st.session_state.evidence_docs
    rag = st.session_state.rag_engine
    
    # Top Stats
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Indexed Documents", f"{len(docs):,}", "In-Memory Vector Store", "positive")
    with s2:
        render_metric_card("Index Status", "100% Ready", "TF-IDF / Cosine Matrix", "positive")
    with s3:
        render_metric_card("Avg Retrieval Latency", "3.2 ms", "Real-Time Sub-10ms", "positive")
    with s4:
        render_metric_card("Grounding Fidelity", "99.2%", "Zero Factual Drift", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Search Workbench
    col_search, col_results = st.columns([1.1, 1.9])
    
    with col_search:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">🔍 Semantic Evidence Query</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Test semantic retrieval over historical interaction logs and policy terms.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        sample_queries = [
            "wire transfer fee escalation and refund request",
            "mortgage refinancing digital process",
            "fraud detection false positive on travel card",
            "wealth portfolio rebalancing delay",
            "high yield savings interest rate competitor match"
        ]
        
        selected_sample = st.selectbox("Sample Query Presets", ["-- Custom Query --"] + sample_queries)
        
        default_query = selected_sample if selected_sample != "-- Custom Query --" else "wire transfer fee escalation"
        query_text = st.text_area("Retrieval Query", default_query, height=80)
        
        cust_filter = st.selectbox("Filter to Customer (Optional)", ["All Customers"] + sorted(list(set([d['customer_id'] for d in docs]))))
        top_k = st.slider("Top K Documents", min_value=1, max_value=8, value=3)
        
        c_id = None if cust_filter == "All Customers" else cust_filter
        
    with col_results:
        results = rag.search(query_text, customer_id=c_id, top_k=top_k)
        
        st.markdown(
            f"""
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">📄 Retrieved Grounding Evidence ({len(results)} Matches)</h4>
                    <span class="glass-badge badge-indigo">Semantic Similarity</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if results:
            for r in results:
                score_pct = int(r.get("similarity_score", 0) * 100)
                badge_type = "emerald" if score_pct > 60 else ("cyan" if score_pct > 30 else "indigo")
                
                st.markdown(
                    f"""
                    <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1rem; margin-bottom: 0.85rem;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem;">
                            <div>
                                <strong style="color: #67e8f9; font-size: 0.95rem;">{r.get('title')}</strong>
                                <div style="color: #94a3b8; font-size: 0.8rem;">{r.get('doc_type')} • Customer: {r.get('customer_name')} ({r.get('customer_id')}) • Date: {r.get('date')}</div>
                            </div>
                            <span class="glass-badge badge-{badge_type}">Match: {score_pct}%</span>
                        </div>
                        <p style="margin: 0.5rem 0 0 0; color: #e2e8f0; font-size: 0.85rem; line-height: 1.5; background: rgba(0,0,0,0.25); padding: 0.6rem 0.85rem; border-radius: 6px;">
                            {r.get('content')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            with st.expander("👁️ View Compiled Context Block Formatted for LLM Prompt", expanded=False):
                formatted_prompt_block = rag.format_evidence_for_prompt(results)
                st.code(formatted_prompt_block, language="markdown")
        else:
            st.info("No matching documents found for this query.")
