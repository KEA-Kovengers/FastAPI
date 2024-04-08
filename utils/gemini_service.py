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
    # Example text and corresponding hashtags
    example_text = '''
    The serene lake shimmered in the moonlight, reflecting the twinkling stars above. 
    A gentle breeze rustled through the trees, carrying the scent of pine and damp earth. 
    Far in the distance, a lone wolf howled, its mournful cry echoing across the silent wilderness. 
    On the shore, a campfire crackled, casting dancing shadows on the faces of the weary travelers gathered around it. 
    Amidst the tranquility of the night, whispers of ancient legends and forgotten tales filled the air, weaving a tapestry of mystery and magic.
    '''
    example_hashtags = [
        "serene lake shimmered moonlight", 
        "gentle breeze rustled trees", 
        "lone wolf howled mournful cry", 
        "campfire crackled dancing shadows", 
        "ancient legends forgotten tales mystery"
    ]

    # Constructing the prompt
    prompt = f'''
    Summarize the following markdown text into hashtags with up to five words to represent the essence of the sentence.

    **Markdown Text**: "{markdown_text}"
    
    **Instructions**:
    1. Generate hashtags in word format to represent the essence of the sentence.
    2. Use up to five words per hashtag.
    3. Each hashtag should capture a key aspect of the sentence's meaning.
    4. Return the result in JSON format.
    5. Speak in Korean.
    
    **Example Text**: "{example_text}"
    **Example Hashtags**: {example_hashtags}
    
    **Example Output**:
    {{
        "hashtags": {example_hashtags}
    }}
    '''

    # Sending the prompt to the GPT model and getting the response
    response = model.generate_content(prompt)
    
    # Returning the text response from the model
    return response.text


def generate_text(keywords):
    # Constructing the prompt
    prompt = f'''
    Generate a sentence based on the provided keywords.
    
    **Keywords**: "{keywords}"
    
    **Instructions**:
    1. Use the provided keywords to generate a meaningful sentence.
    2. The sentence should be written in English.
    3. Ensure that the sentence makes sense and is grammatically correct.
    4. Generate only one sentence.
    5. Speak in Korean.
    
    **Example**: "The dog is playing happily in the park."
    '''

    # Sending the prompt to the GPT model and getting the response
    response = model.generate_content(prompt)
    
    # Returning the text response from the model
    return response.text

# def find_typo(sentence):
#     # 프롬프트 생성
#     prompt = f'''
#     Your task is to find and correct any typos in the following sentence:
    
#     **Original Sentence**: "{sentence}"
    
#     **Instructions**:
#     1. Carefully review the sentence provided.
#     2. Identify and correct any spelling or typographical errors present in the sentence.
#     3. Ensure that the corrected sentence is grammatically correct and makes sense in context.
#     4. Provide the corrected version of the sentence.
#     5. Speak in Korean.
#     '''

#     # GPT 모델을 사용하여 프롬프트를 전달하고 응답 받기
#     response = model.generate_content(prompt)
    
#     # 모델에서 반환된 응답 텍스트 반환
#     return response

def find_typo(sentence):
    prompt = f'''
    Your task is to find and correct any typos in the following sentence. 
    find typos for the following sentence. 
    Please correct each typo: {sentence}. 

    **Instructions**:
    1. Carefully review the sentence provided.
    2. Identify and correct any spelling or typographical errors present in the sentence.
    3. Ensure that the corrected sentence is grammatically correct and makes sense in context.
    4. Provide the corrected version of the sentence.
    5. Speak in Korean.
    '''
    response = model.generate_content(prompt)
    return response.text
