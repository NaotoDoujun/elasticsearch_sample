# -*- coding: utf-8 -*-
import os, shutil, glob
from natsort import natsorted
import librosa
import soundfile
from pydub import AudioSegment
from pydub.silence import split_on_silence
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_inference import Speech2Text
from logging import getLogger, NullHandler, INFO
import config

class Recognizer:

  WORK_DIR = "audios"
  MIN_SILENCE_LEN = 1000
  SILENCE_THRESH = -40
  KEEP_SILENCE = 200
  SEEK_STEP = 5
  MIN_DURATION = 10000

  def __init__(self, name=__name__):
    self.logger = getLogger(name)
    self.logger.addHandler(NullHandler())
    self.logger.setLevel(INFO)
    self.logger.propagate = True

  def get_workdir(self):
    return self.WORK_DIR

  def do_clear_cache(self, videoid):
    """
    Clear Target videoid audio files
    """
    if os.path.exists('{}/{}.mp3'.format(self.WORK_DIR, videoid)):
      os.remove('{}/{}.mp3'.format(self.WORK_DIR, videoid))
    if os.path.exists('{}/{}.wav'.format(self.WORK_DIR, videoid)):
      os.remove('{}/{}.wav'.format(self.WORK_DIR, videoid))
    if os.path.exists('{}/{}/'.format(self.WORK_DIR, videoid)):
      shutil.rmtree('{}/{}/'.format(self.WORK_DIR, videoid))

  def split_file(self, videoid):
    self.logger.info("Split to multiple Audio files")
    source = AudioSegment.from_file("{}/{}.wav".format(self.WORK_DIR, videoid), format="wav")
    chunks = split_on_silence(source, 
      min_silence_len=self.MIN_SILENCE_LEN, 
      silence_thresh=self.SILENCE_THRESH, 
      keep_silence=self.KEEP_SILENCE, 
      seek_step=self.SEEK_STEP)
    count = 0
    for chunk in chunks:
      duration_in_milliseconds = len(chunk)
      if duration_in_milliseconds > self.MIN_DURATION:
        for slice in chunk[::5000]:
          chunk_filepath = "{}/{}/{}.wav".format(self.WORK_DIR, videoid, count)
          with open(chunk_filepath , "wb") as f:
            slice.export(f, format="wav")
          self.logger.info("{} exported.".format(chunk_filepath))
          count += 1
          if config.MAX_AUDIOFILES > 0 and count == config.MAX_AUDIOFILES:
            break
        else:
          continue
        break
      else:
        chunk_filepath = "{}/{}/{}.wav".format(self.WORK_DIR, videoid, count)
        chunk.export(chunk_filepath, format="wav")
        self.logger.info("{} exported.".format(chunk_filepath))
        count += 1
        if config.MAX_AUDIOFILES > 0 and count == config.MAX_AUDIOFILES:
          break


class RecognizerEspnet(Recognizer):

  """
    Recognizer Espnet
    
    Attributes
    ----------
    speech2text : 
        ESPNet
  """

  def __init__(self, name=__name__):
    super().__init__(name)
    d = ModelDownloader("~/.cache/espnet")
    self.speech2text = Speech2Text(
      **d.download_and_unpack(config.ESPNET_ASR_MODEL))

  def do_resample(self, videoid):
    self.logger.info("Re-sampling to {}Hz Audio.".format(config.ASR_SAMPLING_RATE))
    data, samplerate = librosa.core.load(
      "{}/{}.mp3".format(self.WORK_DIR, videoid), 
      sr=config.ASR_SAMPLING_RATE, 
      mono=True)
    librosa.audio.sf.write(
      "{}/{}.wav".format(self.WORK_DIR, videoid), 
      data, 
      samplerate)

  def gen_audio(self, videoid):
    """
    Generate Audio files for Speech-To-Text
    """
    try:

      if os.path.exists("{}/{}.mp3".format(self.WORK_DIR, videoid)):
        
        # resample for speech recognize
        if not os.path.exists("{}/{}.wav".format(self.WORK_DIR, videoid)):
          self.do_resample(videoid)

        # make dir
        if not os.path.exists("{}/{}/".format(self.WORK_DIR, videoid)):
          os.makedirs("{}/{}".format(self.WORK_DIR, videoid))

        # split file
        super().split_file(videoid)

    except Exception as e:
      self.logger.error(e)

  def do_speech2text(self, videoid):
    """
    Do Speech-To-Text
    """
    result = ""
    if os.path.exists("{}/{}/".format(self.WORK_DIR, videoid)):
      files = glob.glob("{}/{}/*.wav".format(self.WORK_DIR, videoid))
      for file in natsorted(files):
        try:
          speech, _ = soundfile.read(file)
          nbests = self.speech2text(speech)
          text, *_ = nbests[0]
          self.logger.info(file)
          self.logger.info(text)
          result += text
        except Exception as e:
          self.logger.error(file)
          self.logger.error(e)
    else:
      self.logger.error("Target videoId[{}] Audio files not found.".format(videoid))
    return result