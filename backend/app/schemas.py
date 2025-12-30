from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List


# ---------- Config Settings ----------
class Settings(BaseSettings):
    app_name: str = Field(default="telecom-billing-cdr")
    environment: str = Field(default="dev")
    database_url: str = Field(default="sqlite:///./telecom.db", alias="DATABASE_URL")
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


# ---------- CDR Models ----------
class CDRIn(BaseModel):
    caller: str
    receiver: str
    duration: int  # in seconds
    timestamp: str  # ISO format


class CDROut(CDRIn):
    id: int


class IngestResponse(BaseModel):
    success: bool
    ingested: int


class RatedEventOut(CDROut):
    cost: float


# ---------- Subscriber Models ----------
class SubscriberBase(BaseModel):
    name: str
    phone_number: str


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberOut(SubscriberBase):
    id: int


# ---------- Usage Models ----------
class UsageItem(BaseModel):
    cdr_id: int
    cost: float
    duration: int


class UsageSummary(BaseModel):
    subscriber_id: int
    total_cost: float
    total_duration: int
    items: List[UsageItem] = []
