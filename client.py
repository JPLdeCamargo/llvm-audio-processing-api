import requests
import whisper
import sounddevice as sd
import numpy as np
import numpy.typing as npt
from scipy.io.wavfile import write


class Client:
    def __init__(self, base_url:str) -> None:
        self.__base_url = base_url

    def send_wav_file(self, file_location:str, endpoint:str) -> requests.Response:
        file_content = whisper.load_audio(file_location)

        url = f"{self.__base_url}{endpoint}"
        data = {
            "file":file_content.tolist()
        }
        return requests.post(url, json=data)

    def send_wav_array(self, wav_array:npt.NDArray[np.float32], endpoint:str) -> requests.Response:
        url = f"{self.__base_url}{endpoint}"
        data = {
            "file":wav_array.tolist()
        }
        return requests.post(url, json=data)


    def record_wav_array(self, max_time:int, sample_rate:int) -> npt.NDArray[np.float32]:
        print("Recording... Press Ctrl+C to stop.")
        try:
            recording = sd.rec(int(max_time * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()
            sd.play(recording, sample_rate)
            # recording = np.squeeze(np.array(recording))
            return recording
        except KeyboardInterrupt:
            print("Recording stopped.")
            return recording[:sd.get_stream().time * sample_rate]

    def save_audio_to_wav(self, audio_data: npt.NDArray[np.float32], sample_rate: int, filename: str) -> None:
        # Scale the float32 array to int16 for WAV file compatibility
        int_data = np.int16(audio_data * 32767)
        write(filename, sample_rate, int_data)
        print(f"Audio saved to {filename}")



if __name__ == "__main__":
    client = Client("http://127.0.0.1:8000/whisper/")
    sample_rate = 16000
    recording = client.record_wav_array(5, sample_rate)
    client.save_audio_to_wav(recording, sample_rate, "test.wav")
    # response = client.send_wav_array(recording, "transcribe/")
    # response = client.send_wav_file("audios/test_english.wav", "transcribe/")
    response = client.send_wav_file("test.wav", "transcribe/")
    print(response.content)

