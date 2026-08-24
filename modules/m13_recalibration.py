import streamlit as st
import time
from components.glass_card import render_banner, render_metric_card
from components.diff_viewer import render_version_diff_radar, render_diff_table

def render_stage_13():
    """Stage 13: Recalibration & Versioning."""
    render_banner(
        title="Stage 13: Twin Recalibration & Model Versioning",
        description="Lifecycle version control and continuous behavioral tuning. Adjust psychographic weights based on validation feedback, publish new twin versions (v1.0 → v2.0), and inspect parameter drift.",
        icon="🔄",
        accent_color="indigo"
    )
    
    twin_store = st.session_state.twin_store
    
    twin_keys = [k for k in twin_store.keys() if k.startswith("TWIN-")]
    
    # Top Stats
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Registered Versions", "v1.0 & v2.0 Active", "SemVer Tracked", "positive")
    with s2:
        render_metric_card("Recalibration Events", f"{len(st.session_state.get('recalibration_logs', []))}", "Audit Logged", "neutral")
    with s3:
        render_metric_card("Max Observed Drift", "+2.5 pts", "Price Sensitivity", "positive")
    with s4:
        render_metric_card("Model Rollback", "Available", "Instant 1-Click", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    col_tune, col_diff = st.columns([1.1, 1.9])
    
    with col_tune:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">⚙️ Behavioral Recalibration Studio</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select a twin to adjust parameters and create a new versioned release.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        selected_twin_id = st.selectbox(
            "Select Twin to Recalibrate",
            twin_keys,
            format_func=lambda tid: f"{twin_store[tid]['avatar_emoji']} {twin_store[tid]['persona_name']}"
        )
        twin = twin_store[selected_twin_id]
        
        current_weights = twin.get("behavioral_weights", {})
        
        st.markdown(f"**Current Active Version:** `{twin.get('version', 'v1.0')}`")
        
        new_price_sens = st.slider("Price Sensitivity Weight", 0.0, 1.0, float(current_weights.get("price_sensitivity", 0.5)), 0.05)
        new_loyalty = st.slider("Brand Loyalty Weight", 0.0, 1.0, float(current_weights.get("brand_loyalty", 0.5)), 0.05)
        new_tech = st.slider("Tech Adoption Weight", 0.0, 1.0, float(current_weights.get("tech_adoption", 0.5)), 0.05)
        new_risk = st.slider("Risk Tolerance Weight", 0.0, 1.0, float(current_weights.get("risk_tolerance", 0.5)), 0.05)
        new_skep = st.slider("Skepticism Weight", 0.0, 1.0, float(current_weights.get("skepticism", 0.5)), 0.05)
        
        recal_reason = st.text_input("Recalibration Changelog Note", "Adjusted for macro inflation and NeoBank competitive pressure.")
        target_version = st.selectbox("Target Version Tag", ["v1.1 (Patch)", "v2.0 (Major Release)", "v2.1 (Feature Update)"])
        
        if st.button("🚀 Publish Recalibrated Twin Version", type="primary", use_container_width=True):
            v_tag = target_version.split()[0]
            
            # Save baseline snapshot if not present
            if "baseline_snapshot" not in twin:
                import copy
                twin["baseline_snapshot"] = copy.deepcopy(twin)
                
            # Update active twin
            twin["version"] = v_tag
            twin["behavioral_weights"] = {
                "price_sensitivity": new_price_sens,
                "brand_loyalty": new_loyalty,
                "tech_adoption": new_tech,
                "risk_tolerance": new_risk,
                "skepticism": new_skep
            }
            
            twin["version_history"].append({
                "version": v_tag,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "notes": recal_reason
            })
            
            # Log in session
            st.session_state.recalibration_logs.append({
                "twin_id": selected_twin_id,
                "version": v_tag,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "reason": recal_reason
            })
            
            st.success(f"Published {selected_twin_id} as {v_tag} successfully!")
            st.rerun()
            
    with col_diff:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">📊 Parameter Drift & Visual Diff</h4>
                    <span class="glass-badge badge-cyan">Visual Diff Engine</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        baseline_profile = twin.get("baseline_snapshot", twin)
        active_profile = twin
        
        # Dual Radar Diff
        fig = render_version_diff_radar(
            baseline_profile.get("behavioral_weights", {}),
            active_profile.get("behavioral_weights", {}),
            v1_label=baseline_profile.get("version", "v1.0"),
            v2_label=active_profile.get("version", "v2.0")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### 🔍 Version Attribute Comparison")
        render_diff_table(baseline_profile, active_profile)
        
        st.markdown("#### 📜 Recalibration Audit Changelog")
        recal_logs = st.session_state.get("recalibration_logs", [])
        if recal_logs:
            st.dataframe(pd.DataFrame(recal_logs), use_container_width=True)
        else:
            st.info("No manual recalibration events logged yet.")
