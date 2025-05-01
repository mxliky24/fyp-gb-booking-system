import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY') # Retrieves the OpenAI API key
openai.api_key=api_key  # Sets the API key for OpenAI usage
# Sends user input (prompt) to OpenAI and returns chatbot response
def generate_response(prompt):

    response = openai.Completion.create(

    engine='gpt-3.5-turbo',

    prompt=prompt,

    max_tokens=150,   # Limits the length of the response

    temperature=0.7,   # Controls randomness of response

    )

    return response.choices[0].text.strip()  # Extracts and returns the response text