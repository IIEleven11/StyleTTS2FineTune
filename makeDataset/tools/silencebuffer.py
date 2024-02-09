from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load the WAV file
audio = AudioSegment.from_wav("full/path/to/wav/file.wav")


# Find silence. These are CRUCIAL. You need to play around with these values to get the best results. Took me about 20 min of testing.
chunks = split_on_silence(audio,
    min_silence_len= 232, # minimum length of silence required for a split in ms
    silence_thresh= -70 # volume threshold below which sound is considered silence
)

silence_chunk = AudioSegment.silent(duration=740)  # amount of silence you want to add in milliseconds

new_audio = AudioSegment.empty()
for chunk in chunks:
    new_audio += chunk + silence_chunk 


new_audio.export("silence_added_audio.wav", format="wav")