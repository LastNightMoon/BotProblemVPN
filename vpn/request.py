import os

import requests
import json


class Request:
    path = f'http://{os.environ["IP_VPN"]}/{os.environ["PATH_VPN"]}'

    def __init__(self):
        self.session = requests.Session()
        self.login()

    def login(self):
        param = {"username": os.environ["USER"], "password": os.environ["PASSWORD"]}
        response = self.session.post(f"{self.path}/login", params=param)
        print(response.status_code)

    def list(self):
        response = self.session.get(f"{self.path}/panel/api/inbounds/list")
        print(response.status_code)
        dict_response = {}
        for user in json.loads(response.text)["obj"]:
            b_user = {"tag": user["remark"], "up": user["up"], "down": user["down"], "time": user["expiryTime"]}

            link = (f"""vless://{json.loads(user["settings"])["clients"][0]["id"]}@
                    {os.environ["IP_VPN"]}?type=tcp&security=reality&pbk={json.loads(user['streamSettings'])['realitySettings']['settings']['publicKey']}
                    &fp=chrome&sni=google.com&sid={json.loads(user['streamSettings'])['realitySettings']['shortIds'][0]}#user1""").replace(
                "\n", "").replace(" ", "")
            b_user["link"] = link
            dict_response[user["remark"]] = b_user
        return dict_response

    def get_user_info(self, user_tag):
        return self.list()[user_tag]

    def check_user(self, user_tag):
        return user_tag in self.list()

    def create_user(self, user_name):
        pass


if __name__ == '__main__':
    request = Request()
    print(request.list())
