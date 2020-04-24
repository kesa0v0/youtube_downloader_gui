import asyncio


import youtube_dl
import os


class Download:
    def __init__(self):
        self.is_login = False  # 로그인 여부
        self.id = ""  # 로그인 id, 비번
        self.pwd = ""


        self.link = ""
        self.format = ""
        self.output_path = "./result"

        self.subtitle = False  # 자막 여부
        self.subtitle_lang = ""  # 자막 언어
        self.thumbnail = False  # 썸네일 다운로드 여부

        self.is_custom_name = False
        self.custom_name = ""

        self._is_audio = False

    def _check(self):
        # TODO: check if args is right
        # TODO: make new class Exception

        if self.is_custom_name:
            if self.custom_name == "":
                raise Exception("Invalid file name")

        if self.format == "bestaudio/best":
            self._is_audio = True

        if self.output_path == "":
            if not (os.path.isdir("./result")):
                os.makedirs("./result")

            self.output_path = "./result"
        elif self.output_path.endswith("/"):
            self.output_path = self.output_path[:-1]

    def _isfile_exist(self):
        # TODO: check if file already exists
        pass

    def _getYoutube(self):
        self.opts = {}

        if self.is_login:
            self.opts['username'] = self.id
            self.opts['password'] = self.pwd

        if self.subtitle:
            self.opts['writesubtitles'] = 'best'
            self.opts['subtitleslangs'] = self.subtitle_lang

        if self.thumbnail:
            self.opts['writethumbnail'] = 'best'

        if self.is_custom_name:
            self.opts['outtmpl'] = self.output_path + f"\\{self.custom_name}.{'mp3' if self._is_audio else 'mp4'}"
        else:
            self.opts['outtmpl'] = self.output_path + f"\\%(title)s-%(id)s.{'mp3' if self._is_audio else 'mp4'}"

        if self._is_audio:
            self.opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': f'mp3',
                'preferredquality': '192',
            }]
            self.opts['prefer_ffmpeg'] = True

        self.opts['format'] = self.format

        return youtube_dl.YoutubeDL(self.opts)

    async def async_download(self):
        self._check()

        try:
            with self._getYoutube() as ydl:
                ydl.download([self.link])

            return True

        except Exception as e:
            import logging

            logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
            logging.exception(f"Cannot downloaded link: {self.link}")

            return Exception

    def download(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_download())
        loop.close()