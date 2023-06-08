from speechmodules.wakeword import PicoWakeWord
from speechmodules.speech2text import BaiduASR, AzureASR, OpenaiASR
from speechmodules.text2speech import BaiduTTS, Pyttsx3TTS, AzureTTS, EdgeTTS
from chatmodules.openai_chat_module import OpenaiChatModule
import asyncio
import struct
import os
os.environ["SERPER_API_KEY"] = "" # 你的serper key
openai_api_key = "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"  # 你的openai key
PICOVOICE_API_KEY = "UOUMvGnvoF6gLKxerJ94W2ExFNE9Ml/PJDQ5NQeyDAw5iSPDPLDJqQ=="  # 你的picovoice key
keyword_path = './hi-lucy_en_raspberry-pi_v2_2_0.ppn'  # 你的唤醒词检测离线文件地址
model_path = '' # 中文模型地址
Baidu_APP_ID = ''  # 你的百度APP_ID
Baidu_API_KEY = ''  # 你的百度API_KEY
Baidu_SECRET_KEY = ''  # 你的百度SECRET_KEY
AZURE_API_KEY = ""  # 你的azure key
AZURE_REGION = ""  # 你的azure region



def run(picowakeword, asr, tts, openai_chat_module):
    while True:  # 需要始终保持对唤醒词的监听
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            picowakeword.porcupine.delete()
            picowakeword.stream.close()
            picowakeword.myaudio.terminate()  # 需要对取消对麦克风的占用!

            print("嗯,我在,请讲！")
            #tts.text_to_speech_and_play("嗯,我在,请讲！")
            asyncio.run(tts.text_to_speech_and_play("嗯,我在,请讲！"))  # 如果用Edgetts需要使用异步执行
            while True:  # 进入一次对话session
                q = asr.speech_to_text()
                print(f'recognize_from_microphone, text={q}')
                res = openai_chat_module.chat_with_origin_model(q)
                # res = openai_chat_module.chat_with_agent(q)
                print(res)
                #tts.text_to_speech_and_play('嗯' + res)
                asyncio.run(tts.text_to_speech_and_play('嗯'+res))  # 如果用Edgetts需要使用异步执行


def Orator():
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    #asr = AzureASR(AZURE_API_KEY, AZURE_REGION)
    #tts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    asr = OpenaiASR(openai_api_key)
    tts = EdgeTTS()
    openai_chat_module = OpenaiChatModule(openai_api_key)
    #openai_chat_module = OpenaiAgentModule(openai_api_key)
    try:
        run(picowakeword, asr, tts, openai_chat_module)
    except KeyboardInterrupt:
        if picowakeword.porcupine is not None:
            picowakeword.porcupine.delete()
            print("Deleting porc")
        if picowakeword.stream is not None:
            picowakeword.stream.close()
            print("Closing stream")
        if picowakeword.myaudio is not None:
            picowakeword.myaudio.terminate()
            print("Terminating pa")
            exit(0)
    finally:
        print('本轮对话结束')
        #tts.text_to_speech_and_play('嗯' + '主人，我退下啦！')
        asyncio.run(tts.text_to_speech_and_play('嗯'+'主人，我退下啦！'))  # 如果用Edgetts需要使用异步执行
        #if picowakeword.porcupine is not None:
        #    picowakeword.porcupine.delete()
        #    print("Deleting porc")
        #if picowakeword.stream is not None:
        #    picowakeword.stream.close()
        #    print("Closing stream")
        #if picowakeword.myaudio is not None:
        #    picowakeword.myaudio.terminate()
        #    print("Terminating pa")
        Orator()

if __name__ == '__main__':
    Orator()
