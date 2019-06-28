# *Face Verification with Anti-Spoof*

Face identification merged with face anti-spoof detection trained on real and fake images dataset using CNN's.

## Features
* Face Identification
* Face Anti-Spoof
* Convolutional Neural Networks


## Installation

Simply clone the repository and extract the files on your working directory.

## Requirements
Download the face_ver.yml file and go to your command prompt and type the following:
  ```bash
  conda env create -f face_ver.yml
  ```
Verify that the new environment was installed correctly:
  ```bash
  conda list
  ```
Activate the environment typing:
  ```bash
  conda activate face_ver
  ```
**[NOTE]** Be sure to have Conda installed before using this!


## Usage
The usage differs if a user is registering for the first time or coming back for a login authentication. Below are the instructions for both cases.

### If you never used the algorithm
1. Generate your image data using the script *Image_Dataset_Generator.py*. Simply type:
   ```bash
   python image_dataset_generator.py
   ```
   And enter the name of the person who's registering<br>
   **[NOTE]** MAX_NUMBER_OF_IMAGES define the number of images that'll be generated (one is enough).      The image(s) will be saved in the    *images folder*.
2. Go to the bottom of the *fr_utils.py* file and uncomment the *update_or_create_known_people()* line (I'm still figuring out a faster and smarter way of doing this). Run the script from your command line by typing:
    ```bash
    python fr_utils.py
    ```
    **[NOTE]** Don't forget to *comment* it again after using. After that, the pickle files are updated, now containing the new image and new name.<br>
    **[NOTE]** Steps 1 and 2 should be done everytime a new person wants to register his/her face.
    
3. Now that the algorithm "knows you" you can finally try and see if your face is now authenticated. To do that, stay in front of your webcam, go to your command prompt and type:
    ```bash
    python fr_main.vX.py
    ```
    **[NOTE]** the X stands for the version number. E.g. for the 0-th version, it'd be: python fr_main.v0.py
  
### If you already used the algorithm
1.  Simply run the main file by repeating the step number 3 above.
 



