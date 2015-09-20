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
    command = "ffmpeg -nostdin -y -i " + json["video"].name + " -codec:v libvpx -vf " + \
              "subtitles=" + srt + " out.webm"
    # print(command)
    # call(command.split())
    return command

if __name__ == '__main__':
    j = {
        "video":open("morty.webm"),
        "subtitles" : [
            {"start_time": 0, "end_time" : 3000, "text": "ayyy"},
            {"start_time": 4321, "end_time" : 7123, "text": "ayyy"},
            {"start_time": 9471, "end_time" : 13583, "text": "ayyy"},
            {"start_time": 15879, "end_time" : 16111, "text": "ayyy"},
            {"start_time": 20537, "end_time" : 30452, "text": "ayyy"},
            {"start_time": 105675, "end_time" : 120001, "text": "ayyy"}
        ]}
    print(merge_webm_srt(j))

