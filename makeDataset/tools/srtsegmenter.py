import pysrt
from pydub import AudioSegment
import os
from phonemizer import phonemize
import glob
from tqdm import tqdm

srt_list = glob.glob("./srt/*.srt")

audio_list = glob.glob("./audio/*.wav")

output_dir = './segmentedAudio/'   # path to where you want the segmented audio to go
bad_audio_dir = './badAudio/'  # path to where you want the bad audio to go

# os.makedirs(output_dir, exist_ok=True)
# os.makedirs(bad_audio_dir, exist_ok=True)

                   # path to /output.txt
print(f"Processing: {len(srt_list)}")
for sub_file in tqdm(srt_list):
    subs = pysrt.open(sub_file)  # Path to .srt file
    audio_name = os.path.basename(sub_file).replace(".srt", ".wav")

    audio = AudioSegment.from_wav(f'./audio/{audio_name}')  # path to .wav file
    with open('./trainingdata/output.txt', 'a+') as out_file:
        for i, sub in enumerate(subs):

            start_time = (sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
            end_time = (sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds

            audio_segment = audio[start_time:end_time]

            duration = len(audio_segment)

            filename = f'{audio_name}_{i}.wav'
            if 1000 <= duration <= 11600: # This part throws out audio segments under 1 second and over 11.6 seconds
                audio_segment.export(os.path.join(output_dir, filename), format='wav')
                out_file.write(f'{filename}|{sub.text}|1\n')
            else:
                audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')


            #phonemized_text = phonemize(sub.text, language='en-us') # I was experimenting with phonemized .srt files. You can comment this out if you want
            #phonemized_file.write(f'{i}\n{str(sub.start)} --> {str(sub.end)}\n{phonemized_text}\n\n')
