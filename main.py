#import flask core modules
from flask import Flask, render_template, request
#impirt qr code library
import qrcode
#handle file paths and folders
import os

#flask is a library which hanlde webh requets, return responses, run web server

#create a flask web app and store it in the variable app
#__name__ is bulit in python variable
app = Flask(__name__)

#create a folder to store generated qr codes
QR_FOLDER = "static/qr_codes" #string represent folder path

#if folder not created, create it
#makedirs create folder, exist_ok=True means if folder already exists, do not raise error
os.makedirs(QR_FOLDER, exist_ok=True)

#HOME ROUTE
#handles:
# GET - displaying home page with form to input data for qr code
# POST - processing form submission, generating qr code, displaying result
#when someone visit home page run the function below and allow both GET and POST requests
#@app.route(...) is decorator, it connects a URL to a python function
#"/" this is the route (path)
@app.route("/", methods=["GET", "POST"])

#   flow:
#       1. User opens the page → GET
#       2. Flask shows the page
#       3. User submits form → POST
#       4. Flask processes the data

def index():

    #variable to store generated QR filename
    qr_image = None

    #check if form is submited
    #flask, represent the current HTTP request
    if request.method == "POST":

        #get the url name entered by user in form
        # (request.form contains all data sent via POST form submission)
        # (.get fetch the value of name qr_text)
        data = request.form.get("qr_text")

        #create QR only if input is not empty
        if data:

            #create a qr object
            qr = qrcode.QRCode(
                version = 1, #control QR size (1 - smallest QR (21×21 grid))
                error_correction=qrcode.constants.ERROR_CORRECT_L, #how much damage qr can handle
                # L- about 7% recovery, others - M,Q,H (more safery, bigger qr)
                box_size = 10, #size of each QR box
                border = 4 #Border thckness
            )

            #add user data, user url name
            qr.add_data(data)

            #build the qr code
            qr.make(fit=True)#auto-adjusts QR size if needed

            #convert QR to image
            img = qr.make_image(
                fill_color="black",
                back_color = "white"
            )

            #File name for generated QR
            qr_image = "qrcode.png"

            #save qr image to static folder
            img.save(os.path.join(QR_FOLDER, qr_image))

        
    # end QR filename to HTML page
    return render_template("index.html", qr_image=qr_image)



#run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
