from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import whisper
import numpy as np

class Transcribe(APIView):
    def post(self, request):
        model = whisper.load_model("tiny")

        # load audio and pad/trim it to fit 30 seconds
        audio = request.data['file']
        audio = np.array(audio, dtype="float32")
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)

        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)

        # print the recognized text
        print(result.text)

        return Response(result.text, status=status.HTTP_200_OK)