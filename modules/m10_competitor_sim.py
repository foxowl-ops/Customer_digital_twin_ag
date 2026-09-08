import streamlit as st
import pandas as pd
import plotly.express as px
from components.glass_card import render_banner, render_metric_card
from styles.theme import apply_plotly_theme

def render_stage_10():
    """Stage 10: Competitor Experiments."""
    render_banner(
        title="Stage 10: Competitor Simulation & Lapse Modeling",
        description="Simulate twin reactions to disruptive competitor offers side-by-side with baseline policies. Measure lapse flight risk, premium elasticity, and feature retention power.",
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
                    <h4 style="margin: 0; color: var(--accent-cyan-text);">🏢 Current Baseline Proposition</h4>
                    <span class="glass-badge badge-indigo">Incumbent</span>
                </div>
                <ul style="margin: 0; padding-left: 1.2rem; color: var(--text-body); font-size: 0.85rem; line-height: 1.6;">
                    <li><strong>Auto + Home Bundle Premium:</strong> ₹17,482/mo baseline</li>
                    <li><strong>Policy Fee:</strong> ₹0 with 2+ bundled policies (₹1,134/mo otherwise)</li>
                    <li><strong>Claims Response SLA:</strong> 48hr Domestic / 72hr Out-of-State</li>
                    <li><strong>Advisory:</strong> Dedicated Human Agent for insured asset value > ₹2.36 Cr</li>
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
                    <h4 style="margin: 0; color: var(--accent-rose-text);">⚡ Competitor Challenger Offer</h4>
                    <span class="glass-badge badge-rose">Disruptor InsurTech</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        comp_discount = st.slider("Competitor Premium Discount (%)", 0.0, 30.0, 20.0, 1.0)
        comp_fee = st.selectbox("Competitor Policy Fee", ["Zero Fees (bundled policies)", "₹472/mo Flat", "Tiered"])
        comp_perk = st.selectbox("Competitor Value Hook", [
            "Instant Digital First-Notice-of-Loss Claims",
            "₹28,350 Cash Switcher Bonus",
            "Usage-Based Telematics Discount",
            "Zero Deductible on First Claim"
        ])

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if st.button("⚔️ Run Side-by-Side Competitor A/B Simulation", type="primary", use_container_width=True):
        with st.spinner("Simulating multi-archetype lapse and switching preferences..."):
            # Compute simulated lapse (switch) probabilities per segment
            sim_results = []
            for seg in df["segment_name"].unique():
                seg_df = df[df["segment_name"] == seg]
                avg_price_sens = seg_df["price_sensitivity"].mean()
                avg_loyalty = seg_df["brand_loyalty"].mean()

                # Lapse/switch model calculation
                switch_prob = min(0.95, max(0.05, (comp_discount * 0.015) + (avg_price_sens * 0.06) - (avg_loyalty * 0.05)))

                sim_results.append({
                    "Segment": seg,
                    "Count": len(seg_df),
                    "Baseline Loyalty": round(avg_loyalty, 1),
                    "Price Sensitivity": round(avg_price_sens, 1),
                    "Estimated Lapse Flight Risk": round(switch_prob * 100, 1),
                    "Primary Driver": "Premium Spread" if comp_discount > 10 else "Fee Transparency"
                })

            st.session_state.competitor_sim_results = pd.DataFrame(sim_results)
            st.success("Competitor simulation complete!")
            
    sim_df = st.session_state.get("competitor_sim_results")
    
    if sim_df is not None:
        col_res1, col_res2 = st.columns([1.5, 1])
        
        with col_res1:
            st.markdown("#### 📊 Lapse Flight Risk by Segment")
            fig = px.bar(
                sim_df,
                x="Segment",
                y="Estimated Lapse Flight Risk",
                color="Estimated Lapse Flight Risk",
                color_continuous_scale=["#10b981", "#f59e0b", "#f43f5e"],
                text="Estimated Lapse Flight Risk",
                labels={"Estimated Lapse Flight Risk": "Estimated Lapse Risk (%)"}
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=350, yaxis=dict(range=[0, 100]))
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
        with col_res2:
            st.markdown("#### 🎯 Segment Lapse Matrix")
            st.dataframe(
                sim_df[["Segment", "Estimated Lapse Flight Risk", "Primary Driver"]],
                use_container_width=True,
                column_config={
                    "Estimated Lapse Flight Risk": st.column_config.ProgressColumn("Flight Risk", min_value=0, max_value=100, format="%.1f%%")
                }
            )
            
            st.markdown(
                """
                <div class="glass-container" style="padding: 0.85rem; background: rgba(244, 63, 94, 0.08); border-color: rgba(244, 63, 94, 0.3);">
                    <h5 style="margin: 0 0 0.35rem 0; color: var(--accent-rose-text); font-size: 0.88rem;">🚨 High Risk Warning</h5>
                    <p style="margin: 0; color: var(--text-secondary-body); font-size: 0.8rem;">Premium-Sensitive and Digitally-Savvy segments show >65% lapse risk if the competitor premium discount exceeds 20% with zero fees.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
