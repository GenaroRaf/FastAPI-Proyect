from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#Class Model
class Proyect(BaseModel): #Schema
    account:str
    detailType:str
    region:str
    source:str
    time:str
    notificationRuleArn:str
    detail:dict
    resources:list
    additionalAttributes:Optional[dict]
