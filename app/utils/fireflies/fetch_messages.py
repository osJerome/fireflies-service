import requests

from fastapi import HTTPException


def fetch_transcript(transcript_id: str, url: str, firefly_api_key: str):
    """
    Fetches the transcript data from the API using the given transcript ID.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {firefly_api_key}",
    }

    data = {
        "query": """
        query Transcript($transcriptId: String!) { 
            transcript(id: $transcriptId) {
                sentences {
                    index
                    speaker_name
                    speaker_id
                    text
                    raw_text
                    start_time
                    end_time
                }
            }
        }""",
        "variables": {"transcriptId": transcript_id},
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500, detail=str(e)
        )
