from pydub import AudioSegment
import os
import glob

# input path to segmentedAudio folder here and create the paddedAudio folder and put its path here as well.
source_dir = 'path/to/segmentedAudio/folder'
target_dir = 'path/to/paddedAudio/folder'

os.makedirs(target_dir, exist_ok=True)

wav_files = glob.glob(os.path.join(source_dir, '*.wav'))

for wav_file in wav_files:
    audio = AudioSegment.from_wav(wav_file)

    # duration of silence in ms
    silence = AudioSegment.silent(duration=400) # This is length of silence to pad beginning and end of segments. You can change this to whatever you want.
    new_audio = silence + audio + silence
    new_file_path = os.path.join(target_dir, os.path.basename(wav_file))
    new_audio.export(new_file_path, format='wav')

print("Processing complete. Modified files are saved in:", target_dir)
