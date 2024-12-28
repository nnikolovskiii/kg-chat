import os
from typing import List, Dict

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

from yago_chat.llms.utils import _get_messages_template


async def chat_with_hf_inference(
        message: str,
        system_message: str,
        history: List[Dict[str, str]] = None,
        stream: bool = False,
):
    load_dotenv()
    hf_api_key = os.getenv("HF_API_KEY")
    hf_model = os.getenv("HF_MODEL")

    client = InferenceClient(model=hf_model, api_key=hf_api_key, headers={"x-use-cache":"false"})

    messages = _get_messages_template(message, system_message, history)

    args = {
        "max_tokens": 15000,
        "messages": messages,
        "temperature": 0.5,
        "top_p": 0.8,
        "stream": False
    }

    output = client.chat_completion(**args)
    return output.choices[0]["message"]["content"]


