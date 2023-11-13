import base64
import datetime
import pickle
import random
import re
import shutil
import ssl
import string
import time
import traceback

import capmonster_python
import cloudscraper
import requests
import warnings

import ua_generator
from eth_account.messages import encode_defunct
from web3.auto import w3

from utils.logger import logger

warnings.filterwarnings("ignore", category=DeprecationWarning)



class Ethermail:

    def __init__(self, proxy, private, address, refCode = None, logger=None):
        self.logger = logger
        self.access_token = None
        self.refCode = refCode

        self.ua = self.generate_user_agent

        self.private, self.address = private, address
        self.session = self._make_scraper
        self.proxy = proxy
        self.session.proxies = {"http": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                "https": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"}
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.session.headers.update({"user-agent": self.ua,
                                     'content-type': 'application/json'})

    def Registration(self):

        with self.session.get(f"https://ethermail.io/?afid={self.refCode}") as response:
            pass

        self.session.headers.update({"referer": f"https://ethermail.io/?afid={self.refCode}",
                                     "dnt": "1"})

        self.session.cookies.update({"afid": self.refCode})

        message = encode_defunct(text=self.nonce)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private)
        self.signature = signed_message["signature"].hex()

        payload = {"web3Address":self.address.lower(),
                   "signature":self.signature}

        with self.session.post("https://ethermail.io/api/auth/login", json=payload) as response:
            # print(response.text)
            self.access_token = response.json()["token"]
        time.sleep(random.randint(1,9)/10)

        with self.session.get("https://ethermail.io/api/users") as response:
            self.user_info = response.json()
        time.sleep(random.randint(1,9)/10)

        with self.session.get("https://ethermail.io/api/users/coins") as response:
            print(response.text)
        time.sleep(random.randint(1,9)/10)

        with self.session.get("https://ethermail.io/api/mailboxes") as response:
            ...
        time.sleep(random.randint(1,9)/10)
        with self.session.get("https://ethermail.io/api/users") as response:
            ...
        time.sleep(random.randint(1,9)/10)
        with self.session.get("https://ethermail.io/api/mailboxes") as response:
            mailbox = response.json()["results"][0]["id"]
        time.sleep(random.randint(1,9)/10)
        with self.session.get("https://ethermail.io/api/users/onboarding") as response:
            ...
        time.sleep(random.randint(1,9)/10)
        # with self.session.get("https://ethermail.io/api/events") as response:
        #     ...
        with self.session.get(f"https://ethermail.io/api/mailboxes/{mailbox}") as response:
            # print(response.json())
            ...
        time.sleep(random.randint(1,9)/10)
        with self.session.get("https://ethermail.io/api/users") as response:
#             print(response.json())
            ...
        time.sleep(random.randint(1,9)/10)
        with self.session.post("https://ethermail.io/api/messages/search", json={"next":None,"previous":None,"page":1,"limit":10,"mailbox":mailbox}) as response:
            ...
        time.sleep(random.randint(1,9)/10)

        while True:
            with self.session.post("https://ethermail.io/api/users/onboarding", json={"email":""}) as response:
                # print(response.text)
                time.sleep(random.randint(1,9)/10)

            payload = {"location":"","rewards":"","frequency":"","gender":"","interests":[],"birthday":None}
            with self.session.post("https://ethermail.io/api/paywall/save-reward-data", json=payload) as response:
#                 print(response.text)
                time.sleep(random.randint(1,9)/10)

            payload = {"paywall":{"typeWeb":"WEB2","configurationPaywall":"FILTER_NO_CONTACT"}}
            with self.session.put("https://ethermail.io/api/users/configuration-paywall", json=payload) as response:
#                 print(response.text)
                time.sleep(random.randint(1,9)/10)

                try:
                    if response.json()["status"] == 500:
                        continue
                    else:
                        pass
                except:
                    pass
            time.sleep(random.randint(1,9)/10)

            payload = {"paywall":{"typeWeb":"WEB3","configurationPaywall":"FILTER_ONLY_COMPANIES_MY_COMMUNITIES"}}
            with self.session.put("https://ethermail.io/api/users/configuration-paywall", json=payload) as response:
                # print(response.text)
                ...

            break

        message = encode_defunct(text="ThorProtocol: \n\nAPPID:ryYjjq9Ff2uhwhnWNo8Cr8aF")
        signed_message = w3.eth.account.sign_message(message, private_key=self.private)
        self.signature = signed_message["signature"].hex()

        payload = {"web3Signature":self.signature,"web3Address":f"{self.address.lower()}@ethermail.io"}
        time.sleep(random.randint(1,9)/10)
        with self.session.post("https://ethermail.io/api/users/keys", json=payload) as response:
            # print(response.text)
            ...
            # self.access_token = response.json()["token"]

        with self.session.get("https://ethermail.io/api/users/coins") as response:
            print(response.text)



    @property
    def nonce(self) -> str:

        payload = {"walletAddress":self.address.lower()}
        with self.session.post("https://ethermail.io/api/auth/nonce", json=payload) as response:

            if response.json()["success"]:
                # logger.success(f"{self.address} | Nonce успешно получен")
                ...
            else:
                logger.error(f"{self.address} | Ошибка при получении Nonce")

        return f"By signing this message you agree to the Terms and Conditions and Privacy Policy\n\nNONCE: {response.json()['nonce']}"

    @property
    def generate_user_agent(self) -> str:
        return ua_generator.generate(device='desktop',platform = 'windows', browser='chrome').text

    @property
    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


if __name__ == '__main__':

    print(' ___________________________________________________________________\n'
          '|                       Rescue Alpha Soft                           |\n'
          '|                   Telegram - @rescue_alpha                        |\n'
          '|                   Discord - discord.gg/438gwCx5hw                 |\n'
          '|___________________________________________________________________|\n\n\n')



    RefCount = (1,5)
    delay = (15,45)



    proxies = []
    addresses = []
    privates = []
    refCodes = []

    with open('InputData/RefCodes.txt', 'r') as file:
        for i in file:
            refCodes.append(i.rstrip())
    with open('InputData/Proxies.txt', 'r') as file:
        for i in file:
            proxies.append(i.rstrip())
    with open('InputData/Addresses.txt', 'r') as file:
        for i in file:
            addresses.append(i.rstrip())
    with open('InputData/Privates.txt', 'r') as file:
        for i in file:
            privates.append(i.rstrip())

    random.shuffle(refCodes)
    # print(refCodes)
    # input()


    count_def = 0

    for refCode in refCodes:

        count_ref = 0
        count_ref_ = random.randint(RefCount[0],RefCount[1])

        logger.success(f"Нагоняем {count_ref_} рефералов по реф-коду {refCode}")

        while count_ref < count_ref_:

            try:
                account = Ethermail(proxy = proxies[0],
                                    private = privates[count_def],
                                    address = addresses[count_def],
                                    refCode = refCode,
                                    logger = logger)

                result = account.Registration()

                count_ref+=1
                count_def+=1

                logger.success(f"{refCode} | {count_ref}/{count_ref_} ({addresses[count_def-1]})")
            except Exception as e:
                traceback.print_exc()
                logger.error(f"{refCode} | {count_ref}/{count_ref_} ({addresses[count_def - 1]})")

            time.sleep(1)
            requests.get("")

            time.sleep(random.randint(delay[0], delay[1]))

        print('')


    input('Скрипт завершил работу...')


