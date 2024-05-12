from flask import Flask, render_template, request
import requests
from PIL import Image
import io
import base64
from gradio_client import Client


import requests
app = Flask(__name__)

lang = 'eng'  
API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-7b-it"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def predict_answer(extracted_text):
	try:
		client = Client("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/")
		result = client.predict(extracted_text, [["Hello!", "null"]], "Hello!!", api_name="/model_chat")
		text = result[1][1][1]
	except:
		output = query({"inputs":extracted_text,})
		text =  output[0]['generated_text'].replace(extracted_text,"")
	return text

def upload_image(image_data):
    # Your ImgBB API key
    api_key = '2523d847e1c1653a9a342bda87acb27d'

    # Endpoint URL for image upload
    upload_url = "https://api.imgbb.com/1/upload"

    # Prepare the data for the POST request
    payload = {
        "key": api_key,
        "image": image_data.decode('utf-8')  
    }

    # Make the POST request to upload the image
    response = requests.post(upload_url, payload)

    # Parse the JSON response
    json_response = response.json()

    if 'data' in json_response:
        image_url = json_response['data']['url']
        return image_url
    else:
        return json_response.get('error', {}).get('message', 'Unknown error')


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "Naidu"

@app.route("/process_edit", methods=['POST'])
def process_edit():
    uploaded_image_url = request.form['uploaded_image_url']
    extracted_text = request.form['edited_text']
    text = predict_answer(extracted_text)
    return render_template("index.html",  extracted_text =extracted_text ,uploaded_image_url=uploaded_image_url,prediction = text)


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	text = "Upload image in any the following format : Png/Jpg/Jpeg"
	extracted_text =" "
	if request.method == 'POST':
	
		try :
	
			extracted_text = request.files['my_image']
			extracted_text= extracted_text.stream.read()
		
			base64_image = base64.b64encode((extracted_text))
			uploaded_image_url = upload_image(base64_image)
			client = Client("https://naiduml-tessa-py-api-dhejfgeufgeufgeygfegfeugfefg.hf.space/")
			extracted_text = client.predict(uploaded_image_url, ["eng"], api_name="/tesseract-ocr")
			text = predict_answer(extracted_text)
		except :
			text = "Invalid Format"
			extracted_text = "Upload image in any the following format : Png/Jpg/Jpeg or Enter Text Here and click on Submit"
			uploaded_image_url =" "
	
	return render_template("index.html", extracted_text =extracted_text ,uploaded_image_url=uploaded_image_url,prediction = text)



if __name__=="__main__":
    app.run(debug=True)
