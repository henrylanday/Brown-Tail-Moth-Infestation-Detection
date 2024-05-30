'''combine_images.py
Combines two images, one from training set folder and one from a validation set folder, into one image by 
    placing them side by side. The purpose of this is to put images into the correct format for the Pix2Pix GAN.
    The images in the train and validation folders must have the same order for them to combined together.
Henry Landay
Independent Study: Brown Tail Moths
Spring 2024
'''

from PIL import Image
import os

# Define the path to the image directories
train_folder = 'val/rgb'
val_folder = 'val/mis'
output_folder = 'val_combined'

# Ensure the output directory exists
if not os.access(os.path.dirname(output_folder), os.W_OK):
    print("Error: Cannot write to output directory. Please check your permissions.")
else:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

# Iterate through each image in the train folder
for image_name in os.listdir(train_folder):
    train_image_path = os.path.join(train_folder, image_name)
    val_image_path = os.path.join(val_folder, image_name)
    
    if os.path.isfile(train_image_path) and os.path.isfile(val_image_path):
        try:
            # Load the images
            train_image = Image.open(train_image_path)
            val_image = Image.open(val_image_path)
            
            # Check if both images have the same size, resize if necessary
            if train_image.size != val_image.size:
                val_image = val_image.resize(train_image.size, Image.ANTIALIAS)
            
            # Create a new image by combining them side by side
            total_width = train_image.width + val_image.width
            max_height = max(train_image.height, val_image.height)
            combined_image = Image.new('RGB', (total_width, max_height))
            combined_image.paste(train_image, (0, 0))
            combined_image.paste(val_image, (train_image.width, 0))
            
            # Save the combined image to the output folder
            combined_image.save(os.path.join(output_folder, image_name))
        except Exception as e:
            print(f"Failed to process {image_name}: {e}")
    else:
        print(f"Missing images for {image_name}")

print("Image processing completed.")
