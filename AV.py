# Голосовой ассистент1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import Weather

# настройки
opts = {
    "alias": ('ва','голосовой помощник','голосовой ассистент','ассистент','voice assistant','помощник'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
        "city": ('киров', 'москва', 'вашингтон', 'лондон'),
        "weather":('погода','скажи погоду','какая сейчас погода')
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
            # обращение
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

    # elif cmd == 'weather':
    #     speak(Weather)


    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Студент на экзамене:— Профессор, понимаете, я не могу сдать математику… потому что совсем не сплю в последний месяц. Вот только закрою глаза как появляется страшная картина… меня прижали к стене атомной станции какие-то страшные мутанты и готовы разорвать… в клочки. А профессор говорит: Окончив институт с теперешними знаниями, молодой человек, наверняка, вы подались бы в сталкеры… а там и до кошмаров ваших недалеко. Да, но у меня есть верное средство. Переэкзаменовку по математике вы так и не сдали, а следовательно будете отчислены и пойдете служить. И никаких монстров, кроме, разве что, «дедов». ")

    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()


speak("Добрый день, Голосовой помощник на связи")
speak("Слушаю команду")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop