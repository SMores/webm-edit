from subprocess import call
from os.path import basename

json = {
  # "video": @file.webm,
  "subtitles": [ {
    "text": "Ayyyyy lmao",
    "start_time": 4,
    "end_time": 12
  }]
}

def create_srt(json):
    with open(json["video"].name + ".srt", 'w') as f:
        # print f
        for sub,i in zip(json["subtitles"],xrange(1,len(json["subtitles"])+1)):
            f.write(str(i) + "\n")
            minutes_start = sub["start_time"] / 60
            seconds_start = sub["start_time"] % 60
            minutes_end = sub["end_time"] / 60
            seconds_end = sub["end_time"] % 60
            f.write("00:" + pad_int_to_str(minutes_start) + ":" + pad_int_to_str(seconds_start) + ",000" + \
            " --> 00:" + pad_int_to_str(minutes_end) + ":" + pad_int_to_str(seconds_end) + ",000\n")
            f.write(sub["text"] + "\n\n")
        return json["video"].name + ".srt"

def pad_int_to_str(i):
    if i >= 10:
        return str(i)
    return "0" + str(i)

def merge_webm_srt(json):
    srt = create_srt(json)
    command = "ffmpeg -nostdin -y -i " + json["video"].name + " -codec:v libvpx -vf " + \
              "subtitles=" + srt + " out.webm"
    print command
    call(command.split())
    return command

if __name__ == '__main__':
    j = {
        "video":open("0b1"),
        "subtitles" : [
            {"start_time": 0, "end_time" : 3, "text": "ayyy"},
            {"start_time": 4, "end_time" : 7, "text": "ayyy"},
            {"start_time": 9, "end_time" : 13, "text": "ayyy"},
            {"start_time": 15, "end_time" : 16, "text": "ayyy"},
            {"start_time": 20, "end_time" : 30, "text": "ayyy"},
            {"start_time": 105, "end_time" : 120, "text": "ayyy"}
        ]}
    print merge_webm_srt(j)

