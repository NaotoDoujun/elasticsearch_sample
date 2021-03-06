# -*- coding: utf-8 -*-
from webbrowser import get
import tubeindexer
import warnings
warnings.filterwarnings('ignore')

def main():
  ES_INDEX = "tube"
  YT_QUERY = "新車レビュー"
  YT_MAXRESULTS = 2

  indexer = tubeindexer.TubeIndexer()

  indexer.make_es_index(index=ES_INDEX, 
    setting_file_path="tube_setting.json", 
    mapping_file_path="tube_mapping.json", 
    recreate=False)

  api_results = indexer.get_video_info(YT_QUERY, YT_MAXRESULTS)
  import_data, count, import_count = [], 1, 0
  for i, result in enumerate(api_results):
    videoid = result['id']['videoId']
    if not indexer.exists(ES_INDEX, videoid):
      indexer.download_video(videoid)
      indexer.gen_audio(videoid)
      text = indexer.do_speech2text(videoid)
      doc = {
        'title': result['snippet']['title'],
        'text': text,
        'url': "https://youtu.be/{}".format(videoid),
        'thumbnail': result['snippet']['thumbnails']['default']['url'],
        'time': result['snippet']['publishedAt']
      }
      import_data.append({'_index': ES_INDEX, '_id': videoid, '_source': doc})
      if count % 1000 == 0:
        import_count = indexer.do_bulk_import(import_data, import_count, clear_cache=True)
        import_data, count = [], 1
      elif len(api_results) == i + 1 and len(import_data) > 1:
        import_count = indexer.do_bulk_import(import_data, import_count, clear_cache=True)
        import_data, count = [], 1
      elif len(api_results) == i + 1 and len(import_data) == 1:
        indexer.do_create(ES_INDEX, videoid, doc, clear_cache=True)
      else:
        count += 1
  
if __name__ == "__main__":
  main()