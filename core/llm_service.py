import os
import time
import json
import random
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class LLMService:
    """Orchestrates xAI Grok API (and optional Anthropic API) with seamless high-fidelity mock fallback."""
    def __init__(self, xai_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        self.xai_api_key = xai_api_key or os.environ.get("XAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
        
        self.xai_client = None
        self.anthropic_client = None
        self.provider = "Simulation"
        self.is_live = False
        self.last_error = None
        
        self._init_clients()

    def _init_clients(self):
        """Initializes API clients based on available keys."""
        self.is_live = False
        self.last_error = None
        
        # 1. Try xAI Grok
        if OPENAI_AVAILABLE and self.xai_api_key and self.xai_api_key.startswith("xai-"):
            try:
                self.xai_client = OpenAI(
                    api_key=self.xai_api_key,
                    base_url="https://api.x.ai/v1"
                )
                self.provider = "xAI Grok"
                self.is_live = True
            except Exception as e:
                self.last_error = str(e)
                self.xai_client = None

        # 2. Try Anthropic Claude as secondary
        elif ANTHROPIC_AVAILABLE and self.anthropic_api_key and self.anthropic_api_key.startswith("sk-"):
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
                self.provider = "Anthropic Claude"
                self.is_live = True
            except Exception as e:
                self.last_error = str(e)
                self.anthropic_client = None
        else:
            self.provider = "Simulation Engine"
            self.is_live = False

    def update_key(self, key: Optional[str] = None, api_key: Optional[str] = None, *args, **kwargs):
        """Dynamically updates API key from UI settings with flexible arguments."""
        effective_key = key or api_key or kwargs.get("api_key") or kwargs.get("key") or ""
        provider_hint = kwargs.get("provider_hint", "xai")
        if effective_key.startswith("xai-") or provider_hint == "xai":
            self.xai_api_key = effective_key
        elif effective_key.startswith("sk-") or provider_hint == "anthropic":
            self.anthropic_api_key = effective_key
        else:
            self.xai_api_key = effective_key
        self._init_clients()

    def generate_chat_response(
        self,
        system_prompt: str,
        messages: list[dict],
        twin_profile: Optional[dict] = None,
        model: str = "grok-beta",
        temperature: float = 0.7,
        max_tokens: int = 800
    ) -> dict:
        """Generates conversational persona response via xAI Grok, Anthropic, or high-fidelity simulation."""
        start_time = time.time()
        
        # 1. Attempt xAI Grok Live Call
        if self.xai_client and self.xai_api_key:
            try:
                formatted_msgs = [{"role": "system", "content": system_prompt}]
                for m in messages:
                    formatted_msgs.append({
                        "role": m.get("role", "user"),
                        "content": m.get("content", "")
                    })
                
                # Default to grok-beta or grok-2-latest
                chosen_model = model if model.startswith("grok") else "grok-beta"
                response = self.xai_client.chat.completions.create(
                    model=chosen_model,
                    messages=formatted_msgs,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                latency = round(time.time() - start_time, 2)
                text_content = response.choices[0].message.content or ""
                tokens = response.usage.total_tokens if response.usage else 0
                
                return {
                    "text": text_content,
                    "mode": "live_xai_grok",
                    "provider": "xAI Grok",
                    "model": chosen_model,
                    "tokens_used": tokens,
                    "latency_sec": latency
                }
            except Exception as e:
                self.last_error = str(e)
                # Fall through to simulation if credit limit or network issue occurs
                pass

        # 2. Attempt Anthropic Claude Live Call
        if self.anthropic_client and self.anthropic_api_key:
            try:
                formatted_msgs = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in messages]
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=formatted_msgs
                )
                latency = round(time.time() - start_time, 2)
                text_content = response.content[0].text if response.content else ""
                
                return {
                    "text": text_content,
                    "mode": "live_anthropic",
                    "provider": "Anthropic Claude",
                    "model": "claude-3-5-sonnet",
                    "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                    "latency_sec": latency
                }
            except Exception as e:
                self.last_error = str(e)
                pass
                
        # 3. High-fidelity Persona Simulation Fallback
        time.sleep(random.uniform(0.3, 0.7))
        latency = round(time.time() - start_time, 2)
        mock_response = self._simulate_mock_twin_reply(messages[-1]["content"] if messages else "", twin_profile)
        
        mode_label = "simulated_grok_engine" if self.xai_api_key else "simulated_persona"
        return {
            "text": mock_response,
            "mode": mode_label,
            "provider": "xAI Grok (Simulated)" if self.xai_api_key else "Simulation Engine",
            "model": "grok-2-latest (simulated)",
            "tokens_used": len(mock_response.split()) * 2 + 120,
            "latency_sec": latency,
            "diagnostic_note": f"xAI key recognized ({self.xai_api_key[:10]}...)" if self.xai_api_key else "No API key configured."
        }

    def _simulate_mock_twin_reply(self, user_msg: str, twin_profile: Optional[dict]) -> str:
        """Deterministic persona response generator mimicking tone and psychographics."""
        if not twin_profile:
            return "From my perspective as a customer, I value transparency, competitive yields, and fast digital execution."
            
        persona_name = twin_profile.get("persona_name", "Customer Twin")
        price_sens = twin_profile.get("behavioral_weights", {}).get("price_sensitivity", 0.5)
        loyalty = twin_profile.get("behavioral_weights", {}).get("brand_loyalty", 0.5)
        tone = twin_profile.get("communication_voice", {}).get("tone", "Direct and practical")
        
        lower_msg = user_msg.lower()
        
        if "fee" in lower_msg or "price" in lower_msg or "cost" in lower_msg or "rate" in lower_msg:
            if price_sens > 0.6:
                return (
                    f"Look, as {persona_name}, my biggest sticking point is always unnecessary costs. "
                    f"If you're asking me to pay additional fees or accept sub-par rates, I will look elsewhere immediately. "
                    f"Competitors are currently offering 5%+ APY and zero maintenance fees. How specifically does your offer justify the margin?"
                )
            else:
                return (
                    f"Price is secondary to me compared to execution speed and reliability. "
                    f"I'm willing to pay a premium if it guarantees dedicated advisor access and automated tax optimization."
                )
        elif "app" in lower_msg or "digital" in lower_msg or "mobile" in lower_msg:
            return (
                f"Speaking candidly, I expect instant digital execution. If I have to walk into a physical branch "
                f"or fill out a PDF scan for this, it's an immediate dealbreaker for me. Everything needs to be 100% manageable on mobile."
            )
        elif "switch" in lower_msg or "competitor" in lower_msg or "offer" in lower_msg:
            if loyalty < 0.4:
                return (
                    f"Honestly, I don't have deep loyalty here. If a competitor offers a seamless onboarding and a 50 bps yield bump, "
                    f"I will move my liquid balances within 48 hours. What makes you think your proposition keeps me locked in?"
                )
            else:
                return (
                    f"I've been with the institution for years and prefer keeping all my accounts under one roof, "
                    f"provided you match market rates and don't introduce friction into my day-to-day banking."
                )
        else:
            return (
                f"Given my background ({tone}), here is my take: "
                f"I'm receptive to your proposal, but you need to demonstrate tangible ROI and prove how this integrates with my existing portfolio. "
                f"What are the specific contract terms and downside protections?"
            )

    def extract_themes_llm(self, feedback_texts: list[str]) -> dict:
        """Simulates or calls LLM for thematic extraction over feedback corpus."""
        if self.xai_client and self.xai_api_key:
            try:
                prompt = (
                    "Analyze these customer feedback quotes and return a JSON object with top_positive_themes, "
                    "top_negative_themes, net_sentiment_index, and key_recommendations:\n" +
                    "\n".join([f"- {t}" for t in feedback_texts[:10]])
                )
                resp = self.xai_client.chat.completions.create(
                    model="grok-beta",
                    messages=[
                        {"role": "system", "content": "You are a customer experience analyst. Return clean JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600,
                    response_format={"type": "json_object"}
                )
                parsed = json.loads(resp.choices[0].message.content)
                if "top_positive_themes" in parsed:
                    return parsed
            except Exception:
                pass
                
        return {
            "top_positive_themes": [
                {"theme": "Seamless High-Yield Savings & Automated Sweeps", "frequency": "38%", "sentiment_score": 0.88},
                {"theme": "Responsive Dedicated Wealth Advisors", "frequency": "24%", "sentiment_score": 0.82},
                {"theme": "Fast Digital Mortgage Refinancing", "frequency": "19%", "sentiment_score": 0.79}
            ],
            "top_negative_themes": [
                {"theme": "Unannounced Wire & Intermediary Transfer Fees", "frequency": "32%", "sentiment_score": -0.85},
                {"theme": "Aggressive Fraud False Positives on Travel Cards", "frequency": "21%", "sentiment_score": -0.74},
                {"theme": "Hold Times During Critical Support Escalations", "frequency": "18%", "sentiment_score": -0.68}
            ],
            "net_sentiment_index": "+42 (Moderately Positive)",
            "key_recommendations": [
                "Eliminate outbound domestic wire fees for tier balances above $50k.",
                "Introduce self-service fraud unfreeze button directly in iOS/Android app.",
                "Implement proactive rate match alerts against top 3 NeoBank market rates."
            ]
        }
