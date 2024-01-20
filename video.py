from library import *

def download_youtube_video(url: str, outpath: str = "./"):

    yt = YouTube(url)

    yt.streams.filter(file_extension="mp4").get_by_resolution("720p").download(outpath)

    start_time = 2.3*60 
    end_time = 2.6*60
    ffmpeg_extract_subclip('/content/Câmera ao vivo em Tokyo Shinjuku (Japão) -  2021.mp4', start_time, end_time, targetname=Config.infe_video)
    os.remove('/content/Câmera ao vivo em Tokyo Shinjuku (Japão) -  2021.mp4')


download_youtube_video(url='https://www.youtube.com/watch?v=9rPmjIrvYAM')