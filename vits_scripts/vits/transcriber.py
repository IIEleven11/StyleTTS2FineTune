import os
from phonemizer import phonemize
import speech_recognition as sr
from text import _clean_text

def transcribe_audio_files_in_directory(
    directory_path, output_directory, bad_audio_directory
):
    r = sr.Recognizer()

    # Create bad audio directory
    os.makedirs(bad_audio_directory, exist_ok=True)

    # Create output directory
    os.makedirs(output_directory, exist_ok=True)

    # Open two files: one for raw transcriptions, one for phonemized transcriptions
    with open(os.path.join(output_directory, "alldata.txt"), "w", newline="") as all_data_file, \
         open(os.path.join(output_directory, "train_data.txt"), "w", newline="") as train_data_file:

        filenames = sorted(os.listdir(directory_path))

        for filename in filenames:
            if filename.endswith(".wav"):
                file_path = os.path.join(directory_path, filename)

                with sr.AudioFile(file_path) as source:
                    audio = r.record(source)
                    try:
                        # transcribe
                        transcription = r.recognize_google(audio)
                        # write raw transcription to all_data_file
                        all_data_file.write(f"{filename}|{transcription}|1\n")

                        # clean the transcription
                        cleaned_transcription = _clean_text(
                            transcription, ["english_cleaners2"]
                        )
                        # phonemize the cleaned transcription
                        phonemized_transcription = phonemize(
                            cleaned_transcription, language="en-us"
                        )
                        # write phonemized transcription to train_data_file
                        train_data_file.write(f"{filename}|{phonemized_transcription}|1\n")
                    except sr.UnknownValueError:
                        print(
                            f"Google Web Speech API could not understand audio for file: {filename}. Moving it to badAudio directory."
                        )
                        # move bad audio badAudio directory
                        os.rename(
                            file_path, os.path.join(bad_audio_directory, filename)
                        )
                    except sr.RequestError as e:
                        print(
                            "Could not request results from Google Web Speech API service; {0}".format(
                                e
                            )
                        )

transcribe_audio_files_in_directory(
    "/home/eleven/StyleGuide/makeDataset/vits_scripts/segmentedAudio", # path to segmentedAudio folder here
    "/home/eleven/StyleGuide/makeDataset/trainingdata", # path to the trainingdata folder
    "/home/eleven/StyleGuide/makeDataset/vits_scripts/badAudio", # put your path to the badAudio folder here
)