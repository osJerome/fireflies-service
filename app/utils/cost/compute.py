import os
import logging

from datetime import datetime
from app.config import config

# Setup logging configuration
log_directory = "/logs"
os.makedirs(log_directory, exist_ok=True)

# Define the log filename based on the current date
cost_log_filename = os.path.join(log_directory, f"cost_log_{datetime.now().date()}.log")

# Configure logger for chat completion costs
cost_logger = logging.getLogger("cost_logger")
cost_logger.setLevel(logging.INFO)
cost_handler = logging.FileHandler(cost_log_filename)
cost_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
cost_logger.addHandler(cost_handler)


def calculate_chat_completion_cost(completion_usage, model_name=config.gpt_model):
    models = {
        "gpt-4o-mini": {
            "input_price_per_1000_tokens": 0.000150,
            "output_price_per_1000_tokens": 0.000600,
            "cached_input_price_per_1M_tokens": 0.075,
        }
        # Add more models here if needed
    }

    # Find the selected model pricing info
    selected_model = models.get(model_name)

    if not selected_model:
        raise ValueError(f"Model '{model_name}' not found.")

    # Extract token details from the completion_usage
    completion_tokens = completion_usage.completion_tokens
    prompt_tokens = completion_usage.prompt_tokens
    cached_tokens = completion_usage.prompt_tokens_details["cached_tokens"]

    # Calculate non-cached input tokens
    non_cached_tokens = prompt_tokens - cached_tokens

    # Pricing per token
    input_price_per_token = selected_model["input_price_per_1000_tokens"] / 1000
    output_price_per_token = selected_model["output_price_per_1000_tokens"] / 1000
    cached_input_price_per_token = (
        selected_model["cached_input_price_per_1M_tokens"] / 1_000_000
    )

    # Cost calculations
    non_cached_input_cost = non_cached_tokens * input_price_per_token
    cached_input_cost = cached_tokens * cached_input_price_per_token
    completion_cost = completion_tokens * output_price_per_token

    # Total cost
    total_cost = non_cached_input_cost + cached_input_cost + completion_cost

    # Log the relevant information
    cost_logger.info(
        f"Model: {model_name}, "
        f"Input Price: ${selected_model['input_price_per_1000_tokens']}, "
        f"Output Price: ${selected_model['output_price_per_1000_tokens']}, "
        f"Cached Input Price: ${selected_model['cached_input_price_per_1M_tokens']}, "
        f"Tokens - Input: {prompt_tokens}, Cached: {cached_tokens}, "
        f"Completion: {completion_tokens}, "
        f"Costs - Non-Cached Input: ${non_cached_input_cost:.6f}, "
        f"Cached Input: ${cached_input_cost:.6f}, "
        f"Completion: ${completion_cost:.6f}, "
        f"Total Cost: ${total_cost:.6f}"
    )

    return total_cost
