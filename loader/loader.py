import requests
#import os

AOC2019_URL = "https://adventofcode.com/2019/day/?/input"
COOKIEPATH = "sessioncookie.txt"

def get_sessioncookie():
    with open(COOKIEPATH) as ifile:
        return ifile.read()

def request_input(url):
    nomnom = {"session": get_sessioncookie()}
    r = requests.get(url, cookies=nomnom)
    return r.text

# Prompt user for AoC day
day = int(input("Enter Advent of Code Day?: "))
assert 1 <= day <= 25, "Invalid day!"

# Request data from AoC website by formatting url
data = request_input(AOC2019_URL.replace("?", str(day)))

# For now, output path will be in the same directory
with open("input.txt", mode="w") as ofile:
    ofile.write(data)
