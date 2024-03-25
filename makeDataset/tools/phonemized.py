import argparse
from phonemizer import phonemize
import os
from tqdm import tqdm

# Create an argument parser
parser = argparse.ArgumentParser(description='Phonemize transcriptions.')
parser.add_argument('--language', type=str, default='en-us',
                    help='The language to use for phonemization.')

args = parser.parse_args()

with open('./trainingdata/output.txt', 'r') as f: # Path to output.txt
    lines = f.readlines()

# Phonemize the transcriptions
phonemized = []
filenames = []
transcriptions = []
speakers = []
phonemized_lines = []
for line in lines:  # Split filenames, text and speaker without phonemizing. Prevents memory protection error.
    filename, transcription, speaker = line.strip().split('|')
    filenames.append(filename)
    transcriptions.append(transcription)
    speakers.append(speaker)

phonemized = phonemize(transcriptions, language=args.language, backend='espeak')  # Phonemize all text in one go to avoid triggering the memory protections error

for i in tqdm(range(len(filenames))):  # Build the expected train_list
    phonemized_lines.append((filenames[i], f'{filenames[i]}|{phonemized[i]}|{speakers[i]}\n'))

# Sort
phonemized_lines.sort(key=lambda x: int(x[0].split('_')[1].split('.')[0]))

# Split training set and validation set
train_lines = phonemized_lines[:int(len(phonemized_lines) * 0.9)]
val_lines = phonemized_lines[int(len(phonemized_lines) * 0.9):]

with open('./trainingdata/train_list.txt', 'w+') as f: # Path for train_list.txt in the training data folder
    for _, line in train_lines:
        f.write(line)

with open('./trainingdata/val_list.txt', 'w+') as f:  # Path for val_list.txt in the training data folder
    for _, line in val_lines:
        f.write(line)
