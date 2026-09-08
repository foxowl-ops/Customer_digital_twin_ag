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
    "Comprehensive Auto Insurance",
    "Homeowners Insurance (HO-3)",
    "Renters Insurance",
    "Term Life Insurance ($500k)",
    "Umbrella Liability Policy ($1M)",
    "Business Owners Policy (BOP)",
    "Pet Insurance Plan",
    "Travel Insurance Plan"
]

OCCUPATIONS = [
    "Senior Software Engineer",
    "Small Business Owner",
    "Healthcare Director",
    "Marketing Strategist",
    "Insurance Claims Adjuster",
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

INDIAN_FIRST_NAMES_MALE = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Rohan", "Aryan", "Kabir", "Dhruv", "Vikram", "Rahul", "Amit", "Sanjay", "Rajesh", "Suresh",
    "Anand", "Deepak", "Manish", "Nikhil", "Pranav", "Karan", "Varun", "Siddharth", "Rakesh", "Ashok"
]

INDIAN_FIRST_NAMES_FEMALE = [
    "Saanvi", "Ananya", "Diya", "Aadhya", "Kavya", "Ira", "Myra", "Sara", "Anika", "Navya",
    "Priya", "Neha", "Pooja", "Sneha", "Divya", "Shreya", "Meera", "Kritika", "Riya", "Isha",
    "Lakshmi", "Deepika", "Anjali", "Swati", "Sunita", "Kavita", "Rekha", "Nisha", "Radhika", "Aditi"
]

INDIAN_LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Mehta", "Shah", "Patel", "Kumar", "Singh", "Rao", "Reddy",
    "Nair", "Menon", "Iyer", "Iyengar", "Pillai", "Chatterjee", "Banerjee", "Mukherjee", "Das", "Ghosh",
    "Kapoor", "Malhotra", "Chopra", "Khanna", "Bhatt", "Joshi", "Desai", "Agarwal", "Bose", "Pandey"
]

FEEDBACK_SNIPPETS_POOL = [
    "The mobile app claims filing is lightning fast, but I hate that my premium jumped 18% at renewal with no explanation.",
    "Very pleased with how my agent handled my homeowners claim, though the adjuster inspection took two days too long to schedule.",
    "Why was my auto claim flagged for review when I was clearly not at fault? Support took 45 minutes on hold.",
    "Great multi-policy bundle discount on my auto and home coverage. Would recommend to friends.",
    "The renters insurance sign-up process was smooth and entirely digital, huge plus.",
    "Your competitor offers 20% lower premiums with the same coverage limits. Seriously considering switching at renewal.",
    "Received an unsolicited promotional email despite opting out. Privacy settings need fixing.",
    "The automated coverage gap insights helped me realize I was underinsured on my umbrella policy.",
    "Claims rep Sarah was knowledgeable and resolved my dispute in 5 minutes.",
    "Hidden policy administration fee of 3% on my renewal is unacceptable."
]

def generate_synthetic_customers(n: int = 150) -> pd.DataFrame:
    """Generates realistic synthetic general insurance policyholder demographic & behavioral records."""
    customers = []

    for i in range(n):
        cust_id = f"CUST-{10000 + i}"
        gender = random.choice(["Female", "Male", "Non-Binary"])
        first_name = random.choice(INDIAN_FIRST_NAMES_FEMALE) if gender == "Female" else random.choice(INDIAN_FIRST_NAMES_MALE)
        last_name = random.choice(INDIAN_LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
        phone = f"+1 ({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"
        city, state = random.choice(CITIES)

        age = int(np.random.normal(44, 14))
        age = max(22, min(78, age))

        occupation = random.choice(OCCUPATIONS)
        tenure_years = round(random.uniform(0.5, 18.0), 1)

        # Financial & Insurability Profile
        if age < 30:
            income = int(np.random.normal(85000, 25000))
            insured_asset_value = int(income * random.uniform(0.5, 2.5))
            credit_score = int(np.random.normal(710, 45))
        elif age < 55:
            income = int(np.random.normal(145000, 45000))
            insured_asset_value = int(income * random.uniform(2.0, 7.0))
            credit_score = int(np.random.normal(765, 40))
        else:
            income = int(np.random.normal(120000, 40000))
            insured_asset_value = int(income * random.uniform(4.0, 12.0))
            credit_score = int(np.random.normal(790, 30))

        income = max(38000, income)
        insured_asset_value = max(15000, insured_asset_value)
        credit_score = max(580, min(850, credit_score))

        # Policy Holdings
        num_policies = min(len(PRODUCT_CATALOG), max(1, int(np.random.poisson(3.2))))
        policies_held = random.sample(PRODUCT_CATALOG, num_policies)

        annual_premium = round(insured_asset_value * random.uniform(0.010, 0.028), 2)
        monthly_premium = round(annual_premium / 12, 2)

        # Claims History
        num_claims_filed = int(np.random.poisson(0.6))
        num_claims_filed = max(0, min(6, num_claims_filed))
        if num_claims_filed == 0:
            last_claim_status = "No Claims Filed"
        else:
            last_claim_status = random.choices(
                ["Approved & Paid", "Under Review", "Denied", "Approved & Paid"],
                weights=[0.55, 0.20, 0.10, 0.15]
            )[0]

        # Behavioral & Risk Metrics
        digital_engagement = int(np.random.normal(70 if age < 45 else 48, 18))
        digital_engagement = max(10, min(99, digital_engagement))

        brand_loyalty = int(np.random.normal(7.2 if tenure_years > 5 else 5.5, 1.8))
        brand_loyalty = max(1, min(10, brand_loyalty))

        price_sensitivity = int(np.random.normal(5.0 if income > 120000 else 7.5, 1.9))
        price_sensitivity = max(1, min(10, price_sensitivity))

        risk_profile = random.choices(
            ["Risk-Averse", "Balanced", "High-Risk"],
            weights=[0.35, 0.45, 0.20] if age > 50 else [0.15, 0.50, 0.35]
        )[0]

        lapse_risk = round(max(0.02, min(0.95, (price_sensitivity * 0.08) + ((10 - brand_loyalty) * 0.05) - (tenure_years * 0.015) + (0.06 * num_claims_filed) + (0.1 if digital_engagement < 30 else -0.05))), 2)

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
            "insured_asset_value": insured_asset_value,
            "credit_score": credit_score,
            "policies_held": policies_held,
            "policy_count": len(policies_held),
            "annual_premium": annual_premium,
            "monthly_premium": monthly_premium,
            "num_claims_filed": num_claims_filed,
            "last_claim_status": last_claim_status,
            "digital_engagement": digital_engagement,
            "brand_loyalty": brand_loyalty,
            "price_sensitivity": price_sensitivity,
            "risk_profile": risk_profile,
            "lapse_risk": lapse_risk,
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
    """Generates realistic interaction transcripts, policy contracts, and claims records for RAG evidence."""
    docs = []
    doc_types = [
        "Support Interaction Transcript",
        "Policy Contract & Rider",
        "Policy Renewal & Coverage Review",
        "Complaint Resolution Note",
        "Claims Satisfaction Survey"
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
                title = f"Support Call: Inquiry regarding {random.choice(row['policies_held'])}"
                sentiment = random.choice(["Neutral", "Positive", "Frustrated"])
                content = (
                    f"Customer {name} ({cust_id}) contacted representative regarding {random.choice(row['policies_held'])}. "
                    f"Customer expressed: '{random.choice(row['feedback_history'])}'. "
                    f"Agent verified identity, reviewed annual premium of ${row['annual_premium']:,.2f}, and noted customer sensitivity to premium changes (Score: {row['price_sensitivity']}/10)."
                )
            elif dtype == "Policy Contract & Rider":
                title = f"Official Terms: {random.choice(row['policies_held'])} Schedule"
                sentiment = "Neutral"
                content = (
                    f"Policy Contract Reference {cust_id}-P. Policyholder: {name}. Policies bound: {', '.join(row['policies_held'])}. "
                    f"Standard state guaranty association limits apply. Lapse propensity index currently logged at {row['lapse_risk']*100:.1f}%. "
                    f"Special Terms: Multi-policy bundle discount applies when 2+ policies are held, with deductible tiers based on insured asset value above $50,000 threshold."
                )
            elif dtype == "Policy Renewal & Coverage Review":
                title = f"Agent Notes: Annual Coverage & Risk Audit ({date_str})"
                sentiment = "Positive"
                content = (
                    f"Agent consultation with {name}. Primary objective: coverage adequacy and claims protection. "
                    f"Current Insured Asset Value logged at ${row['insured_asset_value']:,.2f}. Risk Profile: {row['risk_profile']}. Claims on file: {row['num_claims_filed']} ({row['last_claim_status']}). "
                    f"Recommended raising umbrella liability limits and exploring bundled auto + home renewal discount."
                )
            elif dtype == "Complaint Resolution Note":
                title = "Escalated Service Ticket Resolution Summary"
                sentiment = "Negative"
                content = (
                    f"Case escalated to Senior Claims Ops. Customer {name} reported dissatisfaction with delayed claims adjuster response during a covered loss event. "
                    f"Offered $50 goodwill service credit and verified two-factor authentication token settings on the policyholder portal. Customer accepted resolution."
                )
            else:
                title = "Claims / CSAT Pulse Survey Submission"
                sentiment = "Positive" if row["brand_loyalty"] >= 7 else "Negative"
                content = (
                    f"CSAT rating provided: {row['brand_loyalty']}/10. Customer Comment: '{random.choice(row['feedback_history'])}'. "
                    f"Tenure with carrier: {row['tenure_years']} years. Location: {row['city']}, {row['state']}."
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
    """Generates realistic external market, catastrophe, and regulatory signals for the insurance line of business."""
    return [
        {
            "signal_id": "MKT-2026-01",
            "category": "Competitor Disruption",
            "title": "InsurTech challenger launches AI-underwritten auto bundle with 20% lower premiums",
            "impact": "Elevated lapse risk for high-premium, price-sensitive digital policyholders.",
            "date": "2026-08-10"
        },
        {
            "signal_id": "MKT-2026-02",
            "category": "Catastrophe & Weather Risk",
            "title": "NOAA forecasts above-average hurricane season impacting coastal homeowners book",
            "impact": "Homeowners renewal premiums expected to rise; reinsurance costs pass through to policyholders.",
            "date": "2026-08-18"
        },
        {
            "signal_id": "MKT-2026-03",
            "category": "Regulatory & Privacy",
            "title": "State Insurance Dept. finalizes Rule 1033 on Policyholder Data Portability Rights",
            "impact": "Mandates instant frictionless third-party data portability and strict consent audit trails.",
            "date": "2026-08-22"
        }
    ]
