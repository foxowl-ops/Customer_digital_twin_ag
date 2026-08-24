import streamlit as st
import pandas as pd
from components.glass_card import render_banner, render_metric_card
from core.data_gen import generate_synthetic_customers, generate_evidence_documents

def render_stage_01():
    """Stage 01: Data Ingestion Layer."""
    render_banner(
        title="Stage 01: Customer & Market Data Ingestion",
        description="Simulated multi-source data ingestion pipeline integrating Core Banking, CRM, Policy Administration, and Market Signal feeds into an unified data model.",
        icon="📥",
        accent_color="indigo"
    )
    
    df = st.session_state.customers_df
    docs = st.session_state.evidence_docs
    market_signals = st.session_state.market_signals
    
    # Key Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Ingested Customers", f"{len(df):,}", "+150 New", "positive")
    with m2:
        render_metric_card("Interaction Documents", f"{len(docs):,}", "Active RAG Store", "neutral")
    with m3:
        render_metric_card("Market Signals", f"{len(market_signals)}", "Live Feeds", "neutral")
    with m4:
        render_metric_card("Pipeline Health", "100%", "0 Schema Errors", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Ingestion Controls & Live Feed Inspector
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">⚙️ Ingestion Pipeline Controls</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Trigger synthetic pipeline re-ingestion or adjust sample generation parameters.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        sample_size = st.slider("Sample Population Size", min_value=50, max_value=300, value=len(df), step=25)
        
        if st.button("🔄 Re-generate & Ingest Synthetic Pipeline", type="primary", use_container_width=True):
            with st.spinner("Simulating multi-source ingestion ETL..."):
                new_df = generate_synthetic_customers(sample_size)
                from core.ml_segmentation import run_customer_segmentation
                clustered_df, seg_summary_df, _ = run_customer_segmentation(new_df)
                new_docs = generate_evidence_documents(clustered_df)
                
                st.session_state.customers_df = clustered_df
                st.session_state.seg_summary_df = seg_summary_df
                st.session_state.evidence_docs = new_docs
                st.session_state.rag_engine.index_documents(new_docs)
                
                # Rebuild twins
                from core.state import build_default_twin_profile
                twin_store = {}
                for _, row in clustered_df.iterrows():
                    t = build_default_twin_profile(row, version="v1.0")
                    twin_store[t["twin_id"]] = t
                    twin_store[row["customer_id"]] = t
                st.session_state.twin_store = twin_store
                
                st.success(f"Successfully ingested {sample_size} customer records and {len(new_docs)} documents!")
                st.rerun()
                
        st.markdown(
            """
            <div class="glass-container" style="margin-top: 1rem; padding: 1rem;">
                <h5 style="margin: 0 0 0.5rem 0; color: #67e8f9; font-size: 0.9rem;">📡 Live Pipeline Feeds</h5>
                <ul style="margin: 0; padding-left: 1.2rem; color: #94a3b8; font-size: 0.82rem; line-height: 1.6;">
                    <li><strong style="color: #e2e8f0;">Core Banking (FIS/Temenos)</strong>: Daily balances & deposits</li>
                    <li><strong style="color: #e2e8f0;">Policy Administration (Guidewire)</strong>: Active coverage terms</li>
                    <li><strong style="color: #e2e8f0;">CRM Interaction Stream (Salesforce)</strong>: Transcripts & CSAT</li>
                    <li><strong style="color: #e2e8f0;">Market & Regulatory Feed</strong>: Fed rate updates & competitor signals</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_r:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">📋 Real-Time Ingestion Buffer Preview</h4>
                    <span class="glass-badge badge-indigo">Schema Verified</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        tab1, tab2, tab3 = st.tabs(["Customer Accounts", "Evidence Documents", "External Market Signals"])
        
        with tab1:
            preview_cols = ["customer_id", "name", "age", "occupation", "annual_income", "total_balance", "credit_score"]
            st.dataframe(
                df[preview_cols].head(8),
                use_container_width=True,
                column_config={
                    "customer_id": "Customer ID",
                    "name": "Customer Name",
                    "annual_income": st.column_config.NumberColumn("Annual Income", format="$%d"),
                    "total_balance": st.column_config.NumberColumn("Total Balance", format="$%d"),
                }
            )
            
        with tab2:
            docs_df = pd.DataFrame(docs)[["doc_id", "customer_id", "doc_type", "title", "sentiment", "date"]]
            st.dataframe(docs_df.head(8), use_container_width=True)
            
        with tab3:
            signals_df = pd.DataFrame(market_signals)
            st.dataframe(signals_df, use_container_width=True)
