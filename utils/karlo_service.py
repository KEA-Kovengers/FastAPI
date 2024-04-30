# import os
# from dotenv import load_dotenv
# load_dotenv('fast_sub/.env')

# from PyKakao import Karlo
# api = Karlo(service_key = os.getenv("KAKAO_RESTAPI_KEY"))

# def image_create(text):
#     # 프롬프트에 사용할 제시어
#     # text = "Cute magical flyng cat, soft golden fur, fantasy art drawn by Pixar concept artist, Toy Story main character, clear and bright eyes, sharp nose"
#     thumbnail_prompt = f'''
#     Generate an image that would be suitable as a blog thumbnail based on the provided summary.
    
#     **Summary**: "{text}"
    
#     **Instructions**:
#     1. Use the provided summary to generate an image that would capture readers' interest.
#     2. Ensure that the image is visually appealing and relevant to the content of the blog post.
#     3. Generate only one image.
#     '''

#     # 이미지 생성하기 REST API 호출
#     img_dict = api.text_to_image(thumbnail_prompt, 1)

#     # 생성된 이미지 정보
#     img_str = img_dict.get("images")[0].get('image')
#     print(img_str)

#     return img_str

# # import requests
# # import shutil

# # # 이미지 다운로드할 URL
# # image_url = img_str

# # # GET 요청을 보내서 이미지 다운로드
# # response = requests.get(image_url, stream=True)

# # # 요청이 성공적인지 확인
# # if response.status_code == 200:
# #     # 파일로 저장할 경로 지정
# #     file_path = "downloaded_image.webp"
# #     # 스트림을 이용해 이미지 데이터를 파일로 저장
# #     with open(file_path, 'wb') as f:
# #         response.raw.decode_content = True
# #         shutil.copyfileobj(response.raw, f)
# #     print("이미지가 성공적으로 저장되었습니다:", file_path)
# # else:
# #     print("이미지를 다운로드할 수 없습니다.")

