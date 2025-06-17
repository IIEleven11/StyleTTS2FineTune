# StyleTTS2 Fine-Tuning Guide


## If you want to train/finetune your model on a cloud instance then check out this - [StyleTTS2 Cloud Instance](https://dash.simplepod.ai/account/explore/55/ref-eleven/rrit_HeJcKTczE4o9).
- Make an account
- Use this template with the RTX Pro 6000 Blackwell GPU. It has 96gb of VRAM.
- I pre-installed all the packages/environment so you will just need to swap your wavs folder in and your train_list.txt/val_list.txt then you're set and you can begin training/finetuning.
- You could also pick the RTX 5090 but Stts2 heavily depends on VRAM. You will get better quality the higher the VRAM gets.


This repository provides a guide on how to prepare a dataset and execute fine-tuning using the StyleTTS2 process. https://github.com/yl4579/StyleTTS2
### If you still need to curate your dataset. You might want to checkout https://github.com/IIEleven11/Automatic-Audio-Dataset-Maker. At the end you'll need to convert it from .csv to STTSv2's .txt format (train_list.txt and val_list.txt) but that should be easy.

## Compatibility

The scripts are compatible with WSL2 and Linux. Windows requires additional dependencies and might not be worth the effort.

## Setup

### Environment Setup

1. Install conda and activate environment with Python 3.10:
   - conda create --name dataset python==3.10
   - conda activate dataset

## Install Pytorch

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -U

## Install whisperx/phonemize and segmentation packages

   1. ``` pip install git+https://github.com/m-bain/whisperx.git ```
    
   2. ``` pip install phonemizer pydub pysrt tqdm ```

### Data Preparation

1. Change directory to where you have unpacked StyleTTSFineTune (You should see the makeDataset folder)
2. To make base directories you can run segmenter script. It will create the folders.

   1. run
      - ``` python srtsegmenter.py ```

3. Add WAV audio file/s to the audio directory (remove special characters, brackets, parenthesis to prevent issues)

4. **** This step isnt mandatory **** for the training process. You can run whisperx and segmentation without adding silence. If you do want to add silence then silencebuffer.py within the tools folder will go over your audio file, find the silent portions between sentences/breaks in speech, and add a specific length of silence to them. This could in theory provide a more accurate cut during the segmentation process. You MUST adjust the parameters within the script to fit your data. I left the values that worked for my dataset in the code, you can try them as defaults if you wish.

5. Run the following command to generate srt files for all files in the audio folder:

   - Linux -
     ```
     for i in ../audio/*.wav; do whisperx "$i" --model large-v3 --output_format srt --condition_on_previous_text True --max_line_width 250  --max_line_count 1  --segment_resolution sentence  --align_model WAV2VEC2_ASR_LARGE_LV60K_960H; done
     ```
   - Windows - in a powershell terminal copy and paste the following after verifying path to audio folder:

     ```
      Get-ChildItem -Path 'C:\path\to\wav\folder' -Filter *.wav | ForEach-Object { whisperx $_.FullName --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H }
     ```

   This will generate a Whisperx .SRT file transcription of your audio. Place the srt file/s into the srt folder

### Segmentation and Transcription

1. Navigate to the main directory (You should see the folder makeDataset)
2. Within srtsegmenter.py are some variables to adjust. buffer_time and max_allowed_gap and the final if statement has a desired range you can adjust. You can try to use the defaults I have set, they worked for me. BUT! Theres a chance this will not work out well for your dataset. The process I went through would be to adjust buffer_time then run srtsegmenter.py. Go listen to the segments in order, if they are overlapping, cut mid sentence, or have artifacts then go back and adjust buffer_time. Repeat until you get desired results.
3. Run the segmentation script (python makeDataset/tools/srtsegmenter.py)
4. Run the add_padding.py script to add a duration of silence to the end of each audio clip.

The above steps will generate a set of segmented audio files, a folder of bad audio it didn't like, and an output.txt file. I have it set to throw out segmemts under 1 second and over 11.6 seconds. You can adjust this to varying degrees.

## At this point you should use the curate.ipynb notebook within this repo. Make a copy of the output.txt file and format it following the outline in the notebook. 

### Phonemization

1. Run the script (python makeDataset/tools/phonemized.py --language en-us).
The --language argument refers to an [espeak-ng voice](https://github.com/espeak-ng/espeak-ng/), such as 'fr-fr' for French (default is en-us).
Check the espeak-ng identifier for your language [here](https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md).
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
5. If the language of your dataset is not English, you will need to modify the PLBER model of StyleTTS. If this is your case, refer to [this](https://huggingface.co/papercup-ai/multilingual-pl-bert) repository (don't forget to check if your language is supported).

## Run

Finally, you can start the fine-tuning process with the following command:

- accelerate launch --mixed_precision=fp16 --num_processes=1 train_finetune_accelerate.py --config_path ./Configs/config_ft.yml

## Changelog
- **7/25/2024**: Added a specific output format (srt), condition on previous text, max line width, max line count, and segment resolution to the whisperx command. (Note: max_line_width is supposed to keep it under 250 chars. It sometimes doesn't work. If anyone can figure that out let me know)
- **6/8/2024**: There's now a curate.ipynb notebook. Use it to analyze and prune your dataset. It will give you a few visuals and possible points of concern about your dataset. I highly highly suggest you use it. 
- **6/2/2024**: Added "with_stress" and "preserve_punctuation" to the phonemize script.
- **5/15/2024**: https://github.com/IIEleven11/SilenceRemover This repo is a fork of [@jerryliuoft](https://github.com/jerryliuoft)'s https://github.com/jerryliuoft/SilenceRemover. It's a visual representation for the location, removal, and or addition of silence within media. The original repo I forked is specific to video, so it outputs an mp4. I will modify this soon to allow for the option of either audio or video output as to more align with our use case. It removes a lot of the guesswork that i've been doing with the energy and decible detection. I had to share it right away because it immediately saved me a ton of time. Take a look at it and throw em a star. It's a lifesaver.
- **3/24/2024**: Phonemizer now capable of handling languages other than english. - Contributer: [@Scralius]
- **2/09/2024**: Implemented new buffer for subtitles. This help with the segmentation process. See the "srtsegmenter.py" for more details. Added "add_padding.py" to add a length of silence to both ends of every audio segment.
- **2/08/2024**: Added a script that adds a "silence buffer" within an audio file. This allows a larger margin of error during segmentation. Edited srtsegmenter.py, specifically the "end_time" variable now has to wait 600ms before it can make a cut. This combined with the silence buffer can help combat early segmentation. It was highly effective once I tuned the parameters correctly.
- **1/26/2024**: Updated Readme for clarity and specifying seperate windows and linux whisperx commands.
- **1/12/2024**: Added the ability to work with multiple SRT and Audio files at one time for large datasets or blended voices. - Contributor:  [@78Alpha]
- **12/6/23**: I noticed segmentation from the whisperx .json was unacceptable. I created a segmentation script that uses the .srt file that the whisperx command generates. From what I can tell this is significantly more accurate. This could be dataset specific. Use the json segmenter if needed.
- **12/5/23**: Fixed a missing "else" in the Segmentation script.
- **12/4/23**: A working config_ft.yml file is available in the tools folder.
- **12/2/23**: Rewrote Segmentation and Transcription scripts.

