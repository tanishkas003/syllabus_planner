import json
from nlp.llm_client import chat_completion, DECOMPOSE_SYSTEM, DECOMPOSE_USER, GEN_CARD_SYSTEM, GEN_CARD_USER

def decompose_topic(topic_title: str, context: str):
    prompt = DECOMPOSE_USER.format(topic=topic_title, context=context)
    resp = chat_completion(DECOMPOSE_SYSTEM, prompt, temperature=0.2, max_tokens=600)
    try:
        data = json.loads(resp)
    except Exception:
        import re
        m = re.search(r'(\[.*\])', resp, re.S)
        if m:
            data = json.loads(m.group(1))
        else:
            raise
    for node in data:
        node.setdefault("est_hours", 1)
        node.setdefault("difficulty", "mid")
    return data

def generate_cards_for_node(node):
    prompt = GEN_CARD_USER.format(title=node["title"], objective=node.get("objective",""), est_hours=node.get("est_hours",1))
    resp = chat_completion(GEN_CARD_SYSTEM, prompt, temperature=0.4, max_tokens=800)
    try:
        obj = json.loads(resp)
    except Exception:
        import re
        m = re.search(r'(\{.*\})', resp, re.S)
        if m:
            obj = json.loads(m.group(1))
        else:
            raise
    return obj
