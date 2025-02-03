from pydantic import BaseModel, UUID4
from typing import Optional, List


class AccessPolicyCreate(BaseModel):
    nome: str
    effect: str
    actions: List[str]
    resources: List[str]
    conditions: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class AccessPolicyUpdate(BaseModel):
    nome: Optional[str] = None
    effect: Optional[str] = None
    actions: Optional[List[str]] = None
    resources: Optional[List[str]] = None
    conditions: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class AccessPolicyView(AccessPolicyCreate):
    id: UUID4
    
    class Config:
        from_attributes = True

class AccessPolicyResponseList(BaseModel):
    total: int
    data: List[AccessPolicyView]

    class Config:
        from_attributes = True

class AccessPolicyResponse(BaseModel):
    data: List[AccessPolicyView]

    class Config:
        from_attributes = True