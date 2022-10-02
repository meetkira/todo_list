import json

import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, GetUpdatesResponseSchema, SendMessageResponseSchema


class TgClient:
    def __init__(self, token):
        self.token = token

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
            response = requests.get(url=request_url)
            json_response = json.loads(response.text)
            json_response["result"]["from_"] = json_response["result"].pop("from")
            data = SendMessageResponseSchema().load(json_response)
            return data
        except Exception:
            raise NotImplementedError


if __name__ == "__main__":
    cl = TgClient("5630137267:AAEAa-1q952vsPtg_qneW41QJ0QYVIcbGmw")
    print(cl.get_updates(offset=0, timeout=60))
    print(cl.send_message(818206966, "hello"))
