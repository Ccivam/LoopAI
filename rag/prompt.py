def build_prompt(context, question, history):
    context_text = "\n".join(context)
    history_text = "\n".join(
        [f"{h['role']}: {h['content']}" for h in history[-4:]]
    )

    return f"""
You are Loop AI, a hospital network assistant.

Conversation history:
{history_text}

Hospital network data:
{context_text}

User question:
{question}

Rules:
- If multiple hospitals match, ask a clarifying question.
- If hospital is not present, clearly say it is not in the network.
- Answer briefly and clearly.
"""
