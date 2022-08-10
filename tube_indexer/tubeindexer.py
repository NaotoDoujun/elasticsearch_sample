# -*- coding: utf-8 -*-
import os, shutil, glob, json, sys, datetime
from natsort import natsorted
from apiclient.discovery import build
from yt_dlp import YoutubeDL
import librosa
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_inference import Speech2Text
from elasticsearch import Elasticsearch, helpers
from logging import Formatter, getLogger, StreamHandler, DEBUG
import config

class TubeIndexer:
    """
      YouTube Indexer
      
      Attributes
      ----------
      youtube : 
          YouTube Data API
      speech2text : 
          ESPNet
      logger : 
          Logger
      es :
          Elasticsearch Client
    """

    def __init__(self, name=__name__):
        self.youtube = build(
          config.YOUTUBE_API_SERVICE_NAME, 
          config.YOUTUBE_API_VERSION, 
          developerKey = config.API_KEY)

        d = ModelDownloader("~/.cache/espnet")
        self.speech2text = Speech2Text(
          **d.download_and_unpack(config.ESPNET_MODEL))

        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        if not self.logger.hasHandlers():
          sh = StreamHandler()
          sh.setLevel(DEBUG)
          sh.setFormatter(Formatter("[%(name)s] %(message)s"))
          self.logger.addHandler(sh)

        self.es = Elasticsearch(config.ES_ENDPOINT, request_timeout=100)

    def convert_size(self, size, unit="B"):
      """
      Convert Size
      """
      units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
      i = units.index(unit.upper())
      size = round(size / 1024 ** i, 2)
      return f"{size} {units[i]}"

    def make_es_index(self, index, setting_file_path, mapping_file_path, recreate=False):
      """
      Make Elasticsearch Index
      """
      if recreate and self.es.indices.exists(index=index):
        self.es.indices.delete(index=index)
        
      if not self.es.indices.exists(index=index):
        with open (setting_file_path) as fs:
          setting = json.load(fs)
          with open(mapping_file_path) as fm:
              mapping = json.load(fm)
              self.es.indices.create(index=index, mappings=mapping, settings=setting)

    def exists(self, index, videoid):
      """
      Check Target videoid document exists
      """
      return self.es.exists(index=index, id=videoid)

    def do_clear_cache(self, videoid):
      """
      Clear Target videoid video/audio files
      """
      os.remove('videos/{}.mp4'.format(videoid))
      os.remove('audios/{}.wav'.format(videoid))
      shutil.rmtree('audios/{}/'.format(videoid))

    def do_create(self, index, videoid, doc, clear_cache=False):
      """
      Create document
      """
      self.es.create(index=index, id=videoid, body=doc)
      if clear_cache:
        self.do_clear_cache(videoid)
      print('\r *** create document done at {} ***'.format(datetime.datetime.now()))

    def do_bulk_import(self, import_data, count, clear_cache=False):
      """
      Bulk Import documents
      """
      size = sys.getsizeof(import_data)
      count += 1
      print('\r ****** bulk_import {} [{}] started at {} *****'.format(
          count, 
          self.convert_size(size, "KB"),
          datetime.datetime.now()))
      helpers.bulk(self.es, import_data)
      print('\r ****** bulk_import {} [{}]    done at {} *****'.format(
          count, 
          self.convert_size(size, "KB"), 
          datetime.datetime.now()))
      if clear_cache:
        for data in import_data:
          self.do_clear_cache(data['_id'])
      
      return count

    def get_video_info(self, keyword, maxResults=5):
      """
      Search query matched videos and get each info
      """
      query = self.youtube.search().list(
        part='id,snippet',
        q=keyword,
        type='video',
        maxResults=maxResults,
        order='relevance',
      )
      response = query.execute()
      return response.get('items', [])
    
    def download_video(self, videoid):
      """
      Download Target videoid video
      """
      if not os.path.exists("videos"):
        os.makedirs("videos")
      url = "https://youtu.be/{}".format(videoid)
      ydl_opts = {
        'format': 'bestaudio[ext=m4a]',
        'outtmpl': 'videos/%(id)s.mp4'
      }
      with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    def gen_audio(self, videoid):
      """
      Generate Audio files for Speech-To-Text
      """
      try:
        if not os.path.exists("audios"):
          os.makedirs("audios")
        if os.path.exists("videos/{}.mp4".format(videoid)) and (not os.path.exists("audios/{}.wav".format(videoid))):
          self.logger.info('Re-sampling to 16000Hz Audio')
          data, samplerate = librosa.core.load("videos/{}.mp4".format(videoid), sr=16000, mono=True)
          librosa.audio.sf.write("audios/{}.wav".format(videoid), data, samplerate)
          if not os.path.exists("audios/{}".format(videoid)):
            os.makedirs("audios/{}".format(videoid))
          self.logger.info("Split to multiple Audio files on silence")
          source = AudioSegment.from_file("audios/{}.wav".format(videoid), format="wav")
          chunks = split_on_silence(source, min_silence_len=1000, silence_thresh=-40, keep_silence=200, seek_step=5)
          count = 0
          for chunk in chunks:
            duration_in_milliseconds = len(chunk)
            if duration_in_milliseconds > 40000:
              for slice in chunk[::20000]:
                chunk_filepath = "audios/{}/{}.wav".format(videoid, count)
                with open(chunk_filepath , "wb") as f:
                  slice.export(f, format="wav")
                  self.logger.info("{} exported.".format(chunk_filepath))
                  count += 1 
                  if count == config.MAX_AUDIOFILES:
                    break
              else:
                continue
              break
            else:
              chunk_filepath = "audios/{}/{}.wav".format(videoid, count)
              chunk.export(chunk_filepath, format="wav")
              self.logger.info("{} exported.".format(chunk_filepath))
              count += 1
              if count == config.MAX_AUDIOFILES:
                break
      except Exception as e:
        self.logger.error(e)

    def do_speech2text(self, videoid):
      """
      Do Speech-To-Text
      """
      result = ""
      if os.path.exists("audios/{}".format(videoid)):
        files = glob.glob("audios/{}/*.wav".format(videoid))
        for file in natsorted(files):
          speech, _ = soundfile.read(file)
          nbests = self.speech2text(speech)
          text, *_ = nbests[0]
          self.logger.info(file)
          self.logger.info(text)
          result += text
      else:
        self.logger.error("Target videoId[{}] Audio files not found.".format(videoid))
      return result
