from openai import AzureOpenAI
import requests
from PIL import Image
import json
import os
from dotenv import load_dotenv
load_dotenv('Submodules/fastapi-env/.env')

client = AzureOpenAI(
    api_version="2024-02-01",  
    api_key=os.getenv("openai_api_key"),
    azure_endpoint=os.getenv("openai_azure_endpoint")
)

def generate_hashtag(markdown_text):
    result = client.chat.completions.create(
        model= 'dev-gpt-35-turbo',
        messages= [
            {'role': 'system', 'content': 'gpt의 역할은 블로그의 내용을 받아서 블로그 내용과 어울리는 해시태그를 제작하는 것이다.'},
            {'role': 'system', 'content': '해시태그의 생성 조건은 다음과 같다.'},
            {'role': 'system', 'content': '1. Generate hashtags in word format to represent the essence of the sentence.'},
            {'role': 'system', 'content': '2. Use up to only one word per hashtag.'},
            {'role': 'system', 'content': '3. Each hashtag should capture a key aspect of the sentence\'s meaning.'},
            {'role': 'system', 'content': '4. Return the result in JSON format.'},
            {'role': 'system', 'content': '5. Speak in Korean.'},
            {'role': 'system', 'content': '6. Number of hashtags should be under the 5.'},
            {'role': 'user', 'content': '해시태그를 생성하여 JSON 형식으로 반환해주세요.'},
            {'role': 'user', 'content': '블로그의 내용은 다음과 같다.'},
            {'role': 'user', 'content': markdown_text},
            {'role': 'user', 'content': '''
                **Example Output**:
                {
                    "hashtags": [
                        "first hashtag",
                        "second hashtag",
                        "third hashtag",
                        "fourth hashtag",
                        "fifth hashtag"
                    ]
                }
             '''}
    
        ]
    )
    
    return result

def generate_text(markdown_text):
    result = client.chat.completions.create(
        model= 'dev-gpt-35-turbo',
        messages= [
            {'role': 'system', 'content': 'gpt의 역할은 몇개의 키워드를 받아서 어울리는 문장을 제작하는 것이다.'},
            {'role': 'system', 'content': '문장의 생성 조건은 다음과 같다.'},
            {'role': 'system', 'content': '1. Use the provided keywords to generate a meaningful sentence.'},
            {'role': 'system', 'content': '2. The sentence should be written in Korean.'},
            {'role': 'system', 'content': '3. Ensure that the sentence makes sense and is grammatically correct.'},
            {'role': 'system', 'content': '4. Generate only one sentence.'},
            {'role': 'system', 'content': '5. Return the result in JSON format.'},
            {'role': 'system', 'content': '6. Speak in Korean.'},
            {'role': 'user', 'content': '해시태그를 생성하여 JSON 형식으로 반환해주세요.'},
            {'role': 'user', 'content': '키워드의 내용은 다음과 같다.'},
            {'role': 'user', 'content': markdown_text},
            {'role': 'user', 'content': '''
                **Example Output**:
                {
                    "sentence": "The dog is playing happily in the park."
                }
             '''}
    
        ]
    )
    
    return result

def modify_spell(sentence):
    result = client.chat.completions.create(
        model= 'dev-gpt-35-turbo',
        messages= [
            {'role': 'system', 'content': 'gpt의 역할은 블로그의 내용을 받아서 맞춤법을 검사하고 다시 올바른 문장으로 제작하는 것이다.'},
            {'role': 'system', 'content': '맞춤법 검사 조건은 다음과 같다.'},
            {'role': 'system', 'content': '1. Carefully review the sentence provided.'},
            {'role': 'system', 'content': '2. Identify and correct any spelling or typographical errors present in the sentence.'},
            {'role': 'system', 'content': '3. Ensure that the corrected sentence is grammatically correct and makes sense in context.'},
            {'role': 'system', 'content': '4. Provide the corrected version of the sentence.'},
            {'role': 'system', 'content': '5. Return the result in JSON format.'},
            {'role': 'system', 'content': '6. Speak in Korean.'},
            {'role': 'user', 'content': '''
                **Example Output**:
                {
                    "sentence": "The dog is palying happily in the prak.",
                    "correct": "The dog is playing happily in the park."
                }
             '''},
            {'role': 'user', 'content': '블로그의 내용을 검사하고 JSON 형식으로 반환해주세요.'},
            {'role': 'user', 'content': '아래 나오는 내용이 블로그의 내용이다.'},
            {'role': 'user', 'content': sentence}
    
        ]
    )
    
    return result

def genereate_summary(sentence):
    result = client.chat.completions.create(
        model= 'dev-gpt-35-turbo',
        messages= [
            {'role': 'system', 'content': 'gpt의 역할은 블로그의 내용을 받아서 요약한 내용을 제작하는 것이다.'},
            {'role': 'system', 'content': '블로그 내용 요약의 조건은 다음과 같다.'},
            {'role': 'system', 'content': '1. Read the provided blog post carefully.'},
            {'role': 'system', 'content': '2. Summarize the main points and key information.'},
            {'role': 'system', 'content': '3. Ensure that the summary is concise and well-written.'},
            {'role': 'system', 'content': '4. Generate only one summary.'},
            {'role': 'system', 'content': '5. The summarized blog content should not exceed a maximum of 500 characters.'},
            {'role': 'system', 'content': '6. Return the result in JSON format.'},
            {'role': 'system', 'content': '7. Speak in Korean.'},
            {'role': 'system', 'content': '8. 요약된 글을 작성할 때, 각 문장을 `~~입니다.`와 같은 완성된 문장으로 제작해.'},
            {'role': 'user', 'content': '블로그의 내용을 요약한 뒤 JSON 형식으로 반환해주세요.'},
            {'role': 'user', 'content': '블로그의 내용은 다음과 같다.'},
            {'role': 'user', 'content': sentence},
            {'role': 'user', 'content': '''
                **Example Output**:
                {
                    "summary": "The summary of the blog post goes here."
                }
             '''}
    
        ]
    )
    
    return result

def generate_image(text):
    result = client.images.generate(
        model="dev-dall-e-3", # the name of your DALL-E 3 deployment
        prompt=f'''
            Generate an image that would be suitable as a blog thumbnail based on the provided summary.
            
            **Summary**: "{text}"
            
            **Instructions**:
            1. Use the provided summary to generate an image that would capture readers' interest.
            2. Ensure that the image is visually appealing and relevant to the content of the blog post.
            3. Generate only one image.
            4. 이미지는 글씨를 포함하지 말고 추상적으로 블로그 내용과 어울리는 객체에 대해서 생성해야한다.
        ''',
        n=1
    )

    json_response = json.loads(result.model_dump_json())

    image_url = json_response["data"][0]["url"]

    return image_url