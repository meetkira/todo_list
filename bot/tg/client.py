import json
import random
import string

import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, GetUpdatesResponseSchema, SendMessageResponseSchema


class TgClient:
    def __init__(self, token):
        self.token = token

    def new_verification_code(self):
        self.verification_code = "".join(random.choices(string.ascii_letters + string.digits, k=50))

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        try:
            request_url = self.get_url(method=f"getUpdates?offset={offset}&timeout={timeout}")
            response = requests.get(url=request_url)
            json_response = json.loads(response.text)
            for res in json_response["result"]:
                res["message"]["from_"] = res["message"].pop("from")

            data = GetUpdatesResponseSchema().load(json_response)
            return data

        except Exception:
            raise NotImplementedError


    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        try:
            request_url = self.get_url(method=f"sendMessage?chat_id={chat_id}&text={text}")
            print(request_url)
            response = requests.get(url=request_url)
            json_response = json.loads(response.text)
            print(json_response)
            json_response["result"]["from_"] = json_response["result"].pop("from")
            data = SendMessageResponseSchema().load(json_response)
            return data
        except Exception:
            raise NotImplementedError
