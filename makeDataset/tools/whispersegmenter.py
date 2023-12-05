import json
from pydub import AudioSegment
import os


with open('/TTS/recipes/ljspeech/xtts_v2/16khxtts2.json', 'r') as f: # Path to whisperx json
    transcription = json.load(f)
    
audio = AudioSegment.from_wav('/TTS/recipes/ljspeech/xtts_v2/16khxtts2.wav') #  Path to original wav file

# Define the output directories
output_dir = '/TTS/recipes/ljspeech/xtts_v2/training/segmentedAudio' # path to where you want segmented audio to go
bad_audio_dir = '/TTS/recipes/ljspeech/xtts_v2/training/badAudio' # Path to badaudio folder

os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)


with open('/TTS/recipes/ljspeech/xtts_v2/training/output.txt', 'w') as out_file: # path to training data folder /output.txt
    for i, segment in enumerate(transcription['segments']):
        start_time = segment['start'] * 1000 
        end_time = segment['end'] * 1000
        duration = (end_time - start_time) / 1000
        audio_segment = audio[start_time:end_time]
        filename = f'segment_{i}.wav'

        # Check between 1 and 11.6 seconds
        if 1 <= duration <= 11.6:
            audio_segment.export(os.path.join(output_dir, filename), format='wav')
            out_file.write(f'{filename}|{segment["text"]}|1\n')
        else:
            audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')
