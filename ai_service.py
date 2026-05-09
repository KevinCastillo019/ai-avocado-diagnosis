import os

from dotenv import load_dotenv
from groq import Groq


MODEL_NAME = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = (
    "You are an expert agronomist specialized in avocado crops. "
    "Respond clearly, practically, and professionally."
)


load_dotenv()


def build_recommendation_prompt(diagnosis, treatments, decision_path=None):
    treatment_list = ", ".join(treatments) if treatments else "No predefined treatments"
    context_lines = "\n".join(f"- {step}" for step in (decision_path or []))
    context_block = context_lines if context_lines else "- No additional field context provided"

    return f"""
You are an experienced agronomist from Cauca, Colombia.

The system reached the following diagnosis through a decision graph.

Observed field context:
{context_block}

Diagnosis:
{diagnosis}

Recommended treatments:
{treatment_list}

Explain clearly and simply:
- What is happening
- Why it happens
- What the farmer should do step by step
- Prevention recommendations
- Good agricultural practices
""".strip()


def generate_recommendation(
    diagnosis,
    treatments,
    decision_path=None,
    temperature=None,
):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    request_kwargs = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_recommendation_prompt(
                    diagnosis,
                    treatments,
                    decision_path=decision_path,
                ),
            },
        ],
    }

    if temperature is not None:
        request_kwargs["temperature"] = temperature

    completion = client.chat.completions.create(**request_kwargs)

    return completion.choices[0].message.content
