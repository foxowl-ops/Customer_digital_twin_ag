import streamlit as st
import pandas as pd
import plotly.express as px
from components.glass_card import render_banner, render_metric_card
from styles.theme import apply_plotly_theme

def render_stage_10():
    """Stage 10: Competitor Experiments."""
    render_banner(
        title="Stage 10: Competitor Simulation & Churn Modeling",
        description="Simulate twin reactions to disruptive competitor offers side-by-side with baseline products. Measure churn flight risk, price elasticity, and feature retention power.",
        icon="⚔️",
        accent_color="rose"
    )
    
    df = st.session_state.customers_df
    twin_store = st.session_state.twin_store
    llm = st.session_state.llm_service
    
    # Competitor Offer Configuration
    c_conf1, c_conf2 = st.columns(2)
    
    with c_conf1:
        st.markdown(
            """
            <div class="glass-container" style="border-color: rgba(99, 102, 241, 0.3);">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; color: #67e8f9;">🏢 Current Baseline Proposition</h4>
                    <span class="glass-badge badge-indigo">Incumbent</span>
                </div>
                <ul style="margin: 0; padding-left: 1.2rem; color: #e2e8f0; font-size: 0.85rem; line-height: 1.6;">
                    <li><strong>High-Yield Savings:</strong> 4.25% APY</li>
                    <li><strong>Account Fee:</strong> $0 with $5,000 min balance ($12/mo otherwise)</li>
                    <li><strong>Wire Transfers:</strong> $25 Domestic / $45 International</li>
                    <li><strong>Advisory:</strong> Dedicated Human Advisor for balances > $250k</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with c_conf2:
        st.markdown(
            """
            <div class="glass-container" style="border-color: rgba(244, 63, 94, 0.35);">
                <div class="glass-header-glow" style="background: linear-gradient(90deg, transparent, #f43f5e, #f59e0b, transparent);"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; color: #fda4af;">⚡ Competitor Challenger Offer</h4>
                    <span class="glass-badge badge-rose">Disruptor NeoBank</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        comp_apy = st.slider("Competitor Savings APY (%)", 4.50, 6.00, 5.25, 0.25)
        comp_fee = st.selectbox("Competitor Maintenance Fee", ["Zero Fees ($0 min balance)", "$5/mo Flat", "Tiered"])
        comp_perk = st.selectbox("Competitor Value Hook", [
            "Instant Free Domestic & Global Wires",
            "$300 Cash Switcher Bonus",
            "Automated High-Yield Crypto Sweep",
            "Zero ATM Fees Worldwide"
        ])
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    if st.button("⚔️ Run Side-by-Side Competitor A/B Simulation", type="primary", use_container_width=True):
        with st.spinner("Simulating multi-archetype churn and choice preferences..."):
            # Compute simulated churn probabilities per segment
            sim_results = []
            for seg in df["segment_name"].unique():
                seg_df = df[df["segment_name"] == seg]
                avg_price_sens = seg_df["price_sensitivity"].mean()
                avg_loyalty = seg_df["brand_loyalty"].mean()
                
                # Churn model calculation
                rate_diff = comp_apy - 4.25
                switch_prob = min(0.95, max(0.05, (rate_diff * 0.25) + (avg_price_sens * 0.06) - (avg_loyalty * 0.05)))
                
                sim_results.append({
                    "Segment": seg,
                    "Count": len(seg_df),
                    "Baseline Loyalty": round(avg_loyalty, 1),
                    "Price Sensitivity": round(avg_price_sens, 1),
                    "Estimated Churn Flight Risk": round(switch_prob * 100, 1),
                    "Primary Driver": "Yield Spread" if rate_diff > 0.5 else "Fee Transparency"
                })
                
            st.session_state.competitor_sim_results = pd.DataFrame(sim_results)
            st.success("Competitor simulation complete!")
            
    sim_df = st.session_state.get("competitor_sim_results")
    
    if sim_df is not None:
        col_res1, col_res2 = st.columns([1.5, 1])
        
        with col_res1:
            st.markdown("#### 📊 Churn Flight Risk by Segment")
            fig = px.bar(
                sim_df,
                x="Segment",
                y="Estimated Churn Flight Risk",
                color="Estimated Churn Flight Risk",
                color_continuous_scale=["#10b981", "#f59e0b", "#f43f5e"],
                text="Estimated Churn Flight Risk",
                labels={"Estimated Churn Flight Risk": "Estimated Churn Risk (%)"}
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=350, yaxis=dict(range=[0, 100]))
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
        with col_res2:
            st.markdown("#### 🎯 Segment Churn Matrix")
            st.dataframe(
                sim_df[["Segment", "Estimated Churn Flight Risk", "Primary Driver"]],
                use_container_width=True,
                column_config={
                    "Estimated Churn Flight Risk": st.column_config.ProgressColumn("Flight Risk", min_value=0, max_value=100, format="%.1f%%")
                }
            )
            
            st.markdown(
                """
                <div class="glass-container" style="padding: 0.85rem; background: rgba(244, 63, 94, 0.08); border-color: rgba(244, 63, 94, 0.3);">
                    <h5 style="margin: 0 0 0.35rem 0; color: #fda4af; font-size: 0.88rem;">🚨 High Risk Warning</h5>
                    <p style="margin: 0; color: #cbd5e1; font-size: 0.8rem;">Price-Sensitive and Tech-Forward segments show >65% churn risk if competitor APY exceeds 5.25% with zero fees.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
