import os

import ollama as oll

from typing import Dict, List

LLM_CLIENT: oll.Client = oll.Client(host=os.getenv("OLLAMA_CONN_ENDPOINT"))

def call(
    messages: List[Dict],
) -> str:

    response: oll.ChatResponse = LLM_CLIENT.chat(
        model="llama3.2", 
        messages=messages,
    )
    
    return str(response.message.content)