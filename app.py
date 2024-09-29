from flask import Flask, request, jsonify, render_template
import base64
import io
from PIL import Image
import requests
import openai

app = Flask(__name__)

# Function to encode an image directly from memory
def encode_image(image_file):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")  # Save image in JPEG format to the buffer
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for analyzing images
@app.route('/analyze-images', methods=['POST'])
def analyze_images():
    image_files = request.files.getlist('images')
    
    # Process images from memory
    encoded_images = [encode_image(image) for image in image_files]
    
    # Call your existing function here to analyze the images
    result = analyze_images_with_gpt4(encoded_images)

    return jsonify(result)

# Function to analyze multiple base64-encoded images with GPT-4
def analyze_images_with_gpt4(encoded_images):
    api_key = "sk-Rua0IGK2JbaymtUYO2E5B11AjRuifrd5CAQw131HKqT3BlbkFJ-PqLv3hSS2EQP2B73Joh0khcVhPeh-RTlHgbFQw7kA"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    content = [
        {"type": "text", "text": " You are a Hinge profile optimization assistant. Analyze the Hinge profile in the images for the following: 1. Evaluate the quality of the images and prompts individually on how attractive, genuine it is. 2. If it is a guy’s profile, look at from a female perspective and suggest changes that would attract the opposite sex and vice versa but don't be very explicit about it. You can add a funny tinge to your analysis as well. 3. Give them a ‘Hinge appeal’ rating from 1 to 10 based on the overall profile quality. 4. Lastly put top 3 actionable things they can change about their hinge profile to make it better instantly. In your output dont put the ‘###’ in the final output. 'Lets see how I can get your more matches'- use this phrase at the beginning of your output. Keep your output to 200 words"}
    ]

    for encoded_image in encoded_images:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
        })

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run()










# from flask import Flask, request, jsonify, render_template
# import base64
# import os
# import requests
# import openai
# app = Flask(__name__)

# # Function to encode an image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# # Route for the main page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route for analyzing images
# @app.route('/analyze-images', methods=['POST'])
# def analyze_images():
#     image_files = request.files.getlist('images')
#     image_paths = []

#     # Save and encode images
#     for image in image_files:
#         image_path = os.path.join('uploads', image.filename)
#         image.save(image_path)
#         image_paths.append(image_path)

#     # Call your existing function here to analyze the images
#     result = analyze_images_with_gpt4(image_paths)

#     return jsonify(result)

# # Function to analyze multiple base64-encoded images with GPT-4
# def analyze_images_with_gpt4(image_paths):
#     api_key = "sk-Rua0IGK2JbaymtUYO2E5B11AjRuifrd5CAQw131HKqT3BlbkFJ-PqLv3hSS2EQP2B73Joh0khcVhPeh-RTlHgbFQw7kA"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }

#     content = [
#         {"type": "text", "text": " You are a Hinge profile optimization assistant. Analyze the Hinge profile in the images for the following: 1. Evaluate the quality of the images and prompts individually on how attractive, genuine it is. 2. If it is a guy’s profile, look at from a female perspective and suggest changes that would attract the opposite sex and vice versa but don't be very explicit about it. You can add a funny tinge to your analysis as well. 3. Give them a ‘Hinge appeal’ rating from 1 to 10 based on the overall profile quality. 4. Lastly put top 3 actionable things they can change about their hinge profile to make it better instantly. In your output dont put the ‘###’ in the final output. 'Lets see how I can get your more matches'- use this phrase at the beginning of your output. Keep your output to 200 words"}
#     ]

#     for image_path in image_paths:
#         base64_image = encode_image(image_path)
#         content.append({
#             "type": "image_url",
#             "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
#         })

#     payload = {
#         "model": "gpt-4o-mini",
#         "messages": [{"role": "user", "content": content}],
#         "max_tokens": 300
#     }

#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#     return response.json()

# if __name__ == '__main__':
#     os.makedirs('uploads', exist_ok=True)  # Create uploads directory if it doesn't exist
#     app.run(debug=True)
