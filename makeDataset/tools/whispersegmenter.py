## the WAV2VEC2_ASR_LARGE_LV60K_960H model was trained on a 16khz dataset. But whisperx will also work with your 24khz audio. I've been playing around with it, will update if I get better results.


import json
from pydub import AudioSegment
import os


with open('/StyleGuide/audio.json', 'r') as f: # Path to whisperx json
    transcription = json.load(f)
    
audio = AudioSegment.from_wav('/StyleGuide/makeDataset/audio.wav') #  Path to original wav file


output_dir = 'StyleGuide/makeDataset/segmentedAudio' # path to where you want segmented audio to go
bad_audio_dir = '/StyleGuide/makeDataset/badAudio' # Path to badaudio folder

os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)


with open('/StyleGuide/makeDataset/trainingdata/output.txt', 'w') as out_file: # path to training data folder/output.txt
    for i, segment in enumerate(transcription['segments']):
        start_time = segment['start'] * 1000
        end_time = segment['end'] * 1000
        duration = end_time - start_time
        audio_segment = audio[start_time:end_time]
        filename = f'segment_{i}.wav'

        
        if 1500 <= duration <= 11600:  # Check between 1.5 and 11.6 seconds (converted to milliseconds) You can play with these if you want
            audio_segment.export(os.path.join(output_dir, filename), format='wav')
            out_file.write(f'{filename}|{segment["text"]}|1\n')
        else:
            audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')
