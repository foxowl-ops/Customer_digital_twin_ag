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
        mock_response = self._simulate_mock_twin_reply(messages, twin_profile)
        
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

    def _pick_variant(self, twin_profile: Optional[dict], category: str, variants: list) -> str:
        """Rotates through a category's reply variants so the twin never says the exact same
        line twice in a row. State is stashed on the twin's own profile dict, which is a
        persistent object living in st.session_state.twin_store, so it survives across the
        Streamlit reruns that happen between each chat turn."""
        if len(variants) == 1:
            return variants[0]
        if twin_profile is None:
            return random.choice(variants)
        state = twin_profile.setdefault("_sim_reply_state", {})
        last_idx = state.get(category, -1)
        choices = [i for i in range(len(variants)) if i != last_idx] or list(range(len(variants)))
        idx = random.choice(choices)
        state[category] = idx
        return variants[idx]

    def _simulate_mock_twin_reply(self, messages: list, twin_profile: Optional[dict]) -> str:
        """Context-aware persona response generator mimicking tone and psychographics.

        Looks at the whole conversation so far (not just the latest line) so it can
        acknowledge information the rep already provided, track how many turns have
        passed, and rotate between several phrasings per intent category instead of
        returning one fixed string per keyword match.
        """
        if not twin_profile:
            return "From my perspective as a policyholder, I value transparency, fair premiums, and fast digital claims handling."

        user_msg = messages[-1].get("content", "") if messages else ""
        lower_msg = user_msg.lower()
        turn_index = sum(1 for m in messages if m.get("role") == "assistant")

        persona_name = twin_profile.get("customer_name") or twin_profile.get("persona_name", "Customer Twin")
        price_sens = twin_profile.get("behavioral_weights", {}).get("price_sensitivity", 0.5)
        loyalty = twin_profile.get("behavioral_weights", {}).get("brand_loyalty", 0.5)
        tone = twin_profile.get("communication_voice", {}).get("tone", "Direct and practical")

        if any(k in lower_msg for k in ["mailed", "emailed", "sent you", "sent over", "sent the", "attached", "here are", "here's the", "shared the", "provided the"]):
            variants = [
                f"Got it, thanks for sending that over — let me be direct though: paperwork doesn't close the deal on its own. "
                f"What's the actual premium difference versus my current setup, and what's excluded that I'd need to know about?",
                f"Appreciate you following up with the documentation. Before I sign off, walk me through the claims turnaround time — "
                f"that's the part that actually matters to me as {persona_name}.",
                f"Okay, I'll take a look at what you sent. In the meantime, tell me plainly: is there a cancellation penalty if this doesn't work out for me?",
                f"Thanks. One thing the paperwork never makes clear — how does this bundle actually behave the first time I file a claim?",
            ]
            return self._pick_variant(twin_profile, "provides_info", variants)

        if any(k in lower_msg for k in ["fee", "price", "cost", "premium", "deductible", "expensive", "afford"]):
            if price_sens > 0.6:
                variants = [
                    f"Look, as {persona_name}, my biggest sticking point is always unnecessary costs. "
                    f"If you're asking me to pay a higher premium or accept a worse deductible, I will look elsewhere immediately. "
                    f"Competitors are currently offering 20% lower premiums with the same coverage limits. How specifically does your offer justify the margin?",
                    f"Before we go further — what's the actual dollar number? I've been burned by 'value' pitches that turn out to cost more than what I have now.",
                    f"I need the premium and deductible spelled out plainly, not bundled into a vague 'package value.' Can you give me the real numbers?",
                ]
            else:
                variants = [
                    f"Price is secondary to me compared to claims turnaround and coverage reliability. "
                    f"I'm willing to pay a premium if it guarantees dedicated agent access and fast claims payout.",
                    f"I'm not overly fixated on the premium itself — I care more about whether you'll actually be there when I need to file a claim.",
                    f"Cost matters, but not as much as knowing this coverage will hold up. Convince me on reliability first.",
                ]
            return self._pick_variant(twin_profile, "price", variants)

        if any(k in lower_msg for k in ["app", "digital", "mobile", "claim", "online", "portal"]):
            variants = [
                f"Speaking candidly, I expect instant digital claims filing. If I have to walk into a physical branch "
                f"or fax paperwork for this, it's an immediate dealbreaker for me. Everything needs to be 100% manageable on mobile.",
                f"How does the claims app actually work day-to-day? I don't want a marketing answer — walk me through filing a real claim.",
                f"Digital-first is table stakes for me at this point. What happens if the app goes down mid-claim — is there a fallback?",
            ]
            return self._pick_variant(twin_profile, "digital", variants)

        if any(k in lower_msg for k in ["switch", "competitor", "another carrier", "elsewhere"]):
            if loyalty < 0.4:
                variants = [
                    f"Honestly, I don't have deep loyalty here. If a competitor offers a seamless quote and a meaningful premium discount, "
                    f"I will switch carriers at my next renewal. What makes you think your proposition keeps me locked in?",
                    f"I've switched carriers before and I'll do it again if the math doesn't work. What's actually different about you?",
                ]
            else:
                variants = [
                    f"I've been with the carrier for years and prefer keeping all my policies bundled under one roof, "
                    f"provided you match market premiums and don't introduce friction into claims handling.",
                    f"I'm not eager to switch, but I do expect you to earn that loyalty back with a fair renewal price.",
                ]
            return self._pick_variant(twin_profile, "switch", variants)

        if turn_index == 0 and any(k in lower_msg for k in ["hi", "hello", "hey", "pitch", "offer you", "introduce", "wanted to discuss", "want to pitch", "recommend", "propose", "bundle"]):
            variants = [
                f"Given my background ({tone}), here is my take: "
                f"I'm receptive to your proposal, but you need to demonstrate tangible coverage value and prove how this integrates with my existing policies. "
                f"What are the specific policy terms, exclusions, and claims turnaround guarantees?",
                f"Alright, I'm listening — but I'll be upfront as {persona_name}: I've heard a lot of bundle pitches before. "
                f"What specifically makes this worth changing anything about my current coverage?",
                f"Sure, go ahead. Before you get into details, though — how is this actually different from what I already have?",
            ]
            return self._pick_variant(twin_profile, "opening", variants)

        # Generic fallback for anything else, with a natural progression as the
        # conversation goes on longer instead of repeating the same line forever.
        if turn_index >= 3:
            variants = [
                f"We've covered a fair amount now. If the numbers and claims process check out the way you've described, "
                f"I'm leaning toward saying yes — but send me the final terms in writing before I commit.",
                f"Okay, I think I've got what I need to make a decision. What would it take to lock in these terms today?",
                f"I'm cautiously on board at this point, {tone.split(',')[0].lower()} as I am — what's the next step to actually get this started?",
            ]
            return self._pick_variant(twin_profile, "closing", variants)

        variants = [
            f"Given my background ({tone}), here is my take: I'm receptive, but you still haven't addressed my main concern — "
            f"what happens to my current coverage during the transition?",
            f"That's fair, but I need more specifics before I can react to it. What exactly changes for me day-to-day?",
            f"I hear you, but as {persona_name} I tend to need proof, not promises. Can you give me a concrete example?",
            f"Okay — and what's the catch? There's usually a catch with offers like this.",
        ]
        return self._pick_variant(twin_profile, "general", variants)

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
                {"theme": "Seamless Mobile Claims Filing & Status Tracking", "frequency": "38%", "sentiment_score": 0.88},
                {"theme": "Responsive Dedicated Insurance Agents", "frequency": "24%", "sentiment_score": 0.82},
                {"theme": "Fast Digital Policy Bundling & Renewal", "frequency": "19%", "sentiment_score": 0.79}
            ],
            "top_negative_themes": [
                {"theme": "Unannounced Premium Increases at Renewal", "frequency": "32%", "sentiment_score": -0.85},
                {"theme": "Slow Claims Adjuster Response Times", "frequency": "21%", "sentiment_score": -0.74},
                {"theme": "Hold Times During Critical Claims Escalations", "frequency": "18%", "sentiment_score": -0.68}
            ],
            "net_sentiment_index": "+42 (Moderately Positive)",
            "key_recommendations": [
                "Cap surprise renewal premium increases and proactively disclose rate change drivers.",
                "Introduce self-service claims status tracker directly in iOS/Android app.",
                "Implement proactive premium match alerts against top 3 InsurTech competitor rates."
            ]
        }
