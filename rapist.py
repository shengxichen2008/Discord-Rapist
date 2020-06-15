import requests
import random
from colorama import Fore, Back, Style
from colorama import init

init()

with open("ascii.txt", "r", encoding="utf8") as f:
	print(Fore.RED + f.read() + Fore.WHITE)

def readCodesFromFile():
	with open("codes.txt", "r") as f:
		return f.readlines()

proxy_list = []

with open("proxies.txt", "r") as f:
	for proxy in f.readlines():
		proxy_list.append(proxy.replace("\n", ""))

def checkCodes():
	validCodes = 0
	badCodes = 0
	timeout = input("Please enter the timeout(seconds) for 'discordapp.com' >> ")
	with open("valid.txt", "w") as validFile:
		with open("bannedProxies.txt", "w") as f:
			for code in readCodesFromFile():
				if(len(code) >= 16):
					proxies = {
					"https":"https://" + random.choice(proxy_list)
					}
					url = "https://discordapp.com/api/v6/entitlements/gift-codes/" + code.replace("\n", "") + "?with_application=false&with_subscription_plan=true"
					try:
						r = requests.get(url=url, proxies=proxies, timeout=int(timeout.replace("\n", "")))
						resp = r.text
						if("Unknown Gift Code" in resp):
							badCodes = badCodes + 1
							print(Fore.YELLOW + "[BAD]: Bad Code" + " | " + "[" + code.replace("\n", "") + "]")
						elif("You are being rate limited." in resp):
							print(Fore.RED + "[ERROR]: " + "Banned Proxy" + " | " + "[" + proxies["https"] + "]")
							f.writelines(proxies["https"] + "\n")
						else:
							validCodes = validCodes + 1
							details = resp.split(":")[1].split(",")[0]
							print(Fore.GREEN + "[VALID]: " + code.replace("\n", "") + " | " + details.replace("\n", ""))
							validFile.writelines(code)
					except Exception as e:
						print(Fore.RED + "[ERROR]: " + "Bad Proxy | " + "[" + proxies["https"] + "]")
						continue
				else:
					print("Please enter valid Codes in 'codes.txt'.")
			f.close()
			print(Fore.GREEN + "[DONE]: " + "CHECKER DONE!" + " | " + "Valid: " + str(validCodes) + " / " + "Bad: " + str(badCodes) + Fore.WHITE)
			input("Press any key to close the progran...")

checkCodes()