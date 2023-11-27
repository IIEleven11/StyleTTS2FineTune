
# WSL2 and Linux Usage 

If you're using Windows, good luck!

## Dataset Preparation

First, clone the repository and set up the environment:


git clone https://github.com/IIEleven11/makeDataset.git
cd makeDataset
conda create --name StyleDataset python==3.10
conda activate StyleDataset
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip3 install auditok phonemizer


### Wav File Segmentation

The following is for wav file segmentation. It must be 24kHz and only one file. If you have already curated your dataset you can skip this. I have also tried a bunch of different segmentation techniques. For me and my dataset this worked the best. I'm not sure why but it was extremely accurate.

- Gather a single 24kHz wav file and put it in the folder at path `StyleGuide/makeDataset/vits_scripts/wav_file_here`
- Open the `segmenter.py` script fill in your path to the wav file and the path to the segmentedAudio folder.
- `cd` into `StyleGuide/makeDataset/vits_scripts/vits`
- Run `python3 segmenter.py`

You should now have a full segmentedAudio folder.

### Transcription

Open up the `transcriber.py`

- This script I borrowed from Kreevoz's/vits suggestion in his fine tuning tips. I altered it to do a few things though. Its going to use vits to clean the text then it will use a phonemizer and output your `train_data.txt` in the correct format.  
`audio1.wav|phonemized transcription|1`. 
- It will also print the plain english data to the `alldata.txt` file for reference. Any audio it doesn't like it will move that wav file to the `badAudio` directory and omit its transcription from the `train_list.txt`. 
- Finally it will take 10% of the data and write it to a `val_data.txt`. (I am unclear on this part as well. The StyleTTS2 script/s may be capable or attempt to make the val_list for you)

Scroll to the bottom of `transcriber.py` and make sure you input the correct paths as they're labeled.

- Run python3 transcriber.py



## Training with StyleTTS2


Ok so if you made it this far you now have your train_list.txt and val_list.txt. All we need now is the OOD_list.txt. I am unclear on what exactly this is. I used the original included OOD_list.txt with one dataset. And I am training with a same speaker OOD_list.txt as I write this. One of these I am sure is wrong. Maybe someone else can share some knowledge on this. If there is a val_list what is the point of an OOD_list? Is that redundant? So until further guidance, you can get a new dataset and transcribe and segment it and just label the txt OOD_list.txt. 

Ok so dataset is done. Time to train

==============================================================================================

Because of the volatility of the dependencies were working with I would suggest creating a new folder to work from, entirely seperate from your dataset prep.


## StyleTTS2

conda deactivate
conda create --name StyleTTS2 python==3.10
conda activate StyleTTS2
git clone https://github.com/yl4579/StyleTTS2.git

Just a reminder if you made a new folder and have vscode make sure its in the same environment as your terminal before you go any further
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
