import streamlit as st
import pandas as pd
from core.data_gen import generate_synthetic_customers, generate_evidence_documents, generate_market_signals
from core.ml_segmentation import run_customer_segmentation
from core.rag_engine import InMemoryRAGEngine
from core.llm_service import LLMService
from core.currency import format_inr

def build_default_twin_profile(cust_row: pd.Series, version: str = "v1.0") -> dict:
    """Constructs a structured DigitalTwinProfile record from a policyholder row."""
    cust_id = cust_row["customer_id"]
    name = cust_row["name"]
    seg_name = cust_row.get("segment_name", "General Policyholder")
    seg_id = cust_row.get("segment_id", "SEG-01")

    price_sens = float(cust_row["price_sensitivity"]) / 10.0
    brand_loyalty = float(cust_row["brand_loyalty"]) / 10.0
    tech_adopt = float(cust_row["digital_engagement"]) / 100.0
    risk_profile = cust_row["risk_profile"]
    risk_weight = 0.8 if risk_profile == "High-Risk" else (0.5 if risk_profile == "Balanced" else 0.2)

    avatar = "⚡" if "Digitally-Savvy" in seg_name else ("🛡️" if "Risk-Averse" in seg_name else ("🎯" if "Premium-Sensitive" in seg_name else "🏡"))

    system_prompt = f"""You are acting as the Generative Digital Twin of {name} ({cust_id}).
You are a real policyholder with the following persona profile:
- Age: {cust_row['age']}, Occupation: {cust_row['occupation']}, Location: {cust_row['city']}, {cust_row['state']}
- Annual Income: {format_inr(cust_row['annual_income'])}, Insured Asset Value: {format_inr(cust_row['insured_asset_value'])}, Annual Premium: {format_inr(cust_row['annual_premium'])}
- Customer Segment: {seg_name} ({seg_id})
- Policy Holdings: {', '.join(cust_row['policies_held'])}
- Claims History: {cust_row['num_claims_filed']} claims filed ({cust_row['last_claim_status']})
- Behavioral Traits: Price Sensitivity = {price_sens*10:.0f}/10, Brand Loyalty = {brand_loyalty*10:.0f}/10, Tech Adoption = {tech_adopt*10:.0f}/10, Risk Profile = {risk_profile}
- Past Customer Sentiment: '{cust_row['feedback_history'][0] if cust_row['feedback_history'] else 'Generally satisfied'}'

Respond in the first person ('I', 'me', 'my'). Speak authentically from this policyholder's insurance posture and behavioral tendencies. Do not break character.
"""

    return {
        "twin_id": f"TWIN-{cust_id}",
        "customer_ref_id": cust_id,
        "customer_name": name,
        "segment_id": seg_id,
        "segment_name": seg_name,
        "version": version,
        "avatar_emoji": avatar,
        "persona_name": f"{name} ({seg_name})",
        "headline": f"{cust_row['occupation']} • {cust_row['age']} y/o • {format_inr(cust_row['annual_premium'])}/yr premium",
        "demographics": {
            "age": cust_row["age"],
            "gender": cust_row["gender"],
            "occupation": cust_row["occupation"],
            "city": cust_row["city"],
            "state": cust_row["state"],
            "tenure_years": cust_row["tenure_years"],
            "annual_income": cust_row["annual_income"],
            "insured_asset_value": cust_row["insured_asset_value"],
            "credit_score": cust_row["credit_score"],
            "num_claims_filed": cust_row["num_claims_filed"],
            "last_claim_status": cust_row["last_claim_status"]
        },
        "holdings": cust_row["policies_held"],
        "behavioral_weights": {
            "price_sensitivity": price_sens,
            "brand_loyalty": brand_loyalty,
            "tech_adoption": tech_adopt,
            "risk_tolerance": risk_weight,
            "skepticism": round(1.0 - brand_loyalty, 2)
        },
        "psychographics": {
            "decision_style": "Data & Discount Focused" if price_sens > 0.6 else "Relationship & Trust Focused",
            "financial_goals": ["Coverage Adequacy", "Claims Protection"] if risk_weight < 0.5 else ["Broad Liability Protection", "Premium Optimization"],
            "pain_points": ["Hidden policy fees", "Unnecessary in-branch paperwork", "Slow claims resolution times"],
            "dealbreakers": ["Sudden unnotified premium hikes", "Poor data privacy controls"]
        },
        "communication_voice": {
            "tone": "Analytical, direct, asks for exact premium and deductible schedules" if price_sens > 0.5 else "Polite, values relationship continuity and security",
            "preferred_channel": "Mobile App & Secure Chat" if tech_adopt > 0.6 else "Phone & In-person Agent"
        },
        "system_prompt_blueprint": system_prompt,
        "version_history": [
            {
                "version": version,
                "timestamp": "2026-08-24 10:00:00",
                "notes": "Initial automated twin synthesis from Lakehouse & Segmentation model."
            }
        ]
    }

def init_session_state():
    """Initializes all state variables in st.session_state if not already present."""
    if "data_initialized" not in st.session_state:
        # Generate initial synthetic customer records
        customers_df = generate_synthetic_customers(150)
        
        # Run segmentation
        clustered_df, seg_summary_df, _ = run_customer_segmentation(customers_df, n_clusters=4)
        
        # Generate evidence documents
        evidence_docs = generate_evidence_documents(clustered_df)
        
        # Build RAG engine
        rag = InMemoryRAGEngine()
        rag.index_documents(evidence_docs)
        
        # Generate digital twins
        twin_store = {}
        for _, row in clustered_df.iterrows():
            twin = build_default_twin_profile(row, version="v1.0")
            twin_store[twin["twin_id"]] = twin
            twin_store[row["customer_id"]] = twin
            
        # Store in session state
        st.session_state.customers_df = clustered_df
        st.session_state.seg_summary_df = seg_summary_df
        st.session_state.evidence_docs = evidence_docs
        st.session_state.market_signals = generate_market_signals()
        st.session_state.twin_store = twin_store
        st.session_state.rag_engine = rag
        st.session_state.llm_service = LLMService()
        
        # History & Governance
        st.session_state.focus_group_history = []
        st.session_state.roleplay_history = []
        st.session_state.validation_queue = []
        st.session_state.recalibration_logs = []
        st.session_state.pii_unmasked_auth = False
        st.session_state.current_stage_idx = 0
        st.session_state.data_initialized = True
    else:
        # Hot-reload safety: ensure llm_service has the latest class methods and attributes
        if "llm_service" not in st.session_state or not hasattr(st.session_state.llm_service, "xai_client"):
            st.session_state.llm_service = LLMService()
