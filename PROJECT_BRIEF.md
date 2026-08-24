# Project Brief: Generative AI "Digital Twin of a Customer"

## Last Updated
2026-08-24 23:24 UTC — Integrated xAI Grok API (`XAI_API_KEY`) as the primary generative AI provider for Digital Twin persona reasoning, synthetic focus groups, thematic extraction, and sales role-play with graceful fallback handling.

## Vision
An end-to-end interactive Streamlit prototype demonstrating a Generative AI "Digital Twin of a Customer" platform. The application simulates the ingestion of customer/market data, governance controls, segmentation, and sentiment analysis to build behavioral digital twins that power synthetic focus groups, competitor reaction experiments, and interactive sales role-play with built-in human validation, RAG grounding, and profile versioning.

## Architecture Overview
The platform maps directly to a 13-stage reference architecture:

| Stage # | Pipeline Layer / Module | Description | Status |
|---|---|---|---|
| **01** | **Data Ingestion Layer** | Synthetic customer demographics, transactions, holdings, and market signals generator | Done |
| **02** | **Consent, Security & PII Controls** | Interactive consent toggling, dynamic PII masking/redaction, and simulated audit logs | Done |
| **03** | **CDP / Lakehouse Explorer** | Unified customer profile explorer, query filters, and data catalog | Done |
| **04** | **Segmentation Models** | Unsupervised ML clustering (K-Means/PCA) with interactive 2D/3D Plotly visualizers | Done |
| **05** | **Text & Theme Analysis** | xAI Grok-driven theme & sentiment extraction across surveys, reviews, and transcripts | Done |
| **06** | **Twin Profile Store** | Structured Digital Twin repository with persona behavioral vectors, holdings, and version tags | Done |
| **07** | **Evidence Retrieval / Knowledge Base** | In-memory RAG layer indexing policy docs, interaction transcripts, and market signals | Done |
| **08** | **LLM & Orchestration Layer** | Persona prompt synthesis engine combining twin profile + retrieved evidence + scenario via xAI Grok | Done |
| **09** | **Synthetic Focus Groups** | Multi-twin interactive panel running qualitative feedback on product, pricing, and messaging | Done |
| **10** | **Competitor Experiments** | Side-by-side simulation of customer reaction, willingness-to-pay, and churn risk | Done |
| **11** | **Sales Role-Play & Battlecards** | Real-time interactive pitch simulator with realistic twin objections and auto-generated battlecard | Done |
| **12** | **Human Validation & Monitoring** | Review & governance queue for approving, flagging, and scoring twin responses | Done |
| **13** | **Recalibration & Versioning** | Version history timeline (v1.0 → v2.1) with visual diff of profile traits and behavioral weights | Done |

## Tech Stack
- **Framework & UI**: Streamlit (Python 3.10+) with single-page application router and custom CSS injection.
- **Design System**: Liquid Glass / Glassmorphism UI (CSS3 with backdrop blur, glowing gradients, dark mode palette, custom HTML components).
- **LLM Orchestration**: xAI Grok API (`openai` client targeting `https://api.x.ai/v1` with `grok-2` / `grok-beta`) and optional Anthropic Claude fallback.
- **Synthetic Data Generation**: `faker`, `numpy`, `pandas` for realistic banking/insurance/wealth customer profiles and interactions.
- **Machine Learning**: `scikit-learn` for customer segmentation (K-Means, PCA, standard scaling).
- **Visualizations**: `plotly` (express & graph_objects) with custom dark glassmorphic themes.
- **Information Retrieval (RAG)**: In-memory vector search with cosine similarity over document embeddings / TF-IDF for rapid evidence retrieval.
- **State Management**: Centralized `st.session_state` store preserving dataset updates, twin versions, focus group history, and role-play transcripts.

## File Structure
```
Customer_digital_twin_ag/
├── app.py                     # Main Streamlit application entry point & stepper router
├── PROJECT_BRIEF.md           # Single source of truth project brief (this file)
├── requirements.txt           # Project dependencies (streamlit, openai, anthropic, pandas, etc.)
├── .env                       # Environment configuration with XAI_API_KEY
├── .env.example               # Template for API keys
├── core/                      # Core backend utilities and engines
│   ├── __init__.py
│   ├── state.py               # Session state initialization and persistence
│   ├── data_gen.py            # Faker-based synthetic data generator (demographics, transactions, docs)
│   ├── ml_segmentation.py     # Feature engineering, clustering, and persona archetype extraction
│   ├── rag_engine.py          # Document vectorizer, chunking, and similarity retriever
│   └── llm_service.py         # xAI Grok API client wrapper + mock fallback engine
├── styles/                    # Visual styling and glassmorphism engine
│   ├── __init__.py
│   ├── theme.py               # Theme constants, palette definitions, and CSS injector
│   └── liquid_glass.css       # Custom CSS for frosted glass cards, glow effects, gradients
├── prompts/                   # Structured prompt templates
│   ├── __init__.py
│   ├── persona_prompts.py     # Twin persona system prompt builder
│   ├── theme_prompts.py       # Sentiment & theme extraction prompts
│   ├── focus_group_prompts.py # Panel moderation and twin response prompts
│   ├── roleplay_prompts.py    # Objection generator and sales battlecard evaluator
│   └── validation_prompts.py  # Compliance and hallucination checking prompts
├── components/                # Reusable UI component renderers
│   ├── __init__.py
│   ├── glass_card.py          # Frosted glass card, metric badge, and alert container components
│   ├── stepper.py             # Visual 13-stage pipeline navigation stepper
│   ├── twin_card.py           # Digital Twin persona profile card with radar traits
│   ├── diff_viewer.py         # Visual comparison widget for twin versions
│   └── battlecard_view.py     # Sales battlecard layout component
└── modules/                   # 13 pipeline stage view modules
    ├── __init__.py
    ├── m01_ingestion.py       # Stage 1: Data Ingestion Layer
    ├── m02_consent_pii.py     # Stage 2: Consent, Security & PII Controls
    ├── m03_lakehouse.py       # Stage 3: Customer Data Platform / Lakehouse
    ├── m04_segmentation.py    # Stage 4: Segmentation Models
    ├── m05_theme_analysis.py  # Stage 5: Text & Theme Analysis
    ├── m06_twin_store.py      # Stage 6: Twin Profile Store
    ├── m07_knowledge_base.py  # Stage 7: Evidence Retrieval / Knowledge Base
    ├── m08_orchestration.py   # Stage 8: LLM & Twin Orchestration Layer
    ├── m09_focus_groups.py    # Stage 9: Synthetic Focus Groups
    ├── m10_competitor_sim.py  # Stage 10: Competitor Experiments
    ├── m11_sales_roleplay.py  # Stage 11: Sales Role-Play & Battlecards
    ├── m12_validation.py      # Stage 12: Human Validation & Monitoring
    └── m13_recalibration.py   # Stage 13: Recalibration & Versioning
```

## Data Model
1. **Customer Record (`CustomerRecord`)**:
   - Demographics: `customer_id`, `name`, `age`, `gender`, `occupation`, `annual_income`, `net_worth`, `location`, `tenure_years`.
   - Financial Holdings: `products` (Checking, High-Yield Savings, Mortgages, Wealth Management, Auto Insurance, Term Life), `credit_score`, `total_balance`, `monthly_spend`.
   - Behavioral & Risk: `digital_engagement_score` (1-100), `brand_loyalty` (High/Med/Low), `risk_appetite` (Conservative/Moderate/Aggressive), `price_sensitivity` (1-10), `churn_risk_score` (0.0-1.0).
   - Governance & Privacy: `consent_marketing` (bool), `consent_profiling` (bool), `consent_third_party` (bool), `pii_masked` (bool), `last_consent_audit` (timestamp).
   - Unstructured Interactions: `feedback_snippets` (list of NPS/complaint/survey quotes).

2. **Segment Archetype (`SegmentArchetype`)**:
   - `segment_id`, `name` (e.g., *Affluent Tech-Forward Optimizers*, *Conservative Wealth Builders*, *Price-Sensitive Digital Churners*, *Established Family Anchors*).
   - `cluster_id`, `avg_income`, `avg_net_worth`, `avg_price_sensitivity`, `avg_brand_loyalty`, `primary_objections`, `key_value_drivers`, `size`, `share_pct`.

3. **Digital Twin Profile (`DigitalTwinProfile`)**:
   - `twin_id`, `customer_ref_id`, `segment_id`, `version` (`v1.0`, `v1.1`, `v2.0`).
   - `persona_name`, `avatar_emoji`, `headline`.
   - `demographics`, `psychographics`, `behavioral_weights`, `communication_voice`, `system_prompt_blueprint`, `version_history`.

4. **Evidence Document (`EvidenceDocument`)**:
   - `doc_id`, `customer_id`, `customer_name`, `doc_type`, `title`, `content`, `date`, `sentiment`, `similarity_score`.

5. **Focus Group & Roleplay Sessions (`SimulationSession`)**:
   - `session_id`, `topic` / `product_pitch_type`, `transcript` of turns, `consensus`, `recommendations`.
   - `validation_status`: `PENDING_REVIEW` | `APPROVED` | `FLAGGED_REVISE` | `REJECTED`.

## Design System
- **Theme**: Dark Liquid Glass / Modern Obsidian Glassmorphism
- **Background**: Multi-point animated CSS gradient mesh (`linear-gradient(145deg, #070a12 0%, #0c111d 50%, #090d16 100%)` with radial accent orbs `#6366f1` and `#06b6d4`).
- **Glass Cards**: Translucent cards with `backdrop-filter: blur(16px)`, `border: 1px solid rgba(255, 255, 255, 0.08)`, `border-radius: 16px`.
- **Typography**: Clean modern sans-serif stack (`Plus Jakarta Sans`).

## Completed Features
- Configured xAI Grok API integration with `XAI_API_KEY` across `.env`, `.env.example`, `core/llm_service.py`, `app.py`, and relevant pipeline stages.
- Supported seamless multi-provider fallback (Grok -> Claude -> High-Fidelity Persona Simulation).
- Verified live key registration and simulation response generation.

## Changelog
- **2026-08-24 23:24**: Integrated xAI Grok API key (`XAI_API_KEY`) and updated LLM orchestration service to use Grok-2 / Grok-beta.
- **2026-08-24 23:16**: Completed full end-to-end implementation of all 13 pipeline modules, Liquid Glass design system, and browser automated verification.
- **2026-08-24 23:00**: Initial project brief created.
