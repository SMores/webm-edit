import subprocess
import uuid
import os
from typing import Dict, Any
from flask import Flask, Response, request, send_file
app = Flask(__name__)


@app.route('/crop', methods=['POST'])
def crop() -> Response:
    video = request.files['video']
    filename = os.path.join('tmp', str(uuid.uuid4().hex) + '.webm')
    video.save(filename)
    crop = request.values
    crop_video(crop, filename)
    return send_file(os.path.join('..', filename.split('.')[0] + '-cropped.webm'), mimetype='video/webm')


def subtitle() -> Response:
    video = request.files['video']
    filename = os.path.join('tmp', uuid.uuid4() + '.webm')
    video.save(filename)
    subtitles = request.values['subtitles']
    for sub in subtitles:
        video = add_subtitles(sub, filename)
    return send_file(os.path.join('..', filename), mimetype='video/webm')


def crop_video(crop: Dict[str, int], filename: str):
    crop_params = 'crop={}:{}:{}:{}'.format(crop['width'], crop['height'], crop['horizontal'], crop['vertical'])
    out_filename = filename.split('.')[0] + '-cropped.webm'
    subprocess.call(['ffmpeg', '-nostdin', '-y', '-i', filename, "-c:v",
                     "libvpx", '-qmin', '0', '-qmax', '40', "-crf", "10",
                     "-b:v", "1M", "-c:a", "libvorbis", '-threads', '4', '-vf',
                     crop_params, out_filename])


def add_subtitles(sub: Dict[str, Any], filename: str):
    return video
