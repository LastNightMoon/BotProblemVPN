import os
import random

import requests
import json

from modules.managerDataBase.models import User


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
            b_user = {"tag": user["remark"], "up": user["up"], "down": user["down"], "time": user["expiryTime"],
                      "port": user["port"]}
            link = (f"""vless://{json.loads(user["settings"])["clients"][0]["id"]}@
                    {user["port"]}?type=tcp&security=reality&pbk={json.loads(user['streamSettings'])['realitySettings']['settings']['publicKey']}
                    &fp=chrome&sni=google.com&sid={json.loads(user['streamSettings'])['realitySettings']['shortIds'][0]}#user1""").replace(
                "\n", "").replace(" ", "")
            b_user["link"] = link
            dict_response[str(user["remark"])] = User(**b_user)
        return dict_response

    def get_user_info(self, user_tag):
        return self.list()[user_tag]

    def check_user(self, user_tag):
        return user_tag in self.list()

    def create_user(self, user_name):
        port = 0
        while port == 0 or port in map(lambda us: us.port, self.list().values()):
            port = random.randint(1024, 65535)
        data = {
            "up": 0,
            "down": 0,
            "total": int(1024 * 1024 * 1024 * 0.5),
            "remark": user_name,
            "enable": True,
            "expiryTime": 0,
            "listen": "",
            "port": port,
            "protocol": "vless",
            "settings": "{\"clients\": [{\"id\": \"b86c0cdc-8a02-4da4-8693-72ba27005587\",\"flow\": \"\",\"email\": \""+user_name + str(port)+"\",\"limitIp\": 0,\"totalGB\": 0,\"expiryTime\": 0,\"enable\": true,\"tgId\": \"\",\"subId\": \"rqv5zw1ydutamcp0\",\"reset\": 0}],\"decryption\": \"none\",\"fallbacks\": []}",
            "streamSettings": "{\"network\": \"tcp\",\"security\": \"reality\",\"externalProxy\": [],\"realitySettings\": {\"show\": false,\"xver\": 0,\"dest\": \"google.com:443\",\"serverNames\": [\"google.com\",\"www.google.com\"],\"privateKey\": \"wIc7zBUiTXBGxM7S7wl0nCZ663OAvzTDNqS7-bsxV3A\",\"minClient\": \"\",\"maxClient\": \"\",\"maxTimediff\": 0,\"shortIds\": [\"47595474\",\"7a5e30\",\"810c1efd750030e8\",\"99\",\"9c19c134b8\",\"35fd\",\"2409c639a707b4\",\"c98fc6b39f45\"],\"settings\": {\"publicKey\": \"2UqLjQFhlvLcY7VzaKRotIDQFOgAJe1dYD1njigp9wk\",\"fingerprint\": \"random\",\"serverName\": \"\",\"spiderX\": \"/\"}},\"tcpSettings\": {\"acceptProxyProtocol\": false,\"header\": {\"type\": \"none\"}}}",
            "sniffing": "{\"enabled\": true,\"destOverride\": [\"http\",\"tls\",\"quic\",\"fakedns\"],\"metadataOnly\": false,\"routeOnly\": false}",
            "allocate": "{\"strategy\": \"always\",\"refresh\": 5,\"concurrency\": 3}"
        }
        response = self.session.post(f"{self.path}/panel/api/inbounds/add", json=data, headers={"Accept": "application/json"})
        print(response.text)
        return response.status_code

    def payment(self, user_name: str):
        pass


if __name__ == '__main__':
    request = Request()
    # print(request.list())
    request.create_user("19a")
    print(request.check_user("19a"))