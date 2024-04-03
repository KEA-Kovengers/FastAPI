import os
import vertexai
import vertexai.preview
from vertexai.preview.generative_models import GenerativeModel
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))

import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

model = GenerativeModel(os.getenv("VERSION"))
chat = model.start_chat()

def generate_hashtag(markdown_text):
    prompt = f'''
    Your task is to summarize an markdown text into multiple hashtags. 
    Generate hashtags for the following text: {markdown_text}. 
    Speak in Korean. And you should return as json type.
    '''
    response = model.generate_content(prompt)
    return response.text

def generate_text(keywords):
    prompt = f'''
    Your task is to generate a sentence based on the following keywords. 
    Generate just one sentece for the following keywords : {keywords}. 
    Speak in Korean.
    '''
    response = model.generate_content(prompt)
    return response.text

def find_typo(sentence):
    prompt = f'''
    Your task is to find typos on the following sentence. 
    find typos for the following sentence. 
    Please correct each typo: {sentence}. 
    Speak in Korean.
    '''
    response = model.generate_content(prompt)
    return response.text
