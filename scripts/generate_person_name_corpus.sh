#!/bin/bash


echo "Setting up workspace"
mkdir tmp
mkdir data


echo "Cleanup artifacts"
rm tmp/names.txt
rm data/name_corpus.txt


echo "Downloading source data"
curl -o tmp/first_names.zip https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/v3/first_names.zip
curl -o tmp/last_names.zip https://raw.githubusercontent.com/philipperemy/name-dataset/master/names_dataset/v3/last_names.zip
unzip -o tmp/first_names.zip -d tmp
unzip -o tmp/last_names.zip -d tmp


echo "Sanitizing data"
python -c "

import json
import re


VOWELS = 'aeiouy'
CONSTONANTS = 'bcdfghjklmnpqrstvwxz'


def is_english(char):
	ascii_value = ord(char)
	return (ascii_value >= 65 and ascii_value <= 90) or (ascii_value >= 97 and ascii_value <= 122)


def is_valid(name):
	# remove empty strings
	if 0 == len(name):
		return False

	# remove names with invalid characters
	for char in name:
		if not char.isspace() and not char.isalpha() and not '-' != char:
			return False
		if not char.isprintable():
			return False
		if char in '#()./:[]*':
			return False
		if not is_english(char):
			return False

	# filter out all names with 3 repeating characters
	pattern = re.compile('(.)\\\\1\\\\1', re.IGNORECASE)
	if 0 != len(pattern.findall(name)):
		return False

	# remove strings with one unique character
	if 1 == len(set(c for c in name)):
		return False

	# check if string only contains characters that are constonants
	pattern = re.compile('^['+CONSTONANTS+']+$', re.IGNORECASE)
	if 0 != len(pattern.findall(name)):
		return False

	# name looks valid
	return True


def normalize(name):
	return name.lower().strip()


with open('tmp/names.txt', 'w', encoding='utf-8') as outfh:
	files = ['tmp/first_names.json', 'tmp/last_names.json']
	for file in files:
		print(file)
		with open(file, 'r', encoding='utf-8') as infh:
			data = json.loads(infh.read())
			for key in data.keys():
				for name in key.split(' '):
					name = normalize(name)
					if is_valid(name):
						outfh.write(name + '\n')

"


echo "Removing duplicates"
sort tmp/names.txt | uniq > data/name_corpus.txt


