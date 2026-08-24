"""Theme extraction and text sentiment prompt templates."""

THEME_EXTRACTION_SYSTEM_PROMPT = """You are an advanced Customer Experience & Market Intelligence Analyst.
Analyze the provided batch of customer feedback, survey responses, and support transcripts.

Return a structured JSON object with the following schema:
{
    "top_positive_themes": [
        {"theme": "Theme Name", "frequency": "XX%", "sentiment_score": 0.85, "sample_quote": "..."}
    ],
    "top_negative_themes": [
        {"theme": "Theme Name", "frequency": "XX%", "sentiment_score": -0.78, "sample_quote": "..."}
    ],
    "net_sentiment_index": "+XX (Classification)",
    "key_drivers_of_churn": ["...", "..."],
    "actionable_recommendations": ["...", "...", "..."]
}
"""

def format_theme_analysis_user_prompt(feedback_snippets: list[str]) -> str:
    feed_text = "\n".join([f"- {f}" for f in feedback_snippets])
    return f"""Please perform thematic clustering and sentiment extraction on the following raw customer quotes:

{feed_text}
"""
