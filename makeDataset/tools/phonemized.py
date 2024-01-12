from phonemizer import phonemize
import os
from tqdm import tqdm

with open('./trainingdata/output.txt', 'r') as f: # Path to output.txt
    lines = f.readlines()

# Phonemize the transcriptions
phonemized = []
filenames = []
transcriptions = []
speakers = []
phonemized_lines = []
for line in lines:
    filename, transcription, speaker = line.strip().split('|')
    filenames.append(filename)
    transcriptions.append(transcription)
    speakers.append(speaker)

phonemized = phonemize(transcriptions, language="en-us", backend='espeak')

for i in tqdm(range(len(filenames))):
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
