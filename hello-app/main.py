from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import io

import requests

app = Flask(__name__)

lang = 'eng'  
API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-7b-it"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def predict_answer(text):
	output = query({"inputs": f"detect question and answer all questions with only answers"+text,})
	return output[0]['generated_text'].replace(f"detect question and answer all questions with only answers"+text,"")




# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "Naidu"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	text = "Upload image in any the following format : Png/Jpg/Jpeg"
	extracted_text =" "
	if request.method == 'POST':
		#img = request.files['my_image']

		#img_path =  img.filename	
		#img.save(img_path)
		#bytes_data = img.stream.read()
	
		try :
			extracted_text = request.files['my_image']
			extracted_text= extracted_text.stream.read()
			img = Image.open(io.BytesIO(extracted_text))
			extracted_text  = "who was the president of india in 2023"#pytesseract.image_to_string(img, lang=lang)
			text = predict_answer(extracted_text)
		except :
			text = "Invalid Format"
			extracted_text = "Upload image in any the following format : Png/Jpg/Jpeg"
	
	return render_template("index.html", extracted_text =extracted_text ,prediction = text)#, img_path = img_path)



if __name__=="__main__":
    app.run(debug=True)
