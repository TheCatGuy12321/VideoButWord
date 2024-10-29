import ffmpeg
from os import path, remove
import whisper_timestamped as whisper
from sys import argv
import datetime
from moviepy.editor import concatenate_videoclips, VideoFileClip

if len(argv) != 3:
    print(f"usage: {argv[0]} VIDEO WORD\nVIDEO should be in the folder Inputs.\nDon't input relative path e.g. Inputs/test.mp4, input the name for the video e.g. test")
    quit()

WORD = argv[2]

FILE_NAME = argv[1] # file name

VIDEO_FILE = path.abspath("Inputs/%s.mp4"%FILE_NAME)

# Transcribe audio
result = whisper.transcribe("tiny", VIDEO_FILE)

CustomTranscipt = ""

for segment in result['segments']:
    words = segment['words']
    for j in words:
        start, end = j['start'], j['end']
        CustomTranscipt += f"{start}:{end}:{j['text'].strip()}\n"


StrToSave = "" # Cut transcript

for line in CustomTranscipt.splitlines():
    linesSep = line.split(":")
    if linesSep[2] == WORD:
        StrToSave += line + "\n"

# Trim video

vidL = []
Iter = 0 # temporary iterator
for line in StrToSave.splitlines():
    Iter += 1
    linesSep = line.split(":")
    start = str(datetime.timedelta(seconds=float(linesSep[0])))
    end = str(datetime.timedelta(seconds=float(linesSep[1])+0.1))
    outpath = path.abspath(f"Trimmed/{Iter}.mp4")
    if path.exists(outpath):
        remove(outpath)
    ffmpeg.input(f"Inputs/{argv[1]}.mp4", ss=start, to=end).output(outpath, loglevel="error").run()
    vidL.append(outpath)

def concatenate(video_clip_paths, output_path):
    # create VideoFileClip object for each video file
    clips = [VideoFileClip(c) for c in video_clip_paths]
    final_clip = concatenate_videoclips(clips, method="compose")
    # write the output video file
    final_clip.write_videofile(output_path)

# Concatenate everything
OUT_FILE3 = path.abspath(f"Outputs/{FILE_NAME}.mp4")
if path.exists(OUT_FILE3): remove(OUT_FILE3)
concatenate(vidL, OUT_FILE3)

# Remove the trimmed parts to save disk space
for line in StrToSave.splitlines():
    if path.exists(outpath):
        remove(outpath)