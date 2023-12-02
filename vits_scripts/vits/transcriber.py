import os
from phonemizer import phonemize
import speech_recognition as sr
from text import _clean_text
import random 
import re

def transcribe_audio_files_in_directory(
    directory_path, output_directory, bad_audio_directory
):
    r = sr.Recognizer()
    os.makedirs(bad_audio_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)

    with open(os.path.join(output_directory, "alldata.txt"), "w", newline="") as all_data_file, \
         open(os.path.join(output_directory, "train_data.txt"), "w", newline="") as train_data_file:

        filenames = sorted(os.listdir(directory_path), key=lambda x: int(re.search(r'\d+', x).group()))
        
        for filename in filenames:
            if filename.endswith(".wav"):
                file_path = os.path.join(directory_path, filename)

                with sr.AudioFile(file_path) as source:
                    audio = r.record(source)
                    try:
                        transcription = r.recognize_google(audio)
                        all_data_file.write(f"{filename}|{transcription}|1\n")

                        # clean transcription
                        cleaned_transcription = _clean_text(
                            transcription, ["english_cleaners2"]
                        )
                        # phonemize
                        phonemized_transcription = phonemize(
                            cleaned_transcription, language="en-us"
                        )
                        train_data_file.write(f"{filename}|{phonemized_transcription}|1\n")
                    except sr.UnknownValueError:
                        print(
                            f"Google Web Speech API could not understand audio for file: {filename}. Moving it to badAudio directory."
                        )
                        os.rename(
                            file_path, os.path.join(bad_audio_directory, filename)
                        )
                    except sr.RequestError as e:
                        print(
                            "Could not request results from Google Web Speech API service; {0}".format(
                                e
                            )
                        )

def create_validation_set(train_data_path, val_list_path, percentage=0.1):
    with open(train_data_path, 'r') as f:
        lines = f.readlines()

    # random subset of lines for validation
    val_size = int(len(lines) * percentage)
    val_lines = random.sample(lines, val_size)

    with open(val_list_path, 'w') as f:
        f.writelines(val_lines)

    train_lines = [line for line in lines if line not in val_lines]
    with open(train_data_path, 'w') as f:
        f.writelines(train_lines)

# Transcribe audio files
transcribe_audio_files_in_directory(
    "/home/eleven/StyleGuide/makeDataset/segmentedAudio", # path to segmentedAudio folder here
    "/home/eleven/StyleGuide/makeDataset/trainingdata", #path to the trainingdata folder
    "/home/eleven/StyleGuide/makeDataset/vits_scripts/badAudio", # put your path to the badAudio folder here
)
# Create validation set
create_validation_set(
    "/home/eleven/StyleGuide/makeDataset/trainingdata/train_data.txt", # path to train_data.txt
    "/home/eleven/StyleGuide/makeDataset/trainingdata/val_list.txt" # path to val_list.txt
)
