import streamlit as st
import pandas as pd
from core.data_gen import generate_synthetic_customers, generate_evidence_documents, generate_market_signals
from core.ml_segmentation import run_customer_segmentation
from core.rag_engine import InMemoryRAGEngine
from core.llm_service import LLMService

def build_default_twin_profile(cust_row: pd.Series, version: str = "v1.0") -> dict:
    """Constructs a structured DigitalTwinProfile record from a customer row."""
    cust_id = cust_row["customer_id"]
    name = cust_row["name"]
    seg_name = cust_row.get("segment_name", "General Depositor")
    seg_id = cust_row.get("segment_id", "SEG-01")
    
    price_sens = float(cust_row["price_sensitivity"]) / 10.0
    brand_loyalty = float(cust_row["brand_loyalty"]) / 10.0
    tech_adopt = float(cust_row["digital_engagement"]) / 100.0
    risk_appetite = cust_row["risk_appetite"]
    risk_weight = 0.8 if risk_appetite == "Aggressive" else (0.5 if risk_appetite == "Moderate-Growth" else 0.2)
    
    avatar = "⚡" if "Tech" in seg_name else ("🏛️" if "Conservative" in seg_name else ("🎯" if "Price" in seg_name else "🏡"))
    
    system_prompt = f"""You are acting as the Generative Digital Twin of {name} ({cust_id}).
You are a real customer with the following persona profile:
- Age: {cust_row['age']}, Occupation: {cust_row['occupation']}, Location: {cust_row['city']}, {cust_row['state']}
- Annual Income: ${cust_row['annual_income']:,}, Net Worth: ${cust_row['net_worth']:,}, Balance: ${cust_row['total_balance']:,}
- Customer Segment: {seg_name} ({seg_id})
- Product Holdings: {', '.join(cust_row['products_held'])}
- Behavioral Traits: Price Sensitivity = {price_sens*10:.0f}/10, Brand Loyalty = {brand_loyalty*10:.0f}/10, Tech Adoption = {tech_adopt*10:.0f}/10, Risk Appetite = {risk_appetite}
- Past Customer Sentiment: '{cust_row['feedback_history'][0] if cust_row['feedback_history'] else 'Generally satisfied'}'

Respond in the first person ('I', 'me', 'my'). Speak authentically from this customer's financial posture and behavioral tendencies. Do not break character.
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
        "headline": f"{cust_row['occupation']} • {cust_row['age']} y/o • ${cust_row['total_balance']:,.0f} balance",
        "demographics": {
            "age": cust_row["age"],
            "gender": cust_row["gender"],
            "occupation": cust_row["occupation"],
            "city": cust_row["city"],
            "state": cust_row["state"],
            "tenure_years": cust_row["tenure_years"],
            "annual_income": cust_row["annual_income"],
            "net_worth": cust_row["net_worth"],
            "credit_score": cust_row["credit_score"]
        },
        "holdings": cust_row["products_held"],
        "behavioral_weights": {
            "price_sensitivity": price_sens,
            "brand_loyalty": brand_loyalty,
            "tech_adoption": tech_adopt,
            "risk_tolerance": risk_weight,
            "skepticism": round(1.0 - brand_loyalty, 2)
        },
        "psychographics": {
            "decision_style": "Data & Yield Focused" if price_sens > 0.6 else "Relationship & Trust Focused",
            "financial_goals": ["Wealth Preservation", "Yield Maximization"] if risk_weight < 0.5 else ["Aggressive Capital Growth", "Tax Efficiency"],
            "pain_points": ["Hidden transfer fees", "Unnecessary branch visits", "Slow resolution times"],
            "dealbreakers": ["Sudden unnotified rate cuts", "Poor data privacy controls"]
        },
        "communication_voice": {
            "tone": "Analytical, direct, asks for exact fee schedules and terms" if price_sens > 0.5 else "Polite, values relationship continuity and security",
            "preferred_channel": "Mobile App & Secure Chat" if tech_adopt > 0.6 else "Phone & In-person Advisor"
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
