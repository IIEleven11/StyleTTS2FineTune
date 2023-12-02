from phonemizer import phonemize
import os

with open('/home/eleven/StyleGuide/makeDataset/trainingdata/output.txt', 'r') as f: # Path to output.txt
    lines = f.readlines()

# Phonemize the transcriptions
phonemized_lines = []
for line in lines:
    filename, transcription, speaker = line.strip().split('|')
    phonemes = phonemize(transcription, language='en-us', backend='espeak')
    phonemized_lines.append((filename, f'{filename}|{phonemes}|{speaker}\n'))

# Sort
phonemized_lines.sort(key=lambda x: int(x[0].split('_')[1].split('.')[0]))

# Split training set and validation set
train_lines = phonemized_lines[:int(len(phonemized_lines) * 0.9)]
val_lines = phonemized_lines[int(len(phonemized_lines) * 0.9):]

with open('/home/eleven/StyleGuide/makeDataset/trainingdata/train_list.txt', 'w') as f: # Path for train_list.txt in the training data folder
    for _, line in train_lines:
        f.write(line)

with open('/home/eleven/StyleGuide/makeDataset/trainingdata/val_list.txt', 'w') as f:  # Path for val_list.txt in the training data folder
    for _, line in val_lines:
        f.write(line)