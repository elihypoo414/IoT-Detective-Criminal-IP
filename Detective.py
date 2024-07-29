import requests
import argparse
import banner
import ipaddress
from tqdm import tqdm

QUERY = [
	"D-Link IP Camera",
	"WVC80N",
	"ExacqVision",
	"AXIS webcams",
	"JUNG KNX",
	"Jeedom",
	"Somfy alarm system",
	"polycom command shell",
]

def get_args():
	parser = argparse.ArgumentParser(
		description="Do a security check on your IoT products!"
	)
	parser.add_argument(
		"-k", "--key", type=str, required=True, help="Enter the CIP API key"
	)
	parser.add_argument(
		"-i", "--ip", type=str, required=True, help="Enter the IP address"
	)
	return parser.parse_args()

def check_key(key):
	url = "https://api.criminalip.io/v1/user/me"
	payload = {}
	headers = {
		"x-api-key": key
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	if response.status_code != 200:
		return False, None
	response = response.json()
	name = response["data"]["name"]
	return True, name

def check_ip(ip):
	try:
		ipaddress.ip_address(ip)
		return True
	except ValueError:
		return False

def extract_cve(ip, key):
	url = f"https://api.criminalip.io/v1/asset/ip/report?ip={ip}"
	payload={}
	headers = {
	"x-api-key": key
	}
	response = requests.request("GET", url, headers=headers, data=payload)

	vulns = response.json()["vulnerability"]["data"]
	cve_id = []
	for vuln in vulns:
		cve_id.append(vuln["cve_id"])

	cve_id = list(set(cve_id))
	print("Your IoT device is at risk of the following vulnerabilities:")
	for i in cve_id:
		print(i)


def check_iot(ip, key):
    url = "https://api.criminalip.io/v1/banner/search?query=ssh&offset=0"
    payload={}
    headers = {
  		"x-api-key": key
	}	
    has_cve = False
    progress_bar = tqdm(
        QUERY,
        desc="Investigating,,,",
        ncols=100,
        bar_format="{l_bar}{bar}| {percentage:3.0f}%",
        colour="green",
    )
    for q in progress_bar:
        url = f"https://api.criminalip.io/v1/banner/search?query={q} ip:{ip}&offset=0"
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        data = response["data"]["result"]
        if len(data) == 0:
            continue
        q_has_cve = data[0]["has_cve"]
        if q_has_cve == True:
            has_cve = True
    if has_cve == False:
        print("🎉 Your IP does not have IoT devices or is safe! 🎉")
    else:
        print(
            "🚨 Investigation Finds Your IoT Is Not Safe! We will conduct further investigations 🚨"
        )
        extract_cve(ip, key)

def main():
	args = get_args()
	check, name = check_key(args.key)
	if check == False:
		print("Invalid API key. Please try again.")
		exit()
	check = check_ip(args.ip)
	if check == False:
		print("Invalid IP address. Please try again.")
		exit()
	banner.print_ascii()
	print(f"Welcome, {name}!")
	print("Your IP : ", args.ip)
	check_iot(args.ip, args.key)


if __name__ == "__main__":
	main()
