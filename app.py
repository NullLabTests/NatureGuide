import os
from flask import Flask, render_template, request, jsonify
import gradio as gr
from openai import OpenAI
import base64
import mimetypes
from dotenv import load_dotenv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

load_dotenv()  # Load environment variables from .env if it exists

XAI_API_KEY = os.getenv('XAI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=XAI_API_KEY or OPENAI_API_KEY,
    base_url="https://api.x.ai/v1" if XAI_API_KEY else "https://api.openai.com/v1"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/identify', methods=['POST'])
def identify():
    file = request.files['file']
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in ['image/jpeg', 'image/png']:
            return jsonify({"error": "File type not supported"}), 400

        with open(file_path, 'rb') as img_file:
            b64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64_image}",
                            "detail": "high",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Identify this species and provide some interesting facts about it.",
                    },
                ],
            },
        ]
        
        try:
            completion = client.chat.completions.create(
                model="grok-2-vision-latest" if XAI_API_KEY else "gpt-4-vision-preview",
                messages=messages,
                temperature=0.01,
            )
            identification = completion.choices[0].message.content

            # Check if the identification result indicates it's not a species
            if "not a species" in identification.lower() or "human" in identification.lower():
                identification = "The image depicts humans. Here are some interesting facts about humans:\n\n- Humans are among the few species capable of laughter.\n- The human body contains enough carbon to make 900 pencils.\n- Human DNA is 99.9% identical from one individual to the next."

            return jsonify({"identification": identification})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

def gradio_interface():
    def identify_species(image):
        # Here we simulate sending the image through Flask
        # but in practice, you would directly use the API
        with open('temp_image.png', 'wb') as f:
            f.write(image)
        
        with open('temp_image.png', 'rb') as img_file:
            b64_image = base64.b64encode(img_file.read()).decode('ascii')
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}",
                            "detail": "high",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Identify this species and provide some interesting facts about it.",
                    },
                ],
            },
        ]
        
        try:
            completion = client.chat.completions.create(
                model="grok-2-vision-latest" if XAI_API_KEY else "gpt-4-vision-preview",
                messages=messages,
                temperature=0.01,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    iface = gr.Interface(
        fn=identify_species,
        inputs=gr.Image(type="filepath", label="Upload an Image"),
        outputs="text",
        title="NatureGuide: Species Identification",
        description="Upload an image to identify and learn about species in nature."
    )
    iface.launch()

# To run only Gradio interface
if __name__ == '__main__':
    gradio_interface()
