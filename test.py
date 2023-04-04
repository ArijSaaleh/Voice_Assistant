import pyttsx3
import langid
import fasttext


model = fasttext.load_model('lid.176.bin')

# Initialize the Text-to-Speech engine and print a list of available voices
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    print(voice.id)
    #MSTTS_V110_enCA_RichardM
"""
    'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0' 0
    'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'    1
    'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'     2
    'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'    3
    """
"""
text = 'hey'
predicted_language = model.predict(text)[0][0][-2:]
print(predicted_language)"""