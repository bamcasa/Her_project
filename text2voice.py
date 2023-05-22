import pyttsx3

def text_to_speech(text, voice_id):
    engine = pyttsx3.init()
    engine.setProperty("voice", voice_id)
    engine.say(text)
    engine.runAndWait()

input_text = "안녕하세요, 뤼튼입니다."
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0"

text_to_speech(input_text, voice_id)
