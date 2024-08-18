from pydantic import BaseModel
from typing import Any, Dict

class WebhookRequest(BaseModel):
    activity:str
    data:Dict = None
    