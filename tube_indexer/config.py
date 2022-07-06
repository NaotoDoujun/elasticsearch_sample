# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv()

import os
YOUTUBE_API_SERVICE_NAME = os.getenv('YOUTUBE_API_SERVICE_NAME')
YOUTUBE_API_VERSION = os.getenv('YOUTUBE_API_VERSION')
API_KEY = os.getenv('API_KEY')
ES_ENDPOINT = os.getenv('ES_ENDPOINT')
ESPNET_MODEL = "kan-bayashi/csj_asr_train_asr_transformer_raw_char_sp_valid.acc.ave"