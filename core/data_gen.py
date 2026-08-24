import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

PRODUCT_CATALOG = [
    "Platinum Checking",
    "High-Yield Savings (4.75% APY)",
    "Index Growth Investment Account",
    "Fixed-Rate 30Y Mortgage",
    "Comprehensive Auto Policy",
    "Term Life Coverage ($500k)",
    "Private Wealth Advisory",
    "Cashback Elite Credit Card"
]

OCCUPATIONS = [
    "Senior Software Engineer",
    "Small Business Owner",
    "Healthcare Director",
    "Marketing Strategist",
    "Financial Consultant",
    "Retired Civil Servant",
    "University Professor",
    "Freelance Creative Director",
    "Operations Manager",
    "Real Estate Agent"
]

CITIES = [
    ("New York", "NY"), ("San Francisco", "CA"), ("Austin", "TX"),
    ("Seattle", "WA"), ("Chicago", "IL"), ("Miami", "FL"),
    ("Boston", "MA"), ("Denver", "CO"), ("Atlanta", "GA")
]

FEEDBACK_SNIPPETS_POOL = [
    "The mobile app transfer is lightning fast, but I hate the wire transfer fees.",
    "Very pleased with the wealth advisor check-in, though portfolio rebalancing took two days too long.",
    "Why was my card flagged for fraud when buying gas in my hometown? Support took 45 minutes on hold.",
    "Great interest rate on high-yield savings. Would recommend to friends.",
    "The mortgage refinancing process was smooth and entirely digital, huge plus.",
    "Your competitor offers 5.25% APY without minimum deposit requirements. Seriously considering switching.",
    "Received an unsolicited promotional email despite opting out. Privacy settings need fixing.",
    "The automated budget insights helped me track monthly expenses accurately.",
    "Customer service rep Sarah was knowledgeable and resolved my dispute in 5 minutes.",
    "Hidden international transaction fee of 3% on travel card is unacceptable."
]

def generate_synthetic_customers(n: int = 150) -> pd.DataFrame:
    """Generates realistic synthetic banking/insurance customer demographic & behavioral records."""
    customers = []
    
    for i in range(n):
        cust_id = f"CUST-{10000 + i}"
        gender = random.choice(["Female", "Male", "Non-Binary"])
        first_name = fake.first_name_female() if gender == "Female" else fake.first_name_male()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
        phone = f"+1 ({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"
        city, state = random.choice(CITIES)
        
        age = int(np.random.normal(44, 14))
        age = max(22, min(78, age))
        
        occupation = random.choice(OCCUPATIONS)
        tenure_years = round(random.uniform(0.5, 18.0), 1)
        
        # Financial Profile
        if age < 30:
            income = int(np.random.normal(85000, 25000))
            net_worth = int(income * random.uniform(0.5, 2.5))
            credit_score = int(np.random.normal(710, 45))
        elif age < 55:
            income = int(np.random.normal(145000, 45000))
            net_worth = int(income * random.uniform(2.0, 7.0))
            credit_score = int(np.random.normal(765, 40))
        else:
            income = int(np.random.normal(120000, 40000))
            net_worth = int(income * random.uniform(4.0, 12.0))
            credit_score = int(np.random.normal(790, 30))
            
        income = max(38000, income)
        net_worth = max(15000, net_worth)
        credit_score = max(580, min(850, credit_score))
        
        # Product Holdings
        num_products = min(len(PRODUCT_CATALOG), max(1, int(np.random.poisson(3.2))))
        products_held = random.sample(PRODUCT_CATALOG, num_products)
        
        total_balance = round(net_worth * random.uniform(0.15, 0.45), 2)
        monthly_spend = round(income * random.uniform(0.20, 0.45) / 12, 2)
        
        # Behavioral & Risk Metrics
        digital_engagement = int(np.random.normal(70 if age < 45 else 48, 18))
        digital_engagement = max(10, min(99, digital_engagement))
        
        brand_loyalty = int(np.random.normal(7.2 if tenure_years > 5 else 5.5, 1.8))
        brand_loyalty = max(1, min(10, brand_loyalty))
        
        price_sensitivity = int(np.random.normal(5.0 if income > 120000 else 7.5, 1.9))
        price_sensitivity = max(1, min(10, price_sensitivity))
        
        risk_appetite = random.choices(
            ["Conservative", "Moderate-Growth", "Aggressive"],
            weights=[0.35, 0.45, 0.20] if age > 50 else [0.15, 0.50, 0.35]
        )[0]
        
        churn_risk = round(max(0.02, min(0.95, (price_sensitivity * 0.08) + ((10 - brand_loyalty) * 0.05) - (tenure_years * 0.015) + (0.1 if digital_engagement < 30 else -0.05))), 2)
        
        # Privacy & Consent
        consent_marketing = random.random() > 0.15
        consent_profiling = random.random() > 0.10
        consent_third_party = random.random() > 0.70
        pii_masked = True
        
        # Feedback Quotes
        feedbacks = random.sample(FEEDBACK_SNIPPETS_POOL, k=random.randint(1, 3))
        
        customers.append({
            "customer_id": cust_id,
            "name": full_name,
            "email": email,
            "phone": phone,
            "age": age,
            "gender": gender,
            "city": city,
            "state": state,
            "occupation": occupation,
            "tenure_years": tenure_years,
            "annual_income": income,
            "net_worth": net_worth,
            "credit_score": credit_score,
            "products_held": products_held,
            "product_count": len(products_held),
            "total_balance": total_balance,
            "monthly_spend": monthly_spend,
            "digital_engagement": digital_engagement,
            "brand_loyalty": brand_loyalty,
            "price_sensitivity": price_sensitivity,
            "risk_appetite": risk_appetite,
            "churn_risk": churn_risk,
            "consent_marketing": consent_marketing,
            "consent_profiling": consent_profiling,
            "consent_third_party": consent_third_party,
            "pii_masked": pii_masked,
            "feedback_history": feedbacks,
            "segment_id": None,
            "segment_name": None
        })
        
    return pd.DataFrame(customers)

def generate_evidence_documents(customers_df: pd.DataFrame) -> list:
    """Generates realistic interaction transcripts, contracts, and claims for RAG evidence."""
    docs = []
    doc_types = [
        "Support Interaction Transcript",
        "Policy Contract & Rider",
        "Quarterly Financial Review",
        "Complaint Resolution Note",
        "Mobile App Feedback Survey"
    ]
    
    for _, row in customers_df.iterrows():
        cust_id = row["customer_id"]
        name = row["name"]
        
        # Generate 2-4 documents per customer
        num_docs = random.randint(2, 4)
        for d in range(num_docs):
            dtype = random.choice(doc_types)
            doc_id = f"DOC-{cust_id}-{d+1}"
            date_str = (datetime.now() - timedelta(days=random.randint(5, 360))).strftime("%Y-%m-%d")
            
            if dtype == "Support Interaction Transcript":
                title = f"Support Call: Inquiry regarding {random.choice(row['products_held'])}"
                sentiment = random.choice(["Neutral", "Positive", "Frustrated"])
                content = (
                    f"Customer {name} ({cust_id}) contacted representative regarding {random.choice(row['products_held'])}. "
                    f"Customer expressed: '{random.choice(row['feedback_history'])}'. "
                    f"Agent verified identity, reviewed balance of ${row['total_balance']:,.2f}, and noted customer sensitivity to fees (Score: {row['price_sensitivity']}/10)."
                )
            elif dtype == "Policy Contract & Rider":
                title = f"Official Terms: {random.choice(row['products_held'])} Schedule"
                sentiment = "Neutral"
                content = (
                    f"Account Contract Reference {cust_id}-P. Holder: {name}. Products bound: {', '.join(row['products_held'])}. "
                    f"Standard FDIC / SIPC limits apply. Churn propensity index currently logged at {row['churn_risk']*100:.1f}%. "
                    f"Special Terms: Tiered interest calculation on total balance above $50,000 threshold with zero maintenance fees."
                )
            elif dtype == "Quarterly Financial Review":
                title = f"Advisor Notes: Annual Portfolio & Risk Audit ({date_str})"
                sentiment = "Positive"
                content = (
                    f"Advisor consultation with {name}. Primary objective: wealth preservation and tax efficiency. "
                    f"Current Net Worth logged at ${row['net_worth']:,.2f}. Risk Appetite: {row['risk_appetite']}. "
                    f"Recommended allocating 15% to index fixed income and exploring automated mortgage rate refinance."
                )
            elif dtype == "Complaint Resolution Note":
                title = "Escalated Service Ticket Resolution Summary"
                sentiment = "Negative"
                content = (
                    f"Case escalated to Senior Ops. Customer {name} reported dissatisfaction with digital app outage during travel. "
                    f"Offered $50 goodwill fee credit and verified two-factor authentication token settings. Customer accepted resolution."
                )
            else:
                title = "CSAT / NPS Pulse Survey Submission"
                sentiment = "Positive" if row["brand_loyalty"] >= 7 else "Negative"
                content = (
                    f"NPS rating provided: {row['brand_loyalty']}/10. Customer Comment: '{random.choice(row['feedback_history'])}'. "
                    f"Tenure with firm: {row['tenure_years']} years. Location: {row['city']}, {row['state']}."
                )
                
            docs.append({
                "doc_id": doc_id,
                "customer_id": cust_id,
                "customer_name": name,
                "doc_type": dtype,
                "title": title,
                "date": date_str,
                "sentiment": sentiment,
                "content": content
            })
            
    return docs

def generate_market_signals() -> list:
    """Generates realistic external market and competitor signals."""
    return [
        {
            "signal_id": "MKT-2026-01",
            "category": "Competitor Disruption",
            "title": "Fintech NeoBank launches 5.50% APY 'Zero-Fee' Cash Account",
            "impact": "Elevated churn risk for high-balance, price-sensitive digital users.",
            "date": "2026-08-10"
        },
        {
            "signal_id": "MKT-2026-02",
            "category": "Macro Interest Rates",
            "title": "Federal Reserve signals 25 bps rate pause amid steady inflation",
            "impact": "Mortgage refinance demand stabilizes; fixed-income interest yields peak.",
            "date": "2026-08-18"
        },
        {
            "signal_id": "MKT-2026-03",
            "category": "Regulatory & Privacy",
            "title": "CFPB Finalizes Open Banking Rule 1033 on Customer Financial Data Rights",
            "impact": "Mandates instant frictionless third-party data portability and strict consent audit trails.",
            "date": "2026-08-22"
        }
    ]
