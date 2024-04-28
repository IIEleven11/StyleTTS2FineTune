import pysrt
from pydub import AudioSegment
import os
from phonemizer import phonemize
import glob
from tqdm import tqdm

output_dir = './segmentedAudio/'   # path to where you want the segmented audio to go. dont touch this unless youre having issues
bad_audio_dir = './badAudio/' # path to where you want the bad audio to go. dont touch this unless youre having issues
srt_dir = './srt/'
audio_dir = './audio/'

os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)
os.makedirs(srt_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)
os.makedirs('./trainingdata', exist_ok=True)

srt_list = glob.glob("./srt/*.srt") # Gets a list of all srt files
audio_list = glob.glob("./audio/*.wav") # Gets a list of all audio files


if len(srt_list) == 0 or len(audio_list) == 0:
    raise Exception(f"You need to have at least 1 srt file and 1 audio file, you have {len(srt_list)} srt and {len(audio_list)} audio files!")


print(f"SRT Files: {len(srt_list)}")


for sub_file in tqdm(srt_list):  # Iterate over all srt files
    subs = pysrt.open(sub_file)
    audio_name = os.path.basename(sub_file).replace(".srt", ".wav")

    audio = AudioSegment.from_wav(f'./{audio_dir}/{audio_name}')
    with open('./trainingdata/output.txt', 'a+') as out_file:
        last_end_time = 0
   
   
    buffer_time = 200  # adds an amount of time in ms to that creates a buffer zone around the subtitles
    max_allowed_gap = 1.5 * buffer_time  # maximum gap between subtitles that the script will tolerate without adding additional buffer time.
    
    '''explanation of the above 2 variables and following code block:
    
    I noticed that dataset quality really suffers from poor cuts. Usually because it didnt let the speaker fully end a sentence or word. we usually dont stop all sound right away, 
    it should trail off.
    So I create a buffer zone around the subtitle to provide more room for error.
    The script iterates through each subtitle and calculates the gap to the next subtitle.
    if the gap is greater than max_allowed_gap, the script adds buffer_time to the current subtitle's end time to ensure there is enough
    silence before the next spoken word begins.
    The only things you should adjust in this script is the buffer_time variable, max_allowed_gap, and the duration range in the last if statement.
    
    The process I went through was to adjust buffer_time then run the script, listen to your segments in order. If you hear overlapping, artifacts between clips, and or cut off speech then adjust buffer_time. 
    I left the values I ended up using in the script. They may work as default for you, they may not.
    '''
    
    
    with open('./trainingdata/output.txt', 'a+') as out_file:
    
        for i, sub in enumerate(subs):
            # get start and end times in milliseconds
            start_time = (sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
            end_time = (sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.start.milliseconds
    
            if i < len(subs) - 1:
     
                next_sub = subs[i + 1]
                next_start_time = (next_sub.start.minutes * 60 + next_sub.start.seconds) * 1000 + next_sub.start.milliseconds
                # get the gap to the next subtitle
                gap_to_next = next_start_time - end_time
    
                # If gap to next subtitle is larger than the max allowed gap the we add buffer time to the end time
                if gap_to_next > max_allowed_gap:
                    end_time += buffer_time
                    print(f"Added buffer time to segment {i}: New end_time = {end_time}")
                else:
                    # else, adjust the end time by the smaller of the buffer time and half the gap to the next subtitle
                    adjustment = min(buffer_time, gap_to_next // 2)
                    end_time += adjustment
                    print(f"Adjusted end_time for segment {i} by {adjustment}ms due to small gap: New end_time = {end_time}")
            else:
                # If this is the last subtitle, add the buffer time to the end time
                end_time += buffer_time
                print(f"Added buffer time to the last segment {i}: New end_time = {end_time}")
    
            audio_segment = audio[start_time:end_time]
            duration = len(audio_segment)
            filename = f'{audio_name[:-4]}_{i}.wav'
    
            # If the duration is within the desired range, then we keep, anything outside this range goes into the badAudio folder
            if 1850 <= duration <= 12000:   # Adjust these values to your desired range
     
                audio_segment.export(os.path.join(output_dir, filename), format='wav')
                out_file.write(f'{filename}|{sub.text}|1\n')
            else:
                audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')
