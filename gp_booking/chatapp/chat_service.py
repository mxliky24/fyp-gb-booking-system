import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key=api_key

def generate_response(prompt):

    response = openai.Completion.create(

    engine='gpt-3.5-turbo',

    prompt=prompt,

    max_tokens=150,

    temperature=0.7,

    )

    return response.choices[0].text.strip()