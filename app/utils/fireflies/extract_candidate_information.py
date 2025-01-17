from openai import OpenAI
from app.config import config
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from app.utils.cost.compute import calculate_chat_completion_cost

# Initialize the OpenAI client
client = OpenAI(api_key=config.openai_api_key)


class FieldWithSnippet(BaseModel):
    """
    A model to store a value along with the snippet of transcript where it was pulled from.
    """

    value: Optional[str] = Field(
        description="The extracted value from the transcript. If the value is not available, it will be null."
    )
    snippet: Optional[str] = Field(
        description="The snippet of the transcript from which the value was extracted and a sentence before and after that for more context. If no snippet is available, it will be null."
    )


class CandidateInfo(BaseModel):
    """
    A schema for the candidate information extracted from interviews, including the transcript snippets.
    """

    name: FieldWithSnippet = Field(
        description="The full name of the candidate, including both first and last name. If not available, return null."
    )
    position: FieldWithSnippet = Field(
        description="The current or most recent position of the candidate. If no position is mentioned, return null."
    )
    age: FieldWithSnippet = Field(
        description="The age of the candidate. If the age is not provided or cannot be determined, return null."
    )
    desired_salary: FieldWithSnippet = Field(
        description="The salary amount the candidate desires for their next position. If no desired salary is mentioned, return null."
    )
    current_salary: FieldWithSnippet = Field(
        description="The current salary of the candidate. If no current salary is mentioned, return null."
    )
    desired_position: FieldWithSnippet = Field(
        description="The job position or role the candidate is aiming for. If not mentioned, return null."
    )
    desired_company: FieldWithSnippet = Field(
        description="The company or industry the candidate wants to work in. If no company or industry is mentioned, return null."
    )
    desired_location: FieldWithSnippet = Field(
        description="The location where the candidate prefers to work. If not mentioned, return null."
    )
    personality_assessment: FieldWithSnippet = Field(
        description="An assessment of the candidate's personality based on the interview."
    )
    date_of_birth: FieldWithSnippet = Field(
        description="The date of birth of the candidate. If not provided, return null."
    )
    basic_summary: FieldWithSnippet = Field(
        description="A concise summary of the candidate based on the interview. If no summary is available, return null."
    )
    pitched_jobs: Optional[List[Dict[str, FieldWithSnippet]]] = Field(
        description="A list of jobs pitched during the interview along with candidate interest. If no jobs are mentioned, return an empty list."
    )
    notice_period: FieldWithSnippet = Field(
        description="The candidate's notice period or availability to start a new job. If no notice period is mentioned, return null."
    )
    contact_preference: FieldWithSnippet = Field(
        description="The candidate's preferred method of contact. If no contact preference is mentioned, return null."
    )
    additional_info: Optional[List[Dict[str, FieldWithSnippet]]] = Field(
        description="Other relevant information extracted from the interview. If no additional info is available, return an empty list."
    )


# Function to get structured candidate information from the transcript
def extract_candidate_information(transcript: str):
    # Call the OpenAI API with the request to extract structured data
    completion = client.beta.chat.completions.parse(
        model=config.gpt_model,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts structured information from transcripts.",
            },
            {
                "role": "user",
                "content": f"Extract the candidate information in JSON format: {transcript}",
            },
        ],
        response_format=CandidateInfo,
    )

    completion_cost = calculate_chat_completion_cost(completion.usage)
    print("completion cost:", completion_cost)
    return completion.choices[0].message.parsed
