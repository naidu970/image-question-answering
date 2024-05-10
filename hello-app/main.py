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
		img = request.files['my_image']

		# img_path = "static/" + img.filename	
		# img.save(img_path)
		bytes_data = img.stream.read()
		try :
			image = Image.open(io.BytesIO(bytes_data))
			extracted_text  = pytesseract.image_to_string(image, lang=lang)
			text = predict_answer(extracted_text)
		except :
			text = "Invalid Format"
	return render_template("index.html", extracted_text =extracted_text ,prediction = text)#, img_path = img_path)



if __name__=="__main__":
    app.run(host="127.0.0.1",port =4000,debug=True)