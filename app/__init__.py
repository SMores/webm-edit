import subprocess
import uuid
import os
from typing import Dict, Any, List
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


@app.route('/subtitle', methods=['POST'])
def subtitle() -> Response:
    video = request.files['video']
    filename = os.path.join('tmp', uuid.uuid4() + '.webm')
    video.save(filename)
    subtitles = request.values['subtitles']
    add_subtitles(subtitles, filename)
    return send_file(os.path.join('..', filename.split('.')[0] + '-subbed.webm'), mimetype='video/webm')


def crop_video(crop: Dict[str, int], filename: str):
    crop_params = 'crop={}:{}:{}:{}'.format(crop['width'], crop['height'], crop['horizontal'], crop['vertical'])
    out_filename = filename.split('.')[0] + '-cropped.webm'
    subprocess.call(['ffmpeg', '-nostdin', '-y', '-i', filename, "-c:v",
                     "libvpx", '-qmin', '0', '-qmax', '40', "-crf", "10",
                     "-b:v", "1M", "-c:a", "libvorbis", '-threads', '4', '-vf',
                     crop_params, out_filename])


def create_srt(subtitles: List[Dict[str, Any]], filename: str) -> str:
    for sub, i in zip("subtitles", range(1, len("subtitles") + 1)):
        f.write(str(i) + "\n")
        milli_start = sub["start_time"] % 1000
        sub["start_time"] /= 1000
        minutes_start = sub["start_time"] / 60
        seconds_start = sub["start_time"] % 60
        milli_end = sub["end_time"] % 1000
        sub["end_time"] /= 1000            
        minutes_end = sub["end_time"] / 60
        seconds_end = sub["end_time"] % 60
        f.write("00:{0:02d}:{0:02d},{0:03d} --> 00:{0:02d}:{0:02d},{0:03d}\n".format(
                minutes_start, seconds_start, milli_start, minutes_end, seconds_end, milli_end))
        f.write(sub["text"] + "\n\n")
    return filename + ".srt"


def add_subtitles(subtitles: List[Dict[str, Any]], filename: str):
    srt_filename = create_srt(subtitles, filename)
    command = "ffmpeg -nostdin -y -i {0} -codec:v libvpx -qmin 0 -qmax 50 -crf 5 -b:v 1M -c:a libvorbis -vf " + \
              "subtitles={1} {2}.webm".format(filename, srt_filename, filename.split('.')[0] + '-subbed.webm')
    subprocess.call(command.split())
