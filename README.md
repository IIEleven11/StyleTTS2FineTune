# StyleTTS2 Fine-Tuning Guide

This repository provides a guide on how to prepare a dataset and execute fine-tuning using the StyleTTS2 process. https://github.com/yl4579/StyleTTS2

- A ~gradio webui~ text generation webui extension providing TTS with your fine tuned model will be finished soon.

## Changelog

- **1/12/2024**: Updated Readme for clarity and specifying seperate windows and linux whisperx commands.
- **1/12/2024**: Added the ability to work with multiple SRT and Audio files at one time for large datasets or blended voices. - @78Alpha
- **12/6/23**: I noticed segmentation from the whisperx .json was unacceptable. I created a segmentation script that uses the .srt file that the whisperx command generates. From what I can tell this is significantly more accurate. This could be dataset specific. Use the json segmenter if needed.
- **12/5/23**: Fixed a missing "else" in the Segmentation script.
- **12/4/23**: A working config_ft.yml file is available in the tools folder.
- **12/2/23**: Rewrote Segmentation and Transcription scripts.

## Compatibility

The scripts are compatible with WSL2 and Linux. Windows requires additional dependencies and might not be worth the effort.

## Setup

### Environment Setup

1. Install conda and activate environment with Python 3.10:
   - conda create --name dataset python==3.10
   - conda activate dataset

## Install Pytorch

    - pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -U

## Install whisperx/phonemize and segmentation packages

    - pip install git+https://github.com/m-bain/whisperx.git
    - pip install phonemizer pydub pysrt

## Instal TQDM progress bar

    - pip install tqdm

### Data Preparation

1. Change directory to where you have unpacked StyleTTSFineTune (You should see the makeDataset folder)
2. To make base directories you can run segmenter script. It will create the folders.

   1. run python srtsegmenter.py
3. Add WAV audio file/s to the audio directory (remove special characters, brackets, parenthesis to prevent issues)
4. Run the following command to generate srt files for all files in the audio folder:

   - Linux - for i in ../audio/*.wav; do whisperx "$i" --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H; done
   - Windows - in a powershell terminal copy and paste the following after verifying path to audio folder:

   "Get-ChildItem -Path "\StyleTTS2FineTune\\makeDataset\\tools\\audio" -Filter *.wav | ForEach-Object {whisperx $_.FullName --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H"

   This will generate a Whisperx .SRT file transcription of your audio. Place the srt file/s into the srt folder

### Segmentation and Transcription

1. Navigate to the main directory (You should see the folder makeDataset)
2. Run the segmentation script (python makeDataset/tools/srtsegmenter.py:

The above steps will generate a set of segmented audio files, a folder of bad audio it didn't like, and an output.txt file. I have it set to throw out segmemts under one second and over 11.6 seconds. You can adjust this to varying degrees.

### Phonemization

1. Run the script (python makeDataset/tools/phonemized.py.
2. This script will create the train_list.txt and val_list.txt files.

- OOD_list.txt comes from the LibriTTS dataset. The following are some things to consider taken from the notes at https://github.com/yl4579/StyleTTS2/discussions/81. There is a lot of good information there, I suggest looking it over.

1. The LibriTTS dataset has poor punctuation and a mismatch of spoken/unspoken pauses with the transcripts. This is a common oversight in many datasets.
2. Also it lacks variety of punctuation. In the field, you may encounter texts with creative use of dashes, pauses and combination of quotes and punctuation. LibriTTS lacks those cases. But the model can learn these!
3. Additionally, LibriTTS has stray quotes in some texts, or begins a sentence with a quote. These things reduce quality a little (or a lot, sometimes). You will want to filter those out.
4. Creating your own ODD_list.txt is an option. I need to play around with it more, the only real requirements should be good punctuation and that it contains text the model has not seen. I'm not sure what the ideal size of this list should be though.

- At this point, you should have everything you need to fine-tune.

## Fine-Tuning with StyleTTS2

1. Clone the StyleTTS2 repository and navigate to its directory:

   - git clone https://github.com/yl4579/StyleTTS2.git
2. Install the required packages:

   - cd StyleTTS2
   - pip install -r requirements.txt
   - sudo apt-get install espeak-ng
3. Prepare the data and model:

   - Clear the wavs folder in the data directory and replace with your segmented wav files.
   - Replace the val_list and train_list files in the Data folder with yours. Keep the OOD_list.txt file.
   - Adjust the parameters in the config_ft.yml file in the Configs folder according to your needs.
4. Download the [StyleTTS2-LibriTTS model](https://huggingface.co/yl4579/StyleTTS2-LibriTTS) and place it in the Models/LibriTTS directory.

## Run

Finally, you can start the fine-tuning process with the following command:

- accelerate launch --mixed_precision=fp16 --num_processes=1 train_finetune_accelerate.py --config_path ./Configs/config_ft.yml
