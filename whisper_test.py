import whisper

model = whisper.load_model("base")
result = model.transcribe("audios/test_english.wav")
print(result["text"])
result = model.transcribe("audios/test_portuguese.wav")
print(result["text"])