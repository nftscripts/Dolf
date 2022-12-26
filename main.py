from requests.exceptions import ConnectionError
from loguru import logger
from time import sleep
import pyuseragents
import requests
import random
import string


class Process:
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://dolf.finance',
            'Referer': 'https://dolf.finance/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Dolf-Request-Id': '0ceb80c0-c908-4e5d-0300-bb71e5c5e8b9',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    @staticmethod
    def fake_mail() -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(9))

    def main_register(self) -> None:
        with open('mails.txt', 'r') as file:
            lines = [line.rstrip() for line in file]
            for line in lines:
                json_data = {
                    'email': line,
                    'referralCode': None,
                }

                try:
                    self.headers.update({"User-Agent": pyuseragents.random()})
                    response = requests.post('https://apiserver.dolf.finance/prod/referral', headers=self.headers,
                                             json=json_data)
                except ConnectionError as ex:
                    logger.error('Не удалось получить ответ от сервера')

                if response.status_code == 200:
                    ref_code = {'referralCode': response.json()['data']['referral_code']}
                    json_data.update(ref_code)
                    self.register_referrals(json_data, line)
                    sleep(180)
                elif response.status_code >= 400:
                    sleep(180)
                    logger.error('Превышен лимит запросов')

    def register_referrals(self, json_data: dict, line: str) -> None:
        count = 0
        while count != 4:
            ref_mail = {'email': self.fake_mail() + "@gmail.com"}
            json_data.update(ref_mail)
            self.headers.update({"User-Agent": pyuseragents.random()})
            response = requests.post('https://apiserver.dolf.finance/prod/referral', headers=self.headers, json=json_data)
            if response.status_code == 200:
                count = count + 1
                logger.debug(f'Зарегал {count} реферала для {line}')
            elif response.status_code >= 400:
                sleep(180)
                logger.error('Превышен лимит запросов')
                continue


reg = Process()
reg.main_register()
