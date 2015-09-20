import subprocess
import uuid
import os
import json
from typing import Dict, Any, List
from flask import Flask, Response, Request, request, send_file
app = Flask(__name__)


@app.after_request
def after_request(request: Request) -> Request:
    for the_file in os.listdir('tmp'):
        file_path = os.path.join('tmp', the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    return request


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
    print(request.values)
    video = request.files['video']
    filename = os.path.join('tmp', str(uuid.uuid4().hex) + '.webm')
    video.save(filename)
    subtitles = json.loads(request.values['subtitles'])
    optimize = bool(request.values['optimize'])
    add_subtitles(subtitles, filename, optimize)
    return send_file(os.path.join('..', filename.split('.')[0] + '-opt.gif'), mimetype='image/gif')


def crop_video(crop: Dict[str, int], filename: str):
    crop_params = 'crop={}:{}:{}:{}'.format(crop['width'], crop['height'], crop['horizontal'], crop['vertical'])
    out_filename = filename.split('.')[0] + '-cropped.webm'
    subprocess.call(['ffmpeg', '-nostdin', '-y', '-i', filename, "-c:v",
                     "libvpx", '-qmin', '0', '-qmax', '40', "-crf", "10",
                     "-b:v", "1M", "-c:a", "libvorbis", '-threads', '4', '-vf',
                     crop_params, out_filename])


def create_srt(subtitles: List[Dict[str, Any]], filename: str) -> str:
    srt_filename = filename.split('.')[0] + '.srt'
    with open(srt_filename, 'w') as f:
        for i, sub in enumerate(subtitles):
            f.write(str(i) + "\n")
            milli_start = sub["start_time"] % 1000
            sub["start_time"] //= 1000
            minutes_start = sub["start_time"] // 60
            seconds_start = sub["start_time"] % 60
            milli_end = sub["end_time"] % 1000
            sub["end_time"] //= 1000
            minutes_end = sub["end_time"] // 60
            seconds_end = sub["end_time"] % 60
            f.write("00:{0:02d}:{1:02d},{2:03d} --> 00:{3:02d}:{4:02d},{5:03d}\n".format(
                    minutes_start, seconds_start, milli_start, minutes_end, seconds_end, milli_end))
            f.write(sub["text"] + "\n\n")
    return srt_filename


def add_subtitles(subtitles: List[Dict[str, Any]], filename: str, optimize: bool):
    srt_filename = create_srt(subtitles, filename)
    ffmpeg = ("ffmpeg -nostdin -y -i {0} -vf subtitles={1} -pix_fmt rgb24 {2}").format(filename, srt_filename, filename.split('.')[0] + '-subbed.gif')
    convert = ("convert {0} -coalesce -layers OptimizeFrame {1}").format(filename.split('.')[0] + '-subbed.gif', filename.split('.')[0] + '-frame-opt.gif')
    gifsicle = ("gifsicle -O2 {0} -o {1}").format(filename.split('.')[0] + '-frame-opt.gif', filename.split('.')[0] + '-opt.gif')
    subprocess.call(ffmpeg.split())
    if optimize:
        print('Optimizing!')
        subprocess.call(convert.split())
        subprocess.call(gifsicle.split())
