
# WSL2 and Linux Usage 

If you're using Windows, good luck!

## Dataset Preparation

First, clone the repository and set up the environment:


git clone https://github.com/IIEleven11/makeDataset.git
cd makeDataset
conda create --name StyleDataset python==3.10
conda activate StyleDataset
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip3 install phonemizer
pip3 install https://github.com/m-bain/whisperX.git

### Wav File Segmentation/Transcription

The following is for wav file segmentation. It must be 24kHz and only one file. If you have already curated your dataset you can skip this. 
- Gather a single 24kHz wav file and put it in the folder at path `/home/eleven/StyleGuide/makeDataset/whisperoutput`

On the command line
- whisperx /home/eleven/StyleGuide/makeDataset/whisperoutput/wavfile.wav --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H 

- This will output several transcriptions. You want the json.

- Open the whispersegmenter.py file and fill out the file paths. Run it

- Open the phonemized.py file, fill out the file paths. Run it


## Training with StyleTTS2


Ok so if you made it this far you now have your train_list.txt and val_list.txt. Included in StyleTTS2 Repo is the OOD_list.txt, you can use it.

Ok so dataset is done. Time to train

==============================================================================================

Because of the volatility of the dependencies were working with I would suggest creating a new folder to work from, entirely seperate from your dataset prep.


## StyleTTS2

conda deactivate
conda create --name StyleTTS2 python==3.10
conda activate StyleTTS2
git clone https://github.com/yl4579/StyleTTS2.git

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -U
!That version of torch IS NOT the same as the one we used for the dataset. If you try to use the wrong version you will get an error. (WSL2)!

cd StyleTTS2
pip install -r requirements.txt

make a folder named LibriTTS in the models folder.
git-lfs clone https://huggingface.co/yl4579/StyleTTS2-LibriTTS
Move epochs_2nd_00020.pth and config.yml into the models/LibriTTS folder


- So now we need to get our data in here. In the /StyleTTS2/Data folder you'll find three files that mirror the same names we made with our data set maker process. 
- To make this as simple as possible, just swap them out. You can make a new folder, and put them in there and put your data in their place.

open the config_ft.yml
/StyleTTS2/Configs/config_ft.yml

You shouldnt have to touch these except maybe the root_path. Make sure your segmented wav files go into the wavs folder.
data_params:
  train_data: "Data/train_list.txt"
  val_data: "Data/val_list.txt"
  root_path: "/Data/wavs"
  OOD_data: "Data/OOD_texts.txt"

as for the rest of the parameters/settings within the config, it's hardware and dataset specific. Expect this to not run the first time and to go through and make adjustments. focus on batch_size and max_len if youre getting memory issues.

run 
python train_finetune.py --config_path ./Configs/config_ft.yml
