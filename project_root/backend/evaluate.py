# evaluate.py

import arize.pandas.logger as arize
import pandas as pd
import uuid
import os
from datetime import datetime

# Load API keys from environment (set these before running)
SPACE_KEY = os.getenv("ARIZE_SPACE_KEY")
API_KEY = os.getenv("ARIZE_API_KEY")

# Initialize Arize client
client = arize.Client(space_key=SPACE_KEY, api_key=API_KEY)

def log_response(user_prompt: str, model_response: str):
    """Logs prompt-response pairs to Arize for evaluation."""
    df = pd.DataFrame({
        "prediction_id": [str(uuid.uuid4())],
        "prompt": [user_prompt],
        "response": [model_response],
        "timestamp": [datetime.now()]
    })

    # Log to Arize
    client.log(
        dataframe=df,
        model_id="ai-clone-chatbot",
        model_type="llm",
        prompt_column_name="prompt",
        response_column_name="response",
        prediction_id_column_name="prediction_id",
        timestamp_column_name="timestamp"
    )
