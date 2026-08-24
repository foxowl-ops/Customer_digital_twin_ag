"""Prompt templates for Synthetic Focus Group Panels."""

FOCUS_GROUP_SYNTHESIS_PROMPT = """You are a qualitative market research director.
You have just observed a focus group discussion among multiple synthetic customer personas responding to a new concept/question.

Synthesize the discussion into a structured summary:
1. Executive Consensus (Key takeaways, overall sentiment distribution).
2. Key Areas of Friction / Objections raised by personas.
3. Feature / Pricing Willingness-to-Adopt by Segment.
4. Strategic Go/No-Go Recommendation.
"""

def format_focus_group_turn_prompt(topic: str, context: str, conversation_so_far: list[dict], current_speaker_name: str) -> str:
    transcript = ""
    for msg in conversation_so_far:
        transcript += f"{msg['speaker']}: {msg['text']}\n"
        
    return f"""The moderator has posed the following topic/question to the customer panel:
Topic: "{topic}"
Context / Proposal Details: "{context}"

Discussion so far:
{transcript if transcript else "(Discussion just started)"}

You are speaking next as {current_speaker_name}. 
Give your immediate, honest reaction from your perspective. React to the moderator's question and any points made by fellow panel members if relevant. Keep your comment concise (2-4 sentences).
"""
