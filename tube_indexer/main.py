# -*- coding: utf-8 -*-
import config
import tubeindexer
from logging import Formatter, getLogger, StreamHandler, DEBUG, WARNING
import warnings
warnings.filterwarnings('ignore')

def main():

  logger = getLogger()
  handler = StreamHandler()
  handler.setLevel(DEBUG)
  handler.setFormatter(Formatter('[%(name)s] %(message)s'))
  logger.addHandler(handler)
  logger.setLevel(WARNING)
  logger.info('The root logger is created.')

  indexer = tubeindexer.TubeIndexer()

  indexer.make_es_index(index=config.ES_INDEX, 
    setting_file_path="tube_setting.json", 
    mapping_file_path="tube_mapping.json", 
    recreate=False)

  api_results = indexer.get_video_info(config.YT_QUERY, config.YT_MAXRESULTS)
  import_data, count, import_count = [], 1, 0
  for i, result in enumerate(api_results):
    videoid = result['id']['videoId']
    if not indexer.exists(config.ES_INDEX, videoid):
      indexer.download_video(videoid)
      indexer.recognizer.gen_audio(videoid)
      text = indexer.recognizer.do_speech2text(videoid)
      doc = {
        'title': result['snippet']['title'],
        'text': text,
        'url': "https://youtu.be/{}".format(videoid),
        'thumbnail': result['snippet']['thumbnails']['high']['url'],
        'time': result['snippet']['publishedAt']
      }
      import_data.append({'_index': config.ES_INDEX, '_id': videoid, '_source': doc})
      if count % 1000 == 0:
        import_count = indexer.do_bulk_import(import_data, import_count, clear_cache=True)
        import_data, count = [], 1
      elif len(api_results) == i + 1 and len(import_data) > 1:
        import_count = indexer.do_bulk_import(import_data, import_count, clear_cache=True)
        import_data, count = [], 1
      elif len(api_results) == i + 1 and len(import_data) == 1:
        indexer.do_create(config.ES_INDEX, videoid, doc, clear_cache=True)
      else:
        count += 1
  
if __name__ == "__main__":
  main()