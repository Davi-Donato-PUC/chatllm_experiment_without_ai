from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    title: str | None = None


class SessionUpdate(BaseModel):
    title: str | None = None


class SessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionList(BaseModel):
    sessions: list[SessionOut]