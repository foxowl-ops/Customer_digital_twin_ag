import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

SEGMENT_ARCHETYPES = {
    0: {
        "name": "Digitally-Savvy Bundlers",
        "description": "High-income, digitally active policyholders who bundle multiple lines, file claims via app, and expect zero-friction self-service.",
        "icon": "⚡",
        "primary_objections": ["Hidden policy fees", "Clunky manual claims intake", "Slow digital quote turnaround"],
        "key_value_drivers": ["Instant mobile claims filing", "Multi-policy bundle discounts", "Automated coverage gap alerts"]
    },
    1: {
        "name": "Risk-Averse Coverage Planners",
        "description": "Mature, risk-averse policyholders focused on maximizing coverage adequacy, agent relationships, and long-term protection.",
        "icon": "🛡️",
        "primary_objections": ["Coverage gaps at renewal", "Lack of direct human agent access", "Overly complex policy tech"],
        "key_value_drivers": ["Guaranteed claims payout track record", "Dedicated agent relationship", "Transparent premium schedules"]
    },
    2: {
        "name": "Premium-Sensitive Switchers",
        "description": "Younger, high-mobility policyholders with lower brand loyalty who quickly switch carriers for promotional premium discounts.",
        "icon": "🎯",
        "primary_objections": ["Rising renewal premiums", "High deductible requirements", "Low promotional discount depth"],
        "key_value_drivers": ["Sign-up premium discounts", "No-penalty policy switching", "Usage-based discount programs"]
    },
    3: {
        "name": "Multi-Policy Family Households",
        "description": "Multi-policy households with auto, home, and life coverage valuing bundle discounts and family protection.",
        "icon": "🏡",
        "primary_objections": ["Fragmented policy views", "High multi-policy premium rates", "Inflexible rider terms"],
        "key_value_drivers": ["Multi-policy bundle discounts", "Family coverage dashboards", "Low umbrella liability add-on rates"]
    }
}

def run_customer_segmentation(df: pd.DataFrame, n_clusters: int = 4) -> tuple[pd.DataFrame, pd.DataFrame, PCA]:
    """Runs KMeans clustering and PCA dimensionality reduction on the policyholder dataset."""
    feature_cols = [
        "age", "annual_income", "insured_asset_value", "credit_score", "tenure_years",
        "policy_count", "annual_premium", "digital_engagement", "brand_loyalty",
        "price_sensitivity", "lapse_risk"
    ]

    X = df[feature_cols].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # 2D and 3D PCA for visualization
    pca_3d = PCA(n_components=3, random_state=42)
    pca_coords = pca_3d.fit_transform(X_scaled)

    df_clustered = df.copy()
    df_clustered["cluster"] = clusters
    df_clustered["pca_x"] = pca_coords[:, 0]
    df_clustered["pca_y"] = pca_coords[:, 1]
    df_clustered["pca_z"] = pca_coords[:, 2]

    # Map Archetype metadata
    df_clustered["segment_id"] = [f"SEG-{c+1:02d}" for c in clusters]
    df_clustered["segment_name"] = [SEGMENT_ARCHETYPES.get(c, {}).get("name", f"Segment {c}") for c in clusters]
    df_clustered["segment_icon"] = [SEGMENT_ARCHETYPES.get(c, {}).get("icon", "👤") for c in clusters]

    # Compute aggregate segment profiles
    segment_summaries = []
    for c in range(n_clusters):
        c_df = df_clustered[df_clustered["cluster"] == c]
        arch = SEGMENT_ARCHETYPES.get(c, {
            "name": f"Segment {c}", "description": "", "icon": "👤",
            "primary_objections": [], "key_value_drivers": []
        })

        segment_summaries.append({
            "cluster_id": c,
            "segment_id": f"SEG-{c+1:02d}",
            "name": arch["name"],
            "icon": arch["icon"],
            "description": arch["description"],
            "size": len(c_df),
            "share_pct": round(len(c_df) / len(df_clustered) * 100, 1),
            "avg_income": round(c_df["annual_income"].mean(), 0),
            "avg_insured_asset_value": round(c_df["insured_asset_value"].mean(), 0),
            "avg_age": round(c_df["age"].mean(), 1),
            "avg_credit_score": round(c_df["credit_score"].mean(), 0),
            "avg_digital_engagement": round(c_df["digital_engagement"].mean(), 1),
            "avg_brand_loyalty": round(c_df["brand_loyalty"].mean(), 1),
            "avg_price_sensitivity": round(c_df["price_sensitivity"].mean(), 1),
            "avg_lapse_risk": round(c_df["lapse_risk"].mean(), 2),
            "primary_objections": arch["primary_objections"],
            "key_value_drivers": arch["key_value_drivers"]
        })

    summary_df = pd.DataFrame(segment_summaries)
    return df_clustered, summary_df, pca_3d
