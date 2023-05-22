import speech_recognition as sr
import pyaudio
import webrtcvad
import wave
import keyboard
import threading
import queue
import noisereduce as nr
import numpy as np


def save_audio(filename, frames):
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        f.setframerate(16000)
        f.writeframes(b''.join(frames))

def reduce_noise(chunk):
    chunk_np = np.frombuffer(chunk, dtype=np.int16)  # 청크를 np.ndarray(int16) 형식으로 변환합니다.
    reduced_chunk_np = nr.reduce_noise(y=chunk_np, sr=16000)  # 노이즈 감소를 수행합니다.
    reduced_chunk = reduced_chunk_np.astype(np.int16).tobytes()  # 처리된 청크를 바이트로 변환합니다.
    return reduced_chunk


def recognize_speech(recognizer, audio_data, wake_word, result_queue):
    try:
        text = recognizer.recognize_google(audio_data, language="ko-KR")
        print(text)
        if wake_word in text:
            result_queue.put(True)
    except sr.UnknownValueError:
        print("인식불가")
    except sr.RequestError:
        print("Couldn't get results from Google Speech Recognition service")
        result_queue.put(False)


def main():
    recognizer = sr.Recognizer()
    vad = webrtcvad.Vad()
    vad.set_mode(0)

    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=480,
    )

    print("Listening for wake word...")
    recording = False
    buffer = []
    silence_counter = 0
    max_silence_counter = 100
    start_text = "안녕"
    buffer_size = 480

    result_queue = queue.Queue()

    while True:
        chunk = stream.read(buffer_size, exception_on_overflow=False)
        chunk = reduce_noise(chunk) #노이즈 감소
        is_speech = vad.is_speech(chunk, 16000)

        if not recording:
            buffer.append(chunk)
            if len(buffer) >= 16000 // buffer_size * 3:
                buffer.pop(0)

            if keyboard.is_pressed('q'):
                print('Saving processed audio...')
                save_audio("processed_audio.wav", buffer)

            if is_speech:
                audio_buffer = b''.join(buffer)
                audio_data = sr.AudioData(audio_buffer, 16000, 2)
                recognition_thread = threading.Thread(target=recognize_speech,
                                                      args=(recognizer, audio_data, start_text, result_queue))
                recognition_thread.start()

                # 결과 검사
                if not result_queue.empty():
                    recognition_result = result_queue.get(timeout=1)
                    if recognition_result:
                        recording = True
                        print("Starting recording...")
                        frames = [audio_buffer]
                        silence_counter = 0

        else:
            frames.append(chunk)
            if not is_speech:
                if silence_counter >= max_silence_counter:
                    print("Stopping recording!")
                    save_audio("recorded.wav", frames)
                    break
                silence_counter += 1
            else:
                silence_counter = 0

    stream.stop_stream()
    stream.close()
    pyaudio.PyAudio().terminate()

if __name__ == "__main__":
    main()
