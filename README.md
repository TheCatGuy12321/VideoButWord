# VideoButWord
Cuts a video so that only a specified word is said

Usage: (in terminal)
python VideoButWord.py (video name e.g. test1, not test1.mp4) (word to filter for)

Video should be stored in Inputs/ and the inputted video name shouldn't contain the file extension. currently only mp4 is supported

ffmpeg-split.py is used to split videos that are too long (30 mins+ should be split as ffmpeg can't handle them)
Full credit to: 
https://github.com/c0decracker/video-splitter/tree/master
for it.

Usage is in python file, at the top in comments.
