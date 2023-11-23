import yt_dlp
from stopwatch import Stopwatch
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

url = 'https://music.youtube.com/playlist?list=PLGD_0JBel89PIs6XIYUFPtQNs0EOSfpds&si=Lo8TZcwMZevEQ_JV'

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }
    ],
    "outtmpl": {"default": "out/%(title)s.%(ext)s"}
}


def download_video(video_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading {video_url}: {e}")


def process_videos(video_urls):
    with ProcessPoolExecutor() as process_executor:
        process_executor.map(download_video, video_urls)


def extract_links(url):
    arr = []
    opts = {
        'quiet': False,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            videos = info_dict['entries']
        except yt_dlp.utils.DownloadError as e:
            print(f"Error extracting playlist information: {e}")
            exit()

        for video in videos:
            video_url = video['url']
            arr.append(video_url)
            print(f"Video URL: {video_url}")
    return arr


if __name__ == "__main__":
    stopwatch = Stopwatch(2)
    stopwatch.start()

    links = extract_links(url)

    with ThreadPoolExecutor() as thread_executor:
        thread_executor.map(
            process_videos, [links[i:i+5] for i in range(0, len(links), 5)])

    stopwatch.stop()
    print("It took %d seconds to download %d songs." %
          (stopwatch.duration, len(links)))
