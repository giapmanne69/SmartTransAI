from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

# Glossary Schemas
class GlossaryCreate(BaseModel):
    source_term: str = Field(..., min_length=1)
    target_term: str = Field(..., min_length=1)
    notes: Optional[str] = None

class GlossaryUpdate(BaseModel):
    source_term: Optional[str] = None
    target_term: Optional[str] = None
    notes: Optional[str] = None

class GlossaryOut(BaseModel):
    id: int
    user_id: int
    source_term: str
    target_term: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Document & Chunk Schemas
class DocumentChunkOut(BaseModel):
    id: int
    document_id: int
    original_text: str
    translated_text: Optional[str] = None
    context_window: Optional[str] = None
    position_index: int
    status: str
    reviewer_feedback: Optional[str] = None
    corrected_by_user: bool

    class Config:
        from_attributes = True

class DocumentChunkUpdate(BaseModel):
    translated_text: str
    corrected_by_user: bool = True

class DocumentOut(BaseModel):
    id: int
    name: str
    file_type: str
    status: str
    user_id: int
    created_at: datetime
    chunks: Optional[List[DocumentChunkOut]] = None

    class Config:
        from_attributes = True
