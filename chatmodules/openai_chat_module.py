# pip install openai
import openai
openai_api_key = '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'


class OpenaiChatModule:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_base = "https://proxy.994938.xyz/v1"
        self.origin_model_conversation = [
                                {"role": "system", "content": "你是用户user的好朋友，能够和user进行愉快的交谈，你的名字叫Murphy."}
                            ]

    def chat_with_origin_model(self, text):
        openai.api_key = self.openai_api_key
        text = text.replace('\n', ' ').replace('\r', '').strip()
        if len(text) == 0:
            return
        print(f'chatGPT Q:{text}')
        self.origin_model_conversation.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            #model="gpt-4",
            messages=self.origin_model_conversation,
            max_tokens=2048,
            temperature=0.3,
        )
        reply = response.choices[0].message.content
        self.origin_model_conversation.append({"role": "assistant", "content": reply})
        return reply



if __name__ == '__main__':
    openaichatmodule = OpenaiChatModule(openai_api_key)
    print(openaichatmodule.chat_with_origin_model('你好，你叫什么?'))
    print(openaichatmodule.chat_with_origin_model('天空为什么是蓝色的?'))
