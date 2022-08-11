# -*- coding: utf-8 -*-
import os, json, sys, datetime
from apiclient.discovery import build
from yt_dlp import YoutubeDL
from elasticsearch import Elasticsearch, helpers
from logging import getLogger, NullHandler, INFO
import config
import recognizer

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

        self.logger = getLogger(name)
        self.logger.addHandler(NullHandler())
        self.logger.setLevel(INFO)
        self.logger.propagate = True

        self.recognizer = recognizer.RecognizerEspnet()

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

    def do_create(self, index, videoid, doc, clear_cache=False):
      """
      Create document
      """
      self.es.create(index=index, id=videoid, body=doc)
      if clear_cache:
        self.recognizer.do_clear_cache(videoid)
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
          self.recognizer.do_clear_cache(data['_id'])
      
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
      work_dir = self.recognizer.get_workdir()
      if not os.path.exists(work_dir):
        os.makedirs(work_dir)
      
      url = "https://youtu.be/{}".format(videoid)
      ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': work_dir + '/%(id)s.%(ext)s',
        'postprocessors': [
        {'key': 'FFmpegExtractAudio',
         'preferredcodec': 'mp3',
         'preferredquality': '192'},
        {'key': 'FFmpegMetadata'},
    ],
      }
      with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

