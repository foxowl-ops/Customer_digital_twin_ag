import streamlit as st
import pandas as pd
from components.glass_card import render_banner, render_metric_card

def render_stage_03():
    """Stage 03: Customer Data Platform / Lakehouse Explorer."""
    render_banner(
        title="Stage 03: Customer Data Platform / Lakehouse Explorer",
        description="Unified analytics store and metadata catalog providing structured query exploration, multi-dimensional customer 360 slicing, and real-time profile drilldown.",
        icon="🗄️",
        accent_color="indigo"
    )
    
    df = st.session_state.customers_df
    
    # Top Stats
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Total Ingested Deposits", f"${df['total_balance'].sum():,.0f}", "Across All Accounts", "neutral")
    with s2:
        render_metric_card("Avg Customer Balance", f"${df['total_balance'].mean():,.0f}", "Healthy Liquidity", "positive")
    with s3:
        render_metric_card("Avg Credit Score", f"{df['credit_score'].mean():.0f}", "Prime Tier", "positive")
    with s4:
        render_metric_card("Avg Products / Customer", f"{df['product_count'].mean():.1f}", "High Multi-Product Depth", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Filter Sidebar / Controls
    col_filter, col_table = st.columns([1, 2.5])
    
    with col_filter:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">🔍 Lakehouse Query Builder</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Filter unified customer dataset across demographic & financial dimensions.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Filters
        min_inc, max_inc = int(df["annual_income"].min()), int(df["annual_income"].max())
        income_range = st.slider("Annual Income ($)", min_inc, max_inc, (min_inc, max_inc), step=10000)
        
        segments = ["All"] + sorted(list(df["segment_name"].dropna().unique()))
        selected_seg = st.selectbox("Customer Segment", segments)
        
        risk_opts = ["All"] + list(df["risk_appetite"].unique())
        selected_risk = st.selectbox("Risk Appetite", risk_opts)
        
        search_query = st.text_input("Search Name, ID, City, or Occupation", "")
        
    with col_table:
        filtered_df = df.copy()
        
        # Apply filters
        filtered_df = filtered_df[
            (filtered_df["annual_income"] >= income_range[0]) &
            (filtered_df["annual_income"] <= income_range[1])
        ]
        
        if selected_seg != "All":
            filtered_df = filtered_df[filtered_df["segment_name"] == selected_seg]
            
        if selected_risk != "All":
            filtered_df = filtered_df[filtered_df["risk_appetite"] == selected_risk]
            
        if search_query:
            q = search_query.lower()
            filtered_df = filtered_df[
                filtered_df["name"].str.lower().str.contains(q) |
                filtered_df["customer_id"].str.lower().str.contains(q) |
                filtered_df["city"].str.lower().str.contains(q) |
                filtered_df["occupation"].str.lower().str.contains(q)
            ]
            
        st.markdown(
            f"""
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">📊 Lakehouse Unified Dataset ({len(filtered_df)} Records Found)</h4>
                    <span class="glass-badge badge-cyan">Delta Lake v3.2</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        show_cols = [
            "customer_id", "name", "age", "occupation", "city", "annual_income",
            "net_worth", "total_balance", "segment_name", "risk_appetite", "churn_risk"
        ]
        
        st.dataframe(
            filtered_df[show_cols],
            use_container_width=True,
            column_config={
                "customer_id": "Customer ID",
                "name": "Customer Name",
                "annual_income": st.column_config.NumberColumn("Income", format="$%d"),
                "net_worth": st.column_config.NumberColumn("Net Worth", format="$%d"),
                "total_balance": st.column_config.NumberColumn("Balance", format="$%d"),
                "churn_risk": st.column_config.ProgressColumn("Churn Risk", min_value=0.0, max_value=1.0, format="%.2f"),
            }
        )
        
        # Single Customer 360 Drilldown
        if not filtered_df.empty:
            with st.expander("👤 Customer 360 Deep-Dive Inspector", expanded=False):
                inspect_id = st.selectbox("Select Customer to Drilldown", filtered_df["customer_id"].tolist(), key="drill_id")
                drill_row = filtered_df[filtered_df["customer_id"] == inspect_id].iloc[0]
                
                c_d1, c_d2 = st.columns(2)
                with c_d1:
                    st.markdown(f"**Customer ID:** `{drill_row['customer_id']}`")
                    st.markdown(f"**Full Name:** `{drill_row['name']}`")
                    st.markdown(f"**Occupation:** `{drill_row['occupation']}` ({drill_row['city']}, {drill_row['state']})")
                    st.markdown(f"**Tenure:** `{drill_row['tenure_years']} years`")
                    st.markdown(f"**Holdings:** {', '.join(drill_row['products_held'])}")
                with c_d2:
                    st.markdown(f"**Segment:** `{drill_row['segment_name']}`")
                    st.markdown(f"**Price Sensitivity:** `{drill_row['price_sensitivity']}/10`")
                    st.markdown(f"**Brand Loyalty:** `{drill_row['brand_loyalty']}/10`")
                    st.markdown(f"**Digital Engagement:** `{drill_row['digital_engagement']}/100`")
                    st.markdown(f"**Recent Quote:** *'{drill_row['feedback_history'][0]}'*")
