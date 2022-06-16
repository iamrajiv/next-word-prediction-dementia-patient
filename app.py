import flask
from flask import Flask, request, render_template
import json
import main
import speech_recognition as sr
r = sr.Recognizer()
app = Flask(__name__)


@app.route('/')
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/', methods=['POST'])
def get_audio():
    # get the file
    file = request.files['file']
    # save the file
    filename = file.filename
    file.save(filename)
    print(filename)
    # return a response
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)
        text = text + " "
        return render_template('index.html', text=text)


@app.route('/get_end_predictions', methods=['post'])
def get_prediction_eos():
    try:
        input_text = ' '.join(request.json['input_text'].split())
        input_text += ' <mask>'
        top_k = request.json['top_k']
        res = main.get_all_predictions(input_text, top_clean=int(top_k))
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


@app.route('/get_mask_predictions', methods=['post'])
def get_prediction_mask():
    try:
        input_text = ' '.join(request.json['input_text'].split())
        top_k = request.json['top_k']
        res = main.get_all_predictions(input_text, top_clean=int(top_k))
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=False)
