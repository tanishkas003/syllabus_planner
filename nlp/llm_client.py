import openai
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def chat_completion(
    system_prompt: str, user_prompt: str, temperature=0.2, max_tokens=800
):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # change to a model you have access to
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message["content"]


DECOMPOSE_SYSTEM = (
    "You are an expert instructional designer. Break topics into smaller study units."
)
DECOMPOSE_USER = (
    "Input topic: {topic}\nContext: {context}\n"
    "Return a JSON list of objects: "
    '[{"title": "...", "objective":"...", "est_hours": number, "difficulty": "low|mid|high"}]'
)

GEN_CARD_SYSTEM = "You are a helpful teacher. Generate summary, flashcards and practice questions for a topic."
GEN_CARD_USER = (
    "Topic: {title}\nObjective: {objective}\nEst_hours: {est_hours}\n"
    'Return JSON: {"summary":"..","flashcards":[{"q":"","a":""}],'
    '"practice_questions":[{"q":"","a":""}],"resources":[]}'
)
