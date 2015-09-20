from subprocess import call
from os.path import basename

json = {
  # "video": @file.webm,
  "subtitles": [ {
    "text": "Ayyyyy lmao",
    "start_time": 4, # in milliseconds
    "end_time": 12 # in milliseconds
  }]
}

def create_srt(json):
    with open(json["video"].name + ".srt", 'w') as f:
        # print f
        for sub,i in zip(json["subtitles"],range(1,len(json["subtitles"])+1)):
            f.write(str(i) + "\n")
            milli_start = sub["start_time"] % 1000
            sub["start_time"] /= 1000
            minutes_start = sub["start_time"] / 60
            seconds_start = sub["start_time"] % 60
            milli_end = sub["end_time"] % 1000
            sub["end_time"] /= 1000            
            minutes_end = sub["end_time"] / 60
            seconds_end = sub["end_time"] % 60
            f.write("00:" + pad_int_to_str(minutes_start) + ":" + \
                            pad_int_to_str(seconds_start) + "," + \
                            pad_milliseconds(milli_start) + \
                " --> 00:"+ pad_int_to_str(minutes_end) + ":" + \
                            pad_int_to_str(seconds_end) + "," + \
                            pad_milliseconds(milli_end) + "\n")
            f.write(sub["text"] + "\n\n")
        return json["video"].name + ".srt"

def pad_milliseconds(i):
    if i >= 100:
        return str(i)[:3]
    if i >= 10:
        return "0" + str(i)[:2]
    return "00" + str(i)[:1]

def pad_int_to_str(i):
    if i >= 10:
        return str(i)[:2]
    return "0" + str(i)[:1]

def merge_webm_srt(json):
    srt = create_srt(json)
    command = "ffmpeg -nostdin -y -i " + json["video"].name + " -codec:v libvpx -qmin 0 -qmax 50 -crf 5 -b:v 1M -c:a libvorbis -vf " + \
              "subtitles=" + srt + " out.webm"
    # print(command)
    call(command.split())
    return command

if __name__ == '__main__':
    j = {
        "video":open("dog.webm"),
        "subtitles" : [
            {"start_time": 0, "end_time" : 2000, "text": "waggy waggy waggy waggy"},
            {"start_time": 3321, "end_time" : 5123, "text": "shaggy"},
            {"start_time": 6471, "end_time" : 9583, "text": "taggy"},
            {"start_time": 9879, "end_time" : 10111, "text": "maggy"},
            {"start_time": 10537, "end_time" : 11452, "text": "4real?"},
            {"start_time": 11567, "end_time" : 14000, "text": "such creativity bruh"},
            {"start_time": 14050, "end_time" : 15001, "text": "pen"}
        ]}
    print(merge_webm_srt(j))

