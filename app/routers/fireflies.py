import json
import requests

from app.config import config
from fastapi import APIRouter, HTTPException
from app.utils.fireflies.fetch_messages import fetch_transcript
from app.utils.fireflies.parse_transcript import parse_transcript
from app.utils.fireflies.extract_cheat_sheet import extract_cheat_sheet
from app.models.fireflies import FireflyRequest, TranscriptionRequest
from app.utils.fireflies.extract_candidate_information import (
    extract_candidate_information,
)

url = "https://api.fireflies.ai/graphql"
default_headers = {"Content-Type": "application/json"}

# user id: E08oX1s7um
# transcript id: U2W1tF8zK9qE2iAw

firefly_api_key = config.fireflies_api_key
router = APIRouter()


@router.get("/health-check")
def health_check():
    return {"firefly_api_key": firefly_api_key}


@router.post("/get-user")
async def get_users():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {firefly_api_key}",
    }

    data = {"query": "{ users { name user_id } }"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@router.post("/get-transcriptions")
async def get_transcriptions(request: FireflyRequest):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {firefly_api_key}",
    }

    payload_str = request.model_dump_json()
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in the request payload."
        )

    if "userId" in payload:
        user_id = payload["userId"]
        data = {
            "query": "query Transcripts($userId: String) { transcripts(user_id: $userId) { title id } }",
            "variables": {"userId": user_id},
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="userId is missing in the payload")


@router.post("/get-transcription-messages")
async def get_transcript_messages(request: TranscriptionRequest):
    payload_str = request.model_dump_json()
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in the request payload."
        )

    if "transcriptId" in payload:
        transcript_id = payload["transcriptId"]
        return fetch_transcript(transcript_id, url, firefly_api_key)
    else:
        raise HTTPException(
            status_code=400, detail="transcriptId is missing in the payload"
        )


@router.post("/parse-transcript")
async def parse_transcription(request: TranscriptionRequest):
    payload_str = request.model_dump_json()
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in the request payload."
        )

    if "transcriptId" in payload:
        transcript_id = payload["transcriptId"]
        transcript_data = fetch_transcript(transcript_id, url, firefly_api_key)
        parsed_transcript = parse_transcript(transcript_data)
        return {"parsed_transcript": parsed_transcript}
    else:
        raise HTTPException(
            status_code=400, detail="transcriptId is missing in the payload"
        )


@router.post("/extract-information")
async def extract_information(request: TranscriptionRequest):
    payload_str = request.model_dump_json()
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in the request payload."
        )

    if "transcriptId" in payload:
        transcript_id = payload["transcriptId"]
        transcript_data = fetch_transcript(transcript_id, url, firefly_api_key)
        parsed_transcript = parse_transcript(transcript_data)
        extracted_information = extract_candidate_information(parsed_transcript)
        return {"extracted_information": extracted_information}
    else:
        raise HTTPException(
            status_code=400, detail="transcriptId is missing in the payload"
        )


@router.post("/extract-cheat-sheet")
async def extract_cheatsheet(request: TranscriptionRequest):
    payload_str = request.model_dump_json()
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in the request payload."
        )

    if "transcriptId" in payload:
        transcript_id = payload["transcriptId"]
        transcript_data = fetch_transcript(transcript_id, url, firefly_api_key)
        parsed_transcript = parse_transcript(transcript_data)
        extracted_cheat_sheet = extract_cheat_sheet(parsed_transcript)
        return {"extracted_cheat_sheet": extracted_cheat_sheet}
    else:
        raise HTTPException(
            status_code=400, detail="transcriptId is missing in the payload"
        )
