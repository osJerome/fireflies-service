from pydantic import BaseModel


class FireflyRequest(BaseModel):
    userId: str


class TranscriptionRequest(BaseModel):
    transcriptId: str
