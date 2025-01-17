from enum import Enum
from openai import OpenAI
from app.config import config
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from app.utils.cost.compute import calculate_chat_completion_cost

client = OpenAI(api_key=config.openai_api_key)


class MainCategory(str, Enum):
    INDUSTRY_SPECIFIC = "Industry-Specific Questions"
    GENERIC = "Generic Questions"


class IndustrySpecificSubcategory(str, Enum):
    PREVIOUS_EXPERIENCE = "Previous Experience"
    WORKPLACE_RESPONSIBILITIES = "Workplace and Responsibilities"


class GenericSubcategory(str, Enum):
    CANDIDATE_PROFILE = "Candidate Profile"
    CAREER_DEVELOPMENT = "Career Development and Aspirations"
    JOB_SEARCH = "Job Search"
    APPLICATION_PROCESS = "Application Process"
    CURRENT_COMPENSATION = "Current Compensation"
    FUTURE_OPPORTUNITIES = "Future Opportunities"


class QuestionWithAnswer(BaseModel):
    question: str = Field(description="The interview question being evaluated.")
    is_answered: bool = Field(
        description="A boolean indicating whether the question was answered in the transcript."
    )
    answer_summary: Optional[str] = Field(
        description="A brief summary of the answer, if available. Otherwise, null."
    )


class CategoryEvaluation(BaseModel):
    category_name: Union[IndustrySpecificSubcategory, GenericSubcategory] = Field(
        description="The name of the question subcategory."
    )
    questions: List[QuestionWithAnswer] = Field(
        description="List of questions and their evaluations for this category."
    )


class MainCategoryEvaluation(BaseModel):
    main_category: MainCategory = Field(
        description="The main category name (Industry-Specific or Generic)."
    )
    subcategories: List[CategoryEvaluation] = Field(
        description="List of subcategories and their question evaluations."
    )


class CheatSheet(BaseModel):
    evaluations: List[MainCategoryEvaluation] = Field(
        description="List of main categories with their subcategories and question evaluations."
    )


# Define the questions structure
industry_specific_questions = {
    IndustrySpecificSubcategory.PREVIOUS_EXPERIENCE: [
        "What hotels has the candidate worked at?",
        "For the latest hotel: How many rooms does the hotel have?",
        # ... (include all questions from this category)
    ],
    IndustrySpecificSubcategory.WORKPLACE_RESPONSIBILITIES: [
        "What hotel departments have they experienced working in?",
        "What hotel department do they currently work in?",
        # ... (include all questions from this category)
    ],
}

generic_questions = {
    GenericSubcategory.CANDIDATE_PROFILE: [
        "Where are they from originally?",
        "Where did they go to university?",
        # ... (include all questions from this category)
    ],
    GenericSubcategory.CAREER_DEVELOPMENT: [
        "What is their ultimate career goal?",
        "What role and title do they want next?",
        # ... (include all questions from this category)
    ],
    GenericSubcategory.JOB_SEARCH: [
        "What have they done so far in their search?",
        "How has that worked for them?",
        # ... (include all questions from this category)
    ],
    GenericSubcategory.APPLICATION_PROCESS: [
        "When is the candidate available for an interview?",
        "Did the consultant confirm we have the resume?",
        "What next steps were agreed?",
    ],
    GenericSubcategory.CURRENT_COMPENSATION: [
        "What is their current salary (monthly base, overtime, incentive, bonus, housing)?",
        "Is it gross or net, and what currency?",
    ],
    GenericSubcategory.FUTURE_OPPORTUNITIES: [
        "Which specific roles did the consultant pitch to the candidate?",
        "Which roles did the candidate agree to apply to?",
    ],
}


def extract_cheat_sheet(transcript: str) -> CheatSheet:
    prompt = f"""
    Given the following transcript of an interview, evaluate each question in the categories below:
    - Determine if the question was answered in the transcript.
    - If answered, provide a brief summary of the answer.
    - If not answered, set the summary to null.

    Transcript:
    {transcript}

    Questions to evaluate:

    Industry-Specific Questions:
    {industry_specific_questions}

    Generic Questions:
    {generic_questions}

    Extract the information in JSON format matching the CheatSheet model structure.
    Ensure that all category and subcategory names exactly match the enum values defined in the model.
    """

    completion = client.beta.chat.completions.parse(
        model=config.gpt_model,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts structured information from transcripts.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=CheatSheet,
    )

    completion_cost = calculate_chat_completion_cost(completion.usage)
    print("completion cost:", completion_cost)
    return completion.choices[0].message.parsed
