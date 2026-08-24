import streamlit as st
import pandas as pd
from components.glass_card import render_banner, render_metric_card

def render_stage_12():
    """Stage 12: Human Validation & Monitoring."""
    render_banner(
        title="Stage 12: Human Validation & Compliance Governance",
        description="Human-in-the-loop (HITL) audit workbench. Review, score, annotate, and approve synthetic twin outputs for persona fidelity, regulatory compliance, and factual alignment.",
        icon="⚖️",
        accent_color="amber"
    )
    
    queue = st.session_state.validation_queue
    
    # Pre-populate sample items if empty
    if not queue:
        st.session_state.validation_queue = [
            {
                "id": "VAL-FG-001",
                "type": "Synthetic Focus Group",
                "target": "Platinum Wealth Subscription ($25/mo)",
                "status": "APPROVED",
                "score": 5,
                "timestamp": "2026-08-24 10:30:15",
                "reviewer": "Sarah_Compliance_Officer",
                "notes": "Verified authentic representation of price-sensitive objections without regulatory breach.",
                "flags": ["None"]
            },
            {
                "id": "VAL-RP-002",
                "type": "Sales Role-Play",
                "target": "Sarah Jenkins - Wealth Advisory",
                "status": "PENDING_REVIEW",
                "score": None,
                "timestamp": "2026-08-24 11:15:40",
                "reviewer": None,
                "notes": "",
                "flags": []
            }
        ]
        queue = st.session_state.validation_queue
        
    approved_count = len([q for q in queue if q.get("status") == "APPROVED"])
    pending_count = len([q for q in queue if q.get("status") == "PENDING_REVIEW"])
    flagged_count = len([q for q in queue if q.get("status") in ["FLAGGED_REVISE", "REJECTED"]])
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Pending Reviews", f"{pending_count}", "Awaiting Governance", "neutral" if pending_count == 0 else "negative")
    with m2:
        render_metric_card("Approved Simulations", f"{approved_count}", "Governance Certified", "positive")
    with m3:
        render_metric_card("Flagged for Revision", f"{flagged_count}", "Requires Calibration", "negative" if flagged_count > 0 else "positive")
    with m4:
        render_metric_card("Governance SLA", "99.8%", "Sub-2h Turnaround", "positive")
        
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    col_q, col_audit = st.columns([1.1, 1.9])
    
    with col_q:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">📋 Governance Audit Queue</h4>
                <p style="color: #94a3b8; font-size: 0.85rem;">Select an item to inspect reasoning trace and record compliance approval.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        item_ids = [item["id"] for item in queue]
        selected_id = st.selectbox("Select Audit Record", item_ids, index=0)
        selected_item = next((item for item in queue if item["id"] == selected_id), queue[0])
        
        status_color = "emerald" if selected_item.get("status") == "APPROVED" else ("amber" if selected_item.get("status") == "PENDING_REVIEW" else "rose")
        
        st.markdown(
            f"""
            <div style="background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 0.85rem; font-size: 0.83rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="color: #67e8f9;">{selected_item['id']}</strong>
                    <span class="glass-badge badge-{status_color}">{selected_item.get('status')}</span>
                </div>
                <div style="color: #cbd5e1;"><strong>Type:</strong> {selected_item.get('type')}</div>
                <div style="color: #cbd5e1;"><strong>Target:</strong> {selected_item.get('target')}</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-top: 0.3rem;">Logged: {selected_item.get('timestamp')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("#### ✍️ Human Validator Assessment")
        eval_score = st.slider("Persona Authenticity & Alignment Rating", 1, 5, selected_item.get("score") or 4)
        flags = st.multiselect("Compliance / Quality Flags", [
            "Excessive Sycophancy / Generic Tone",
            "Disregard of High Price Sensitivity Weight",
            "Unauthorized Financial Advice Risk",
            "Hallucinated Contract Terms",
            "None / Flawless Execution"
        ], default=selected_item.get("flags") or ["None / Flawless Execution"])
        
        eval_notes = st.text_area("Auditor Review Comments", value=selected_item.get("notes") or "", height=80)
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("✅ Approve Output", type="primary", use_container_width=True):
                selected_item["status"] = "APPROVED"
                selected_item["score"] = eval_score
                selected_item["flags"] = flags
                selected_item["notes"] = eval_notes
                selected_item["reviewer"] = "Compliance_Lead"
                st.success(f"{selected_id} approved!")
                st.rerun()
        with c_btn2:
            if st.button("🚩 Flag for Revision", use_container_width=True):
                selected_item["status"] = "FLAGGED_REVISE"
                selected_item["score"] = eval_score
                selected_item["flags"] = flags
                selected_item["notes"] = eval_notes
                selected_item["reviewer"] = "Compliance_Lead"
                st.warning(f"{selected_id} flagged for recalibration!")
                st.rerun()
                
    with col_audit:
        st.markdown(
            """
            <div class="glass-container">
                <div class="glass-header-glow"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">🔍 Simulation Trace & Evidence Inspector</h4>
                    <span class="glass-badge badge-indigo">Audit Record Details</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        details = selected_item.get("details", {})
        if details:
            st.json(details)
        else:
            st.markdown(
                f"""
                <div class="glass-container" style="background: rgba(17, 24, 39, 0.5);">
                    <h5 style="margin: 0 0 0.5rem 0; color: #67e8f9;">Recorded Audit Context</h5>
                    <p style="color: #cbd5e1; font-size: 0.88rem;"><strong>Simulation Target:</strong> {selected_item.get('target')}</p>
                    <p style="color: #cbd5e1; font-size: 0.88rem;"><strong>Current Status:</strong> {selected_item.get('status')}</p>
                    <p style="color: #cbd5e1; font-size: 0.88rem;"><strong>Reviewer:</strong> {selected_item.get('reviewer') or 'Unassigned'}</p>
                    <p style="color: #cbd5e1; font-size: 0.88rem;"><strong>Notes:</strong> {selected_item.get('notes') or 'No notes logged yet.'}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("#### 📜 Full Governance Master Ledger")
        summary_rows = []
        for q in queue:
            summary_rows.append({
                "ID": q.get("id"),
                "Type": q.get("type"),
                "Target": q.get("target"),
                "Status": q.get("status"),
                "Score": f"{q.get('score')}/5" if q.get("score") else "Pending",
                "Reviewer": q.get("reviewer") or "Unassigned"
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
