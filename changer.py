import os
import random
import string
import requests
import json
import threading
import tls_client
from colorama import Fore, Style
import datetime
from datetime import datetime
import ctypes

try:
    import tls_client
    import random
    import string
    import requests
    import json
except ModuleNotFoundError:
    i = 0
    imports = [
        "requests",
        "tls_client",
    ]
    for _import in imports:
        i += 1
        print(f"Installing dependencies... ({i}/2)")
        print(f"installing {_import}")
        os.system(f'pip install {_import} > nul')
    import tls_client
    import random
    import string
    import requests


class Files:
    @staticmethod
    def write_config():
        if not os.path.exists("config.json"):
            data = {
                "Proxies": False,
                "Custom_Password": False,
                "Password": ""
            }
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def write_files():
        files = [
            "tokens.txt", 
            "proxies.txt",
            "new_tokens.txt"
        ]
        for file in files:
            if not os.path.exists(file):
                with open(f"{file}", "a") as f:
                    f.close()

    @staticmethod
    def run_tasks():
        tasks = [Files.write_config, Files.write_files]
        for task in tasks:
            task()

Files.run_tasks()

session = tls_client.Session(client_identifier="chrome_120",random_tls_extension_order=True)

with open("proxies.txt") as f:
    proxies = f.read().splitlines()

with open("config.json") as f:
    Config = json.load(f)

proxy = Config["Proxies"]
Password = Config["Password"]
Custom_Password = Config["Custom_Password"]

if proxy:
    session.proxies = {
        "http": f"http://{random.choice(proxies)}",
        "https": f"http://{random.choice(proxies)}",
    }

class Change:
    def get_random_str(self, length: int) -> str:
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

    def get_discord_cookies(self):
        try:
            response = requests.get("https://canary.discord.com")
            if response.status_code == 200:  # Updated this line
                return "; ".join(
                    [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                ) + "; locale=en-US"
            else:
                return "__dcfduid=4e0a8d504a4411eeb88f7f88fbb5d20a; __sdcfduid=4e0a8d514a4411eeb88f7f88fbb5d20ac488cd4896dae6574aaa7fbfb35f5b22b405bbd931fdcb72c21f85b263f61400; __cfruid=f6965e2d30c244553ff3d4203a1bfdabfcf351bd-1699536665; _cfuvid=rNaPQ7x_qcBwEhO_jNgXapOMoUIV2N8FA_8lzPV89oM-1699536665234-0-604800000; locale=en-US"
        except Exception as e:
            print(e)
        
    def Headers(self, token):
        return {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en',
            'authorization': token,
            'content-type': 'application/json',
            'cookie': self.get_discord_cookies(),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en',
            'x-discord-timezone': 'Europe/Warsaw',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjAuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjAuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjU2MjMxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        }
    
    def Changer(self, token, password, email, new_pass):
        try:
            
            headers = self.Headers(token)

            data = {
                'password': password,
                'new_password': new_pass,
            }
            ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
            response = session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=data)
            if response.status_code == 200:
                new_token = response.json()['token']
                success = ts + Fore.GREEN + "     [SUCCESS]  " + Fore.RESET
                print(f"{success} Changed ({email}) → {new_token[:22]}*****")
                # Remove the account from tokens.txt
                with open('tokens.txt', 'r') as file:
                    lines = file.readlines()
                with open('tokens.txt', 'w') as file:
                    for line in lines:
                        if not line.startswith(email):
                            file.write(line)
                return f'69:{email}:{new_pass}:{new_token}'
            elif response.status_code == 40002:
                failed = ts + Fore.RED + "     [FAILED]  " + Fore.RESET
                print(f"{failed} Failed to change {email} → {token} is locked")
                return f'07:{email}:{password}:{token}'
            else:
                error = ts + Fore.YELLOW + "     [ERROR]  " + Fore.RESET
                print(f"{error} Failed to change → ({email})")
                return f'07:{email}:{password}:{token}'
        except Exception as e: 
            print(e)   


class ChangeAccountThread(threading.Thread):
    def __init__(self, token, password, email, new_pass):
        threading.Thread.__init__(self)
        self.token = token
        self.password = password
        self.email = email
        self.new_pass = new_pass

    def run(self):
        new_combo = Change().Changer(self.token, self.password, self.email, self.new_pass)
        if new_combo:
            if new_combo.split(':')[0] == '69':
                with open('new_tokens.txt', 'a') as f:
                    f.write(new_combo.split(':')[1] + ':' + new_combo.split(':')[2] + ':' + new_combo.split(':')[3] + '\n')
            else:
                with open('failed.txt', 'a') as f:
                    f.write(new_combo.split(':')[1] + ':' + new_combo.split(':')[2] + ':' + new_combo.split(':')[3] + '\n')
        else:
            print("Error occurred while processing:", self.email)

for _ in range(1000):
    print("This code is leaked in https://github.com/bbsitauah1337/smm-discord-panel-bot and credits to sociality.lol")
    
os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleW("sociality.lol | Discord Token/Password Changer")
    print(Fore.LIGHTBLUE_EX + """                 _       _ _ _           _       _ 
                (_)     | (_) |         | |     | |
  ___  ___   ___ _  __ _| |_| |_ _   _  | | ___ | |
 / __|/ _ \ / __| |/ _` | | | __| | | | | |/ _ \| |
 \__ \ (_) | (__| | (_| | | | |_| |_| |_| | (_) | |
 |___/\___/ \___|_|\__,_|_|_|\__|\__, (_)_|\___/|_|
                                  __/ |            
                                 |___/             
                                                                                        
                                                                                        
                     Discord Token/Password Changer | sociality.lol \n\n""" + Fore.RESET)
    with open(f"tokens.txt") as f:
        combo = f.read().splitlines()
    combo = list(set(combo))
    if len(combo) == 0:
        error = Fore.YELLOW + "     [ERROR]  " + Fore.RESET
        print(f"{error} Add your tokens in tokens.txt in this format: email:password:token")
        ext = Fore.BLUE + "     [EXIT]  " + Fore.RESET
        input(ext + "Please press the \"Enter\" key to close the application\n")

    if Custom_Password:
        new_pass = Password
    else:
        new_pass = Change().get_random_str(20)

    threads = []
    for account in combo:
        if len(account.split(':')) != 3:
            
            ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
            error = ts + Fore.YELLOW + "     [ERROR]  " + Fore.RESET
            print(f"{error} Invalid token format: {account} (Format: email:pass:token). Skipping...")
            continue
        email = account.split(':')[0]
        password = account.split(':')[1]
        token = account.split(':')[2]

        thread = ChangeAccountThread(token, password, email, new_pass)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    ext = Fore.BLUE + "     [EXIT]  " + Fore.RESET
    input(ext + "Please press the \"Enter\" key to close the application\n")
