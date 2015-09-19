from flask import Flask 
from flask import Response, request, jsonify
app = Flask(__name__)


@app.route('/add_subtitles', methods=['POST'])
def index() -> Response:
    with request.files['video'] as video:
        subtitles = request.values['subtitles']
        for sub in subtitles:
            video = add_subtitles(video, sub)
    return jsonify(video=video)


def add_subtitles(video, sub):
    return video
