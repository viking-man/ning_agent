import whisper
import time
import logging
import torch


class WhisperModel():
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.device = None
        self.whisper_model = None
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    def load_model(self):
        self.whisper_model = whisper.load_model("small", self.device)

    def transcribe(self, audio, lang):
        tic = time.time()

        res = self.whisper_model.transcribe(
            audio,
            task="transcribe",
            language=lang,
            verbose=True
        )

        logging.info(f"Done transcription in {time.time() - tic:.1f} sec")
        return res
