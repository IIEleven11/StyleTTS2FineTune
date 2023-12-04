This repo serves the purpose of preparing a dataset and then the execution of Fine tuning using the StyleTTS2 process.

# 12-2-23 Rewrote Segmentation and Transcription

This works on WSL2 and Linux. Windows requires a bunch of other stuff, probably not worth it.

## Install conda/activate environment with python 3.10

- conda create --name dataset python==3.10
- conda activate dataset

## Install this version of Pytorch
- pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -U

## Install whisperx/phonemize and segmentation packages
- pip install https://github.com/m-bain/whisperX.git
- pip install phonemizer pydub


# You need a single 24khz .wav file. Put this file in the /StyleGuide/makeDataset folder.

- whisperx /StyleGuide/makeDataset/wavfile.wav --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H
    - (Run this on the command line. If your GPU cant handle it there are other models you can use besides large-v2)

  This will give you a set of transcriptions. We want the .json.

# Segmentation and transcription

- cd into the tools directory StyleGuide/makeDataset/tools
- Open whispersegmenter.py and fill out all the file paths
- run whispersegmenter.py

This will give you a path full of segmented audio files, a folder of bad audio it didnt like, and an output.txt

# Phonemization

- I split these processess up so you can check the output.txt as it is in english. Make sure segmentation went alright and punctuation was handled.
- open phonemized.py
- Fill out the file paths.

  This script will create the train_data.txt and val_list.txt. You should now have everything you need to fine tune.

# Fine Tuning with StyleTTS2

- git clone https://github.com/yl4579/StyleTTS2.git
- cd StyleTTS2
- pip install -r requirements.txt
- sudo apt-get install espeak-ng

- in the StyleTTS2 data folder youll see a wavs folder, delete the contents and put in your segmented wav files.
- delete the val_list and train_list files in the Data folder and replace with yours. Keep the OOD_list.txt file you'll use it.
- In the Configs folder you'll see a config_ft.yml open it. Edit any parameters you need. Paying attention to batch and max_len. These two are going to control how much ram is used. Its a heavy process. Drop batch size to favor max_len if you can. Supposedly a max_len of 800 proveds great results but requires a lot of ram.
- you will need to download this model clone https://huggingface.co/yl4579/StyleTTS2-LibriTTS
    - Create a folder named Models at /StyleTTS2/Models
    - Create a folder named Models at /StyleTTS2/Models/LibriTTS     
    - put epochs_2nd_00020.pth and its config.yml in here /StyleTTS2/Models/LibriTTS/epochs_2nd_00020.pth & /StyleTTS2/Models/LibriTTS/config.yml

# Run
accelerate launch --mixed_precision=fp16 --num_processes=1 train_finetune_accelerate.py --config_path ./Configs/config_ft.yml

  
