import os
from enum import Enum

from dotenv import load_dotenv

from yago_chat.llms.custom_chat import chat_with_custom_api
from yago_chat.llms.hf_inference_chat import chat_with_hf_inference
from yago_chat.llms.nim_chat import chat_with_nim
from yago_chat.llms.ollama_chat import chat_with_ollama
from yago_chat.llms.openai_chat import chat_with_openai


class ChatModel(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    NIM = "nim"
    HF_INF = "hf_inf"
    CUSTOM_API = "custom_api"


async def generic_chat(
        message: str,
        system_message: str = "You are a helpful AI assistant.",
        model:str = None
) -> str:
    load_dotenv()

    chat_model = os.getenv("CHAT_MODEL")

    if chat_model == ChatModel.OPENAI.value:
        return chat_with_openai(message, system_message)
    elif chat_model == ChatModel.OLLAMA.value:
        return chat_with_ollama(message, system_message)
    elif chat_model == ChatModel.NIM.value:
        return chat_with_nim(message, system_message)
    elif chat_model == ChatModel.HF_INF.value:
        return await chat_with_hf_inference(message, system_message, model)
    elif chat_model == ChatModel.CUSTOM_API.value:
        return chat_with_custom_api(message)
