'''ImageMetaDataExtractor.py
Extract the meta data from a set images using Python Pillow library
Henry Landay
Brown Tail Moth Project
Spring 2024
'''

from PIL import Image, ExifTags
import os
import csv


def ImageMetaDataExtractor(image_name):
    '''
    This function takes in the name of an image and outputs a dictionary of the resulting meta-data associated with that image
    Source: https://stackoverflow.com/questions/21697645/how-to-extract-metadata-from-an-image-using-python

    Parameters
    -----------
    image_name: String representing the name of the image in the Images folder

    Returns
    ----------- 
    exif: a Python dictionary of all of the meta data associated with the image
    '''
    img = Image.open(f'Images/{image_name}')
    exif = {ExifTags.TAGS[k]: v for k,
            v in img._getexif().items() if k in ExifTags.TAGS}
    return exif


def GetMetaDataFromFolder():
    '''
    This function utilizes the above ImageMetaDataExtractor function to create a dictionary of dictionaries of 
        all of the photos in the Images folder as keys mapped to their meta-data

    Parameters
    -----------
    None - we already know the folder name we want to use

    Returns
    -----------
    result: a dictionary of dictionaries such that each image name is a key mapped to a dictionary of its metadata
    '''
    file_names = os.listdir('Images')
    result = {}
    for image in file_names:
        metaData = ImageMetaDataExtractor(image)
        result[image] = metaData
    return result


def dms_to_decimal(dms, direction):
    '''Convert from DMS (Degrees, Minutes, Seconds) format to decimal format.'''
    decimal = float(dms[0] + dms[1]/60 + dms[2]/3600)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal


def convertMetaDataToCSV(metaData):
    '''
    This function converts a dictionary of dictionaries of the meta data of images into a csv file
    *** Created with the help of ChatGPT 4 ***

    Parameters
    -----------
    metaData: a dictionary of dictionary where each image is a key mapped to a dictionary of its metadata

    Returns
    -----------
    None: nothing to return but it creates a csv file with the meta data
    '''
    with open('full_image_metadata.csv', 'w', newline='') as full_file, \
            open('summary_image_metadata.csv', 'w', newline='') as summary_file:

        # Prepare headers for the full metadata file (excluding GPSInfo, adding Latitude/Longitude after ImageID)
        first_image_metadata = next(iter(metaData.values()))
        full_headers = ['ImageID', 'Latitude', 'Longitude'] + \
            [key for key in first_image_metadata if key != 'GPSInfo']
        summary_headers = ['ImageID', 'Latitude',
                           'Longitude', 'DateTimeOriginal', 'ExposureTime']

        full_writer = csv.writer(full_file)
        summary_writer = csv.writer(summary_file)

        full_writer.writerow(full_headers)
        summary_writer.writerow(summary_headers)

        for image_id, metaData in metaData.items():
            # Convert GPSInfo to latitude and longitude if available
            if 'GPSInfo' in metaData:
                gps_info = metaData['GPSInfo']
                latitude = dms_to_decimal(gps_info[2], gps_info[1])
                longitude = dms_to_decimal(gps_info[4], gps_info[3])
            else:
                latitude, longitude = 'N/A', 'N/A'

            # Prepare the full metadata row, placing Latitude and Longitude right after ImageID
            full_row = [image_id, latitude, longitude] + [metaData.get(
                key, 'N/A') for key in first_image_metadata if key != 'GPSInfo']

            # Prepare the summary row
            summary_row = [
                image_id,
                latitude,
                longitude,
                metaData.get('DateTimeOriginal', 'N/A'),
                metaData.get('ExposureTime', 'N/A')
            ]

            full_writer.writerow(full_row)
            summary_writer.writerow(summary_row)

if __name__ == "__main__":
    convertMetaDataToCSV(GetMetaDataFromFolder())

