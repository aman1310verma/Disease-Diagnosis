from flask import Flask,render_template, url_for ,flash , redirect
from sklearn.externals import joblib
from flask import request
import numpy as np



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
import os
from flask import send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
model222=load_model("my_model.h5")

dir_path = os.path.dirname(os.path.realpath(__file__))
# UPLOAD_FOLDER = dir_path + '/uploads'
# STATIC_FOLDER = dir_path + '/static'
UPLOAD_FOLDER = 'uploads'


def api1(full_path):
    data = image.load_img(full_path, target_size=(64, 64, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    predicted = model222.predict(data)
    return predicted
@app.route('/upload11', methods=['POST','GET'])       #for pneumonia
def upload11_file():


    file = request.files['image']
    full_name = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(full_name)
    indices = {0: 'Normal', 1: 'Pneumonia'}
    result = api1(full_name)
    if(result>50):
        return render_template("Normal.html")
    else:
        return render_template("unhealthy.html")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/diabetes")
def diabetes():
    return render_template("diabetes.html")

@app.route("/heart")
def heart():
    return render_template("heart.html")

@app.route("/liver")
def liver():
    return render_template("liver.html")


@app.route("/Pneumonia")
def Pneumonia():
    return render_template("pneumonia.html")


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==8):#Diabetes
        loaded_model = joblib.load("model1")
        result = loaded_model.predict(to_predict)
    elif(size==10):  #liver
        loaded_model = joblib.load("model4")
        result = loaded_model.predict(to_predict)
    elif(size==11):#Heart
        loaded_model = joblib.load("model2")
        result =loaded_model.predict(to_predict)
    return result[0]


#loading the models
@app.route('/result',methods = ["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))

        if(len(to_predict_list)==8):#Daiabtes
            result = ValuePredictor(to_predict_list,8)
        elif(len(to_predict_list)==12): #kidney
            result = ValuePredictor(to_predict_list,12)
        elif(len(to_predict_list)==11):   #heart
            result = ValuePredictor(to_predict_list,11)
        elif(len(to_predict_list)==10):    #liver
            result = ValuePredictor(to_predict_list,10)
    if (int(result) == 1):
        return render_template("unhealthy.html")
    else:
        return render_template("Normal.html")


if __name__ == "__main__":
    app.run(debug=True)