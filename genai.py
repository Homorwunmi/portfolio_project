""" This module is responsible for generating the questions and answers for the quiz.

    Returns:
        _type_: dict
"""

import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI with the API key from environment variables
genai.configure(api_key=os.getenv('GENAI_API_KEY'))

# Generate a random number between 0 and 3
random_number = random.randint(0, 3)

# Quiz Prompt Structure
structure = '{\
"question" : " ",\
"options" : ["", "", "", ""],\
"explanation" : "" (200 chars max),\
"correct_option_id" : \
}'

# List of languages to generate questions for
languages = [
  "python",
  "javascript",
  "c",
  "bash"
]

# Create a prompt for generating a quiz question for a randomly selected language
prompt = f"Generate an interesting quiz question for {languages[random_number]} in the format: {structure}"

# AI Model Configuration settings
generation_config = {
  "temperature": 1,               # Controls the randomness of the output
  "top_p": 0.95,                  # Nucleus sampling parameter
  "top_k": 64,                    # Top-k sampling parameter
  "max_output_tokens": 8192,      # Maximum number of output tokens
  "response_mime_type": "text/plain",  # Response format
}

# Create the AI model with specified configuration
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Start a chat session with the AI model
chat_session = model.start_chat(
  history=[]  # No history for the chat session
)

# Function to prompt the AI model
def prompt_model():
  """ This function is responsible for prompting the AI model
  
    Args:
        prompts (_type_): list
        prompt_index (_type_): int

    Returns:
        _type_: dict
                The response from the AI model
    """
  
  # Send the prompt to the model and get the response
  response = chat_session.send_message(prompt)
  
  # Clean up the response by removing unnecessary characters
  response_data = response.text.replace("```json", "").replace("}\n```", "}").strip()

  # Convert the response string to a dictionary
  response_clean = eval(response_data)
  
  # Return the cleaned response dictionary
  return response_clean

# Uncomment the following line to call the function and print the response
# prompt_model()