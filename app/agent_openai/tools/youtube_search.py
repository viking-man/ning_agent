from youtubesearchpython import VideosSearch
import webbrowser
from langchain.tools import tool
import os
import subprocess


class YoutubeSearch:

    @tool
    def search_and_play(video_name: str):
        """当用户需要播放视频时调用这个方法，参数video_name表示需要播放视频名称。通过youtube网页搜索并播放指定的视频内容，执行后返回已播放信息给用户。
        This method is called when the user needs to play a video, the parameter video_name indicates the name of the video to be played. Search and play the specified video content through youtube webpage, and return the played information to the user after execution.
        """
        videos_search = VideosSearch(video_name, limit=1)
        results = videos_search.result()
        if results['result']:
            first_result_url = results['result'][0]['link']
            webbrowser.open(first_result_url)

        return f'A video featuring {video_name} has been played'

    def play_music_with_default_player(song_path: str):
        """通过系统默认的播放器播放给定的歌曲文件song_path"""
        if os.path.exists(song_path):
            # 在Windows系统中
            if os.name == 'nt':
                os.startfile(song_path)
            # 在Unix/Linux系统中
            elif os.name == 'posix':
                subprocess.call(['open', song_path])
        else:
            print(f"File not found: {song_path}")


if __name__ == "__main__":
    # Replace with the video you want to search for
    YoutubeSearch.search_and_play({'video_name': "Never gonna give you up"})
