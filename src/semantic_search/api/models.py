from pydantic import BaseModel

from typing import List, Dict

class ChatRequest(BaseModel):
    history: List[Dict]
    inject_info: bool = False
