import pyfiglet
from termcolor import colored
import shutil
import os

def print_ascii():
	os.system("clear")
	columns, _ = shutil.get_terminal_size()
	banner_iot = (pyfiglet.figlet_format("IoT", font="sub-zero", width=columns)).split(
		"\n"
	)
	banner_detective = (
		pyfiglet.figlet_format("Detective", font="sub-zero", width=columns)
	).split("\n")
	banner_cip = (pyfiglet.figlet_format("Criminal IP", font="sub-zero", width=columns)).split(
		"\n"
	)

	print(colored("*" * columns, color="yellow"))
	for i in banner_iot:
		if i.strip() != "":
			print(f"{colored('*', color='yellow')}{colored(i.center(columns-2), color='light_blue')}{colored('*', color='yellow')}")
	for i in banner_detective:
		if i.strip() != "":
			print(f"{colored('*', color='yellow')}{colored(i.center(columns-2), color='light_blue')}{colored('*', color='yellow')}")
	for i in banner_cip:
		if i.strip() != "":
			print(f"{colored('*', color='yellow')}{colored(i.center(columns-2), color='light_blue')}{colored('*', color='yellow')}")
	print(colored("*" * columns, color="yellow"))
