import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.glass_card import render_banner, render_metric_card
from core.ml_segmentation import run_customer_segmentation
from styles.theme import apply_plotly_theme

def render_stage_04():
    """Stage 04: Segmentation Models."""
    render_banner(
        title="Stage 04: Machine Learning Segmentation Models",
        description="Unsupervised clustering (K-Means & PCA) grouping customers into distinct behavioral archetypes based on financial footprint, digital habits, and price sensitivity.",
        icon="📊",
        accent_color="violet"
    )
    
    df = st.session_state.customers_df
    seg_summary_df = st.session_state.seg_summary_df
    
    # Archetype summary cards
    cols = st.columns(len(seg_summary_df))
    for i, (_, row) in enumerate(seg_summary_df.iterrows()):
        with cols[i]:
            st.markdown(
                f"""
                <div class="glass-container" style="padding: 1rem; border-color: rgba(99, 102, 241, 0.25);">
                    <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">{row['icon']}</div>
                    <h4 style="margin: 0 0 0.25rem 0; font-size: 0.95rem; color: #ffffff;">{row['name']}</h4>
                    <span class="glass-badge badge-cyan" style="font-size: 0.72rem; margin-bottom: 0.5rem;">{row['share_pct']}% of Base ({row['size']} users)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.4; margin-top: 0.35rem;">
                        <strong>Avg Income:</strong> ${row['avg_income']:,.0f}<br/>
                        <strong>Price Sens:</strong> {row['avg_price_sensitivity']}/10<br/>
                        <strong>Loyalty:</strong> {row['avg_brand_loyalty']}/10
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Visual Cluster Exploration
    col_plot, col_archetypes = st.columns([1.8, 1.2])
    
    with col_plot:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">🪐 Interactive Latent Space Clustering</h4>
                    <span class="glass-badge badge-indigo">PCA Latent Projection</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        plot_dim = st.radio("Visualization Mode", ["3D Latent Space (PCA)", "2D PCA Scatter", "Income vs. Total Balance"], horizontal=True)
        
        if plot_dim == "3D Latent Space (PCA)":
            fig = px.scatter_3d(
                df,
                x="pca_x",
                y="pca_y",
                z="pca_z",
                color="segment_name",
                hover_data=["customer_id", "name", "annual_income", "total_balance", "price_sensitivity"],
                color_discrete_sequence=["#6366f1", "#06b6d4", "#f59e0b", "#10b981", "#ec4899"],
                labels={"pca_x": "PCA 1 (Wealth & Scale)", "pca_y": "PCA 2 (Digital Engagement)", "pca_z": "PCA 3 (Price Sensitivity)"}
            )
            fig.update_layout(
                scene=dict(
                    xaxis=dict(backgroundcolor="rgba(17, 24, 39, 0.3)", gridcolor="rgba(255, 255, 255, 0.08)"),
                    yaxis=dict(backgroundcolor="rgba(17, 24, 39, 0.3)", gridcolor="rgba(255, 255, 255, 0.08)"),
                    zaxis=dict(backgroundcolor="rgba(17, 24, 39, 0.3)", gridcolor="rgba(255, 255, 255, 0.08)"),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
                height=460,
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_dim == "2D PCA Scatter":
            fig = px.scatter(
                df,
                x="pca_x",
                y="pca_y",
                color="segment_name",
                size="total_balance",
                hover_data=["customer_id", "name", "occupation", "churn_risk"],
                color_discrete_sequence=["#6366f1", "#06b6d4", "#f59e0b", "#10b981", "#ec4899"],
                labels={"pca_x": "Principal Component 1", "pca_y": "Principal Component 2"}
            )
            fig.update_layout(height=440, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            fig = px.scatter(
                df,
                x="annual_income",
                y="total_balance",
                color="segment_name",
                size="price_sensitivity",
                hover_data=["customer_id", "name", "credit_score"],
                color_discrete_sequence=["#6366f1", "#06b6d4", "#f59e0b", "#10b981", "#ec4899"],
                labels={"annual_income": "Annual Income ($)", "total_balance": "Total Deposit Balance ($)"}
            )
            fig.update_layout(height=440, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
    with col_archetypes:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">🎯 Behavioral Archetype Profiles</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select an archetype to inspect value drivers and objection patterns.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        selected_seg_name = st.selectbox("Inspect Archetype", seg_summary_df["name"].tolist())
        seg_data = seg_summary_df[seg_summary_df["name"] == selected_seg_name].iloc[0]
        
        st.markdown(
            f"""
            <div class="glass-container" style="background: rgba(17, 24, 39, 0.85); padding: 1.25rem;">
                <div style="font-size: 2rem; margin-bottom: 0.25rem;">{seg_data['icon']}</div>
                <h4 style="margin: 0; color: #67e8f9; font-size: 1.1rem;">{seg_data['name']}</h4>
                <p style="color: #94a3b8; font-size: 0.88rem; margin: 0.35rem 0 1rem 0;">{seg_data['description']}</p>
                
                <h5 style="margin: 0 0 0.35rem 0; color: #6ee7b7; font-size: 0.88rem;">💎 Key Value Drivers:</h5>
                <ul style="margin: 0 0 0.85rem 0; padding-left: 1.2rem; color: #f8fafc; font-size: 0.83rem; line-height: 1.5;">
                    {"".join([f'<li>{d}</li>' for d in seg_data['key_value_drivers']])}
                </ul>
                
                <h5 style="margin: 0 0 0.35rem 0; color: #fda4af; font-size: 0.88rem;">⚠️ Dominant Objections:</h5>
                <ul style="margin: 0; padding-left: 1.2rem; color: #f8fafc; font-size: 0.83rem; line-height: 1.5;">
                    {"".join([f'<li>{o}</li>' for o in seg_data['primary_objections']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
