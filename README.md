# Brown Tail Moth Investigation - DavisAI

## A fully functional implementation of the Pix2Pix GAN used to conduct image-to-image translation between the RGB and NIR color-spaces

## Table of Contents
- [Project Goals](#project-goals)
- [Results](#results)
- [Getting Started](#getting-started)
- [Contents](#contents)
	- [Coordinate_Mapping](#coordinate_mapping)
  - [Pix2Pix](#pix2pix)
    - [GAN Creation Files](#GAN_creation_files)
    - [Image Storage Folders](#Image_Storage_Folders)
    - [combine_images.py](#combine_images)
- [Data](#data)
  - [SEN12MS](#sen12ms)
  - [Drone_Images](#drone_images)

## Project Goal <a name="project-goals"></a>
The goal of this project was to develop a computer vision pipeline to detect Brown Tail Moth infestations using drone footage by performing image processing, data analysis, training an AI model, and mapping the detected infestations. To do so, we attempt to conduct RGB to NIR image-to-image translation using a Pix2Pix GAN model with the goal of making BTM overwintering pods more visible to a object detection AI model.

## Results <a name="results"></a>
<img src="https://github.com/Tahiya31/DavisAI_BTM/raw/main/Pix2Pix/test_drone_images/Waterville%20Brown%20Tail%202022-69.jpg" alt="Image 2" width="256" height="256" style="object-fit: contain;" /> <img src="https://github.com/Tahiya31/DavisAI_BTM/raw/main/Pix2Pix/saved_images/generated_image_Waterville%20Brown%20Tail%202022-69.png" alt="Image 1" width="256" height="256" /> </div>

</div>

The above figures show the generator does not do a very good job at simulating the NIR channel using the drone captured images. Possible reasons that the model does not perform well are 1) the data it was trained is too dissimilar from the data it is being used for and 2) the model produces images in the RGB colorspace instead of in grayscale

## Getting Started <a name="getting-started"></a>
1. Download the Pix2Pix folder
2. Download the [SEN12MS](https://inkyusa.github.io/deepNIR_dataset/download/synth/) dataset
3. Put the SEN12MS dataset in the Pix2Pix folder and rename it 'dataset' (any dataset used must be in a folder called 'dataset')
4. Configur the dataset.py file to match the characteristics of the dataset in use (no change is needed if using SEN12MS)
6. Change the names of the files that the generator and discriminator models get saved to
   - i.e. in 'config.py' change 'CHECKPOINT_DISC = ' and 'CHECKPOINT_GEN = ' to names of your choice
8. Run 'pix2pix.ipynb' and wait!

## Contents <a name="contents"></a>

### Coordinate_Mapping <a name="coordinate_mapping"></a>
<div style="display: flex;">
    <img src="https://github.com/Tahiya31/DavisAI_BTM/blob/main/coordinate_mapping/results/manual-only-coords.png" alt="Mapping Manual" width="300" style="object-fit: contain;"/>
    <img src="https://github.com/Tahiya31/DavisAI_BTM/blob/main/coordinate_mapping/results/drone-only-coords.png" alt="Mapping Drone" width="212" style="object-fit: contain;"/>
</div>
<img src="https://github.com/Tahiya31/DavisAI_BTM/blob/main/coordinate_mapping/results/combined.png" alt="Mapping Both" style="object-fit: contain;"/>

Contains the python scripts in order to extract the metadata (latitude, longitude,  etc.) from the images in a Mac folder, and maps that coordinates of the manually captured data (black circles) vs. the coordinates of the drone captured data (colored circles; blue to red maps when the images were taken on December 22, 2022, early to late) using the Folium python package. As we can see, there is a surprising lack of overlap between the two datasets making them difficult to use in conjunction with one another.

### Pix2Pix <a name="pix2pix"></a>
This is the only folder needed in order to run train/validate/test the GAN. In this folder we have...

<ins>**GAN Creation Files**</ins> <a name="GAN_creation_files"></a>

<sub> *Must change one of 3 'dataset_xyz.py' files to 'dataset.py' depending on what dataset you want to work with (if using SEN12MS dataset, rename 'dataset_SEN12MS.py' --> 'dataset.py')* </sub>

<sub> *Change the output file name in 'config.py'; output files will build on top of previous training if name is not changed* </sub>

- config.py
- dataset_anime.py
- dataset_maps.py
- dataset_SEN12MS.py
- discriminator_model.py
- generator_model.py
- train.py
- utils.py

<ins>**Image Storage Folders**</ins> <a name="Image_Storage_Folders"></a>

- dataset
- evaluation
- results
- saved_images
- test_drone_images

### combine_images.py <a name="combine_images"></a>
A helper method that combines two images, one from training set folder and one from a validation set folder, into one image by placing them side by side. The purpose of this is to put images into the correct format for the Pix2Pix GAN. The images in the train and validation folders must have the same order for them to combined together.

## Data <a name="data"></a>
Contains the datasets used to train (SEN12MS) and test (Drone_Images) the GAN

### SEN12MS <a name="sen12ms"></a>
![https://github.com/Tahiya31/DavisAI_BTM/blob/main/coordinate_mapping/results/combined.png](https://github.com/Tahiya31/DavisAI_BTM/blob/main/Pix2Pix/SEN12MS_combined_examples/ROIs1158_spring_s000001_p000041.png)

Data that contains the RGB-NIR paired satellite images used to train the GAN. The [SEN12MS](https://inkyusa.github.io/deepNIR_dataset/download/synth/) dataset is an open source dataset of over 180,000 RGB-NIR paired images.
### Drone_Images <a name="drone_images"></a>
<img src="https://github.com/Tahiya31/DavisAI_BTM/blob/main/Pix2Pix/test_drone_images/Waterville%20Brown%20Tail%202022-54.jpg" alt="Drone Image" width="450" style="object-fit: contain;" />

Dataset that contains over 5000 aerial drone images of trees that either both infested with BTMs or healthy. The images were collected on December 22, 2022.
