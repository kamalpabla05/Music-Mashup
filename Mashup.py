import sys
import os
from googleapiclient.discovery import build
from pytube import YouTube
from pytube import Playlist
import moviepy.editor as mp 
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import AudioFileClip,concatenate_audioclips
import re
import random
import shutil

directory_v='Videos'
directory_a='Audios'
directory_t='Trim'

path=os.path.join(os.path.dirname(os.path.abspath(__file__)),directory_v)
opath=os.path.join(os.path.dirname(os.path.abspath(__file__)),directory_a)
tpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),directory_t)
mpath=os.path.dirname(os.path.abspath(__file__))

def generate_playlist_url(singer):
    youtube = build("youtube", "v3", developerKey="AIzaSyBL5eZvHecjOOLBD6HwLI5Cusj8DsCv2YI")
    request = youtube.search().list(
        part="id",
        type="playlist",
        q=singer,
        maxResults=1,
        fields="items(id(playlistId))"
    )
    response = request.execute()
    playlist_id = response["items"][0]["id"]["playlistId"]
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    return playlist_url

def download_video(link, n):
    playlist=Playlist(link)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    play_url=playlist.video_urls
    for i in range(0,n):
        play=random.choice(play_url)
        yt = YouTube(play, use_oauth=True, allow_oauth_cache=True)
        d_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        d_video.download(path)

def videotoaudio():
    for filename in os.listdir(path):
        if filename.endswith(".mp4"):
            clip = mp.VideoFileClip(r'{}'.format(os.path.join(path,filename)))
            audio_file = filename.replace(".mp4", ".mp3")
            clip.audio.write_audiofile(r'{}'.format(os.path.join(opath,audio_file)))

def trim(y):
    for filename in os.listdir(opath):
        if filename.endswith(".mp3"):
            ffmpeg_extract_subclip(os.path.join(opath, filename),0,y,targetname=os.path.join(tpath,'trim_'+filename))

def merge(output):
    files = [f for f in os.listdir(tpath) if f.endswith(".mp3")]
    ofile = AudioFileClip(os.path.join(tpath,files[0]))
    for file in files[1:]:
        ofile = concatenate_audioclips([ofile,AudioFileClip(os.path.join(tpath,file))])
        ofile.write_audiofile(r'{}'.format(os.path.join(mpath,output))) 

# def remove_dir():
#     shutil.rmtree(directory_v)
#     shutil.rmtree(directory_a)
#     shutil.rmtree(directory_t)

def main():
    if not os.path.exists(directory_v):
        os.mkdir(directory_v)

    if not os.path.exists(directory_a):
        os.mkdir(directory_a)

    if not os.path.exists(directory_t):
        os.mkdir(directory_t)

    if len(sys.argv) != 5:
        print("Arguments missing or not provided properly.\n Required input format- python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        exit()

    singer = sys.argv[1]
    n = int(sys.argv[2])
    y = int(sys.argv[3])
    output = sys.argv[4]
    
    try:
        link=generate_playlist_url(singer)
        print("Downloading in Progress....")
    except:
        print("The specified singer couldn't be found!!!")

    try:
        download_video(link,n) 
    except:
        print("Error while downloading videos!!!")

    try:
        videotoaudio()
    except:
        print("Unable to convert video to audio!!!")

    try:
        trim(y)
    except:
        print("Trimming of audio files failed!!!")
    
    try:
        merge(output)
    except:
        print("Couldn't merge the files!!!")

if __name__ == "__main__":
    main()
