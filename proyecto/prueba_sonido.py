import speech_recognition as sr

# Crear un reconocedor de voz
r = sr.Recognizer()

# Usar el micrófono como fuente de audio
with sr.Microphone() as source:
    print("Di algo...")
    audio = r.listen(source)

# Intentar reconocer el comando de voz
try:
    comando = r.recognize_google(audio, language='es-ES')
    print("Has dicho: " + comando)
except sr.UnknownValueError:
    print("No he podido entender lo que has dicho")
except sr.RequestError as e:
    print("No se pudo solicitar resultados; {0}".format(e))