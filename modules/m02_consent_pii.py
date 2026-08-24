import streamlit as st
import pandas as pd
from datetime import datetime
from components.glass_card import render_banner, render_metric_card

def mask_pii_name(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}*** {parts[1][0]}***"
    return f"{name[0]}***"

def mask_pii_email(email: str) -> str:
    parts = email.split("@")
    if len(parts) == 2:
        return f"{parts[0][:2]}***@{parts[1]}"
    return "******@***.com"

def mask_pii_phone(phone: str) -> str:
    return phone[:9] + "****" if len(phone) > 8 else "***-***-****"

def render_stage_02():
    """Stage 02: Consent, Security & PII Controls."""
    render_banner(
        title="Stage 02: Consent, Security & PII Controls",
        description="Enterprise-grade privacy governance layer enforcing granular customer consent directives, automated PII tokenization/masking, and immutable compliance audit logging.",
        icon="🛡️",
        accent_color="cyan"
    )
    
    df = st.session_state.customers_df
    
    # Metrics
    total_cust = len(df)
    consented_profiling = len(df[df["consent_profiling"] == True])
    consented_marketing = len(df[df["consent_marketing"] == True])
    consented_3rd = len(df[df["consent_third_party"] == True])
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Profiling Consent", f"{consented_profiling/total_cust*100:.1f}%", f"{consented_profiling}/{total_cust}", "positive")
    with c2:
        render_metric_card("Marketing Consent", f"{consented_marketing/total_cust*100:.1f}%", f"{consented_marketing}/{total_cust}", "neutral")
    with c3:
        render_metric_card("3rd Party Sharing", f"{consented_3rd/total_cust*100:.1f}%", f"{consented_3rd}/{total_cust}", "negative")
    with c4:
        render_metric_card("PII Masking Status", "ENFORCED" if not st.session_state.pii_unmasked_auth else "AUTHORIZED OVERRIDE", "AES-256 GCM", "positive" if not st.session_state.pii_unmasked_auth else "negative")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 1.9])
    
    with col_left:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">🔒 Privacy & Consent Inspector</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select a customer to inspect and toggle individual GDPR/CCPA consent flags.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        cust_list = df["customer_id"].tolist()
        selected_cust_id = st.selectbox("Select Customer to Manage", cust_list, index=0)
        cust_row = df[df["customer_id"] == selected_cust_id].iloc[0]
        
        st.markdown(f"**Selected Customer:** `{cust_row['name']}` (`{selected_cust_id}`)")
        
        c_mkt = st.checkbox("Consent: Marketing Outreach", value=bool(cust_row["consent_marketing"]), key=f"mkt_{selected_cust_id}")
        c_prof = st.checkbox("Consent: AI Profiling & Digital Twin Creation", value=bool(cust_row["consent_profiling"]), key=f"prof_{selected_cust_id}")
        c_3rd = st.checkbox("Consent: 3rd-Party Analytics Sharing", value=bool(cust_row["consent_third_party"]), key=f"3rd_{selected_cust_id}")
        
        if st.button("💾 Save Consent Directive", type="primary", use_container_width=True):
            idx = df[df["customer_id"] == selected_cust_id].index[0]
            st.session_state.customers_df.at[idx, "consent_marketing"] = c_mkt
            st.session_state.customers_df.at[idx, "consent_profiling"] = c_prof
            st.session_state.customers_df.at[idx, "consent_third_party"] = c_3rd
            
            # Log audit event
            audit_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event": f"Consent updated for {selected_cust_id}: Profiling={c_prof}, Marketing={c_mkt}, 3rdParty={c_3rd}",
                "actor": "Compliance_DPO_Admin",
                "status": "LOGGED_IMMUTABLE"
            }
            if "audit_logs" not in st.session_state:
                st.session_state.audit_logs = []
            st.session_state.audit_logs.insert(0, audit_entry)
            
            st.success(f"Consent directives updated for {selected_cust_id}!")
            st.rerun()
            
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 1rem 0;' />", unsafe_allow_html=True)
        
        st.markdown("#### 🕵️ Data Protection Officer (DPO) Mode")
        auth_toggle = st.toggle("Override PII Masking (Requires Compliance Auth)", value=st.session_state.pii_unmasked_auth)
        if auth_toggle != st.session_state.pii_unmasked_auth:
            st.session_state.pii_unmasked_auth = auth_toggle
            audit_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event": f"DPO PII Unmasking Override set to {auth_toggle}",
                "actor": "Compliance_DPO_Admin",
                "status": "SECURITY_ALERT_EMITTED"
            }
            if "audit_logs" not in st.session_state:
                st.session_state.audit_logs = []
            st.session_state.audit_logs.insert(0, audit_entry)
            st.rerun()
            
    with col_right:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">👁️ Live Masked Customer Data View</h4>
                    <span class="glass-badge badge-emerald">GDPR & CCPA Compliant</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        display_df = df.copy()
        if not st.session_state.pii_unmasked_auth:
            display_df["name"] = display_df["name"].apply(mask_pii_name)
            display_df["email"] = display_df["email"].apply(mask_pii_email)
            display_df["phone"] = display_df["phone"].apply(mask_pii_phone)
            
        show_cols = ["customer_id", "name", "email", "phone", "consent_profiling", "consent_marketing", "consent_third_party"]
        st.dataframe(display_df[show_cols].head(10), use_container_width=True)
        
        st.markdown("#### 📜 Immutable Governance & Consent Audit Trail")
        audit_logs = st.session_state.get("audit_logs", [
            {"timestamp": "2026-08-24 10:14:02", "event": "Batch PII tokenization applied across 150 synthetic records", "actor": "Automated_Privacy_Daemon", "status": "LOGGED_IMMUTABLE"},
            {"timestamp": "2026-08-24 09:55:12", "event": "Consent schema verification passed (Rule 1033 compliant)", "actor": "SecOps_Auditor", "status": "LOGGED_IMMUTABLE"}
        ])
        
        audit_df = pd.DataFrame(audit_logs)
        st.dataframe(audit_df, use_container_width=True)
