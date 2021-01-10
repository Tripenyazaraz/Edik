import pyttsx3
import speech_recognition as sr
import os
import time
import datetime
import webbrowser
from fuzzywuzzy import fuzz

# настройки
opts = {
    "alias": ('эдик', 'эдгар', 'эдуард'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupidJoke": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
        "close": ('пока', 'выключись')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Эдику
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        speak("Рито говна не посоветуют")

    elif cmd == 'stupidJoke':
        # рассказать анекдот
        speak("Рито говна не посоветуют")

    elif cmd == 'close':
        # выключить Эдика
        speak("Вернусь в любое время, повелитель")
        exit()

    else:
        print('Команда не распознана, повторите!')

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=2)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# выбор голоса
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voices', voices[3].id)

speak('Добрый день, повелитель')
speak('Эдик слушает')
sr.energy_threshold = 3000 # попробуйте от 50 до 4000

while True:
    with m as source:
        audio = r.listen(source)
    callback(r, audio)
    time.sleep(0.1)