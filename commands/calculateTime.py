import subprocess
from multiprocessing import Pool
from datetime import datetime
import string


class calculateTime:
    def __init__(self, newpage):
        self.newpage = newpage

    def calculateProb():
        return
    def timeEstimate():
        return
    def run(self):
        self.newpage()
       
        includes_upper = input("Does the password include uppercase letters? (y/n): ").strip().lower() == 'y'
        includes_lower = input("Does the password include lowercase letters? (y/n): ").strip().lower() == 'y'
        includes_numbers = input("Does the password include numbers? (y/n): ").strip().lower() == 'y'
        includes_symbols = input("Does the password include symbols? (y/n): ").strip().lower() == 'y'

        charset = ""
        if includes_upper:
            charset += string.ascii_uppercase
        if includes_lower:
            charset += string.ascii_lowercase
        if includes_numbers:
            charset += string.digits
        if includes_symbols:
            charset += string.punctuation
