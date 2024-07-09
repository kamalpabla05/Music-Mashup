# Music-Mashup
In this project we are making a mashup of n audio files using the following steps:
i) First, we are randomly downloading N videos of X singer from “Youtube”
ii) Then we are convert all the videos to audio and cut first Y sec audios from all downloaded files.
iii) At last we are merging all audios to make a single output file (mp3).

The syntax to run the file is (5 input parameters): python ScriptName SingerName NumberOfVideos AudioDuration(in sec) OutputFileName(in mp3 format)
Eg: python Mashup.py "Taylor Swift" 3 60 Mashup.mp3 (Mashup.mp3 will be the merged output file).
