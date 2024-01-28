import logging
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
from langchain.tools import tool

music_directory = "/Users/viking/song/"

template = ('你是一个聪明的歌曲选择AI助手，用户会要求播放一首歌，你首先进行本地音乐搜索，如果本地有这首歌的话，直接进行播放。'
            '如果本地没有，通过工具【1】搜索线上的歌曲链接，下载符合要求的歌曲，然后播放。')

songs_path = '/Users/viking/song/'


class SpotifySearch:

    @tool
    def download_song(song_url: str):
        """用于下载本地不存在的音乐文件，需要的参数分别为歌曲在spotify的song_url和保存歌曲的目录song_directory"""
        command = ['spotdl', song_url, '--output', music_directory]
        subprocess.run(command)

    @tool
    def search_spotify_music(track_name: str):
        """搜索歌曲在spotify上的歌手名称和对应的url，格式为[{"artist:url"}]"""
        # Set up credentials
        client_credentials_manager = SpotifyClientCredentials(client_id="55ed24ee34534fe48d11b0795f378482",
                                                              client_secret="1128b4939fbd45e0969319d9bbee5575")
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Search for a song
        results = sp.search(q=track_name, limit=3)
        songs = []
        for idx, item in enumerate(results['tracks']['items']):
            songs.append({item['artists'][0]['name']: item['external_urls']['spotify']})
        return songs

    # 搜索本地音乐库
    @tool
    def search_local_music(song_name: str):
        """搜索给定目录music_directory是否包含指定的歌曲song_name"""
        for root, dirs, files in os.walk(music_directory):
            for file in files:
                if song_name.lower() in file.lower():
                    return os.path.join(root, file)
        return None

    # 主程序
    @tool
    def search_download_songs(song_name: str, artist: str):
        """搜索给定目录music_directory是否包含对应的歌曲，如果本地存在，直接播放；如果本地不存在，从spotify上搜索并下载。
        如果指定歌手artist，下载对应歌手的歌曲，如果未指定，默认下载第一首。"""

        local_song_path = SpotifySearch.search_local_music(song_name)
        if local_song_path:
            print(f"Playing local song->{local_song_path}")
            # play_local_music(local_song_path)
            SpotifySearch.play_music_with_default_player(local_song_path)
            return None
        else:
            songs = SpotifySearch.search_spotify_music(song_name)
            if len(songs) > 0:
                logging.info(f"Song found on Spotify,songs->{songs}")
                # 这里可以添加代码来处理Spotify的音乐，比如添加到用户的Spotify库中
                # download spotify todo 如果出自两个以上艺术家，需要用户选择
                if artist:
                    for item in songs:
                        song = item.get(artist)
                        if song:
                            SpotifySearch.download_song(song)
                            break
                first_song = next(iter(songs[0].values()))
                SpotifySearch.download_song(first_song)
            else:
                logging.info(f"Song not found->{song_name}")
        # 重新搜索播放
        SpotifySearch.search_play_song(music_directory, song_name)

    def search_play_song(music_directory: str, song_name: str):
        local_song_path = SpotifySearch.search_local_music(song_name)
        if local_song_path:
            print(f"Playing local song->{local_song_path}")
            # play_local_music(local_song_path)
            SpotifySearch.play_music_with_default_player(local_song_path)

    @tool
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

    # 需要spotify会员
    def play_direct_spotify(song: str):
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth

        # Set up Spotipy with user authorization
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="your spotify app client_id",
                                                       client_secret="your spotify app client_secret",
                                                       redirect_uri="your app rediect_uri",
                                                       scope="user-read-playback-state,user-modify-playback-state"))

        # Search for a track
        track_name = song
        results = sp.search(q=track_name, limit=1, type='track')
        track_uri = results['tracks']['items'][0]['uri']
        # Play the track
        sp.start_playback(uris=[track_uri])


if __name__ == '__main__':
    # 运行主程序
    # 请将下面的 "/path/to/your/music/directory" 替换为您的音乐目录路径
    # main("When We Were Young", "/Users/viking/song")
    # main("Next Level", "/Users/viking/song")
    SpotifySearch.search_download_songs({"song_name": "Spicy", "artist": "aespa"})
    # play_direct_spotify("Spicy")
