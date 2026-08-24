import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

SEGMENT_ARCHETYPES = {
    0: {
        "name": "Affluent Tech-Forward Optimizers",
        "description": "High-income, digitally active professionals seeking high yields, automated portfolio tools, and zero friction.",
        "icon": "⚡",
        "primary_objections": ["Hidden platform fees", "Clunky manual onboarding", "Slow digital execution"],
        "key_value_drivers": ["Instant mobile actions", "High APY cash sweeps", "Automated portfolio rebalancing"]
    },
    1: {
        "name": "Conservative Wealth Builders",
        "description": "Mature, risk-averse depositors focused on capital preservation, relationship banking, and retirement security.",
        "icon": "🏛️",
        "primary_objections": ["Market volatility risk", "Lack of direct human advisor access", "Overly complex tech"],
        "key_value_drivers": ["FDIC security guarantees", "Dedicated wealth manager", "Transparent fixed yields"]
    },
    2: {
        "name": "Price-Sensitive Digital Churners",
        "description": "Younger, high-mobility users with lower brand loyalty who quickly switch to competitors for promotional bonuses.",
        "icon": "🎯",
        "primary_objections": ["Monthly account maintenance fees", "High minimum balance thresholds", "Low promotional rates"],
        "key_value_drivers": ["Sign-up cash bonuses", "No-fee overdraft", "High cashback rewards"]
    },
    3: {
        "name": "Established Family Anchors",
        "description": "Multi-product households with mortgages, life insurance, and college savings valuing bundle discounts.",
        "icon": "🏡",
        "primary_objections": ["Fragmented account views", "High multi-policy rates", "Inflexible loan terms"],
        "key_value_drivers": ["Multi-product relationship discounts", "Family financial dashboards", "Low mortgage rates"]
    }
}

def run_customer_segmentation(df: pd.DataFrame, n_clusters: int = 4) -> tuple[pd.DataFrame, pd.DataFrame, PCA]:
    """Runs KMeans clustering and PCA dimensionality reduction on customer dataset."""
    feature_cols = [
        "age", "annual_income", "net_worth", "credit_score", "tenure_years",
        "product_count", "total_balance", "digital_engagement", "brand_loyalty",
        "price_sensitivity", "churn_risk"
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
            "avg_net_worth": round(c_df["net_worth"].mean(), 0),
            "avg_age": round(c_df["age"].mean(), 1),
            "avg_credit_score": round(c_df["credit_score"].mean(), 0),
            "avg_digital_engagement": round(c_df["digital_engagement"].mean(), 1),
            "avg_brand_loyalty": round(c_df["brand_loyalty"].mean(), 1),
            "avg_price_sensitivity": round(c_df["price_sensitivity"].mean(), 1),
            "avg_churn_risk": round(c_df["churn_risk"].mean(), 2),
            "primary_objections": arch["primary_objections"],
            "key_value_drivers": arch["key_value_drivers"]
        })
        
    summary_df = pd.DataFrame(segment_summaries)
    return df_clustered, summary_df, pca_3d
