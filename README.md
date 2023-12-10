# StyleTTS2 Fine-Tuning Guide

This repository provides a guide on how to prepare a dataset and execute fine-tuning using the StyleTTS2 process. https://github.com/yl4579/StyleTTS2

- A gradio webui will be finished soon.

## Changelog

- **12/6/23**: I noticed segmentation from the whisperx .json was unacceptable. I created a segmentation script that uses the .srt file that the whisperx command generates. From what I can tell this is significantly more accurate.
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
    - pip install phonemizer pydub


### Data Preparation

1. Place a single 24khz .wav file in the /StyleGuide/makeDataset folder.
2. Run the whisperx command on the wav file:
    - whisperx /StyleGuide/makeDataset/wavfile.wav --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H
        - (Run this on the command line. If your GPU cant handle it there are other models you can use besides large-v2)
3. The above command will generate a set of transcriptions. Save the resulting files.


### Segmentation and Transcription

1. Navigate to the tools directory:
2. Open srtsegmenter.py and fill out all the file paths.
3. Run the segmentation script:

The above steps will generate a set of segmented audio files, a folder of bad audio it didn't like, and an output.txt file.

### Phonemization

1. Open phonemized.py and fill out the file paths.
2. Run the script.
3. This script will create the train_list.txt and val_list.txt files.

At this point, you should have everything you need to fine-tune.


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

  
