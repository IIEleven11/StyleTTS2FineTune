import auditok

# Load audio file
audio_regions = auditok.split(
    "/home/eleven/StyleGuide/makeDataset/vits_scripts/wav_file_here/Newdataset24khz11_24.wav", # path to single wav file
    min_dur=2,  # minimum duration of a valid audio event in seconds
    max_dur=12,  # maximum duration of an event
    max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
    energy_threshold=35,  # threshold of detection
)

for i, region in enumerate(audio_regions):
    region.save(f"/home/eleven/StyleGuide/makeDataset/vits_scripts/segmentedAudio/audio{i}.wav") # output folder/audio{i}.wav
