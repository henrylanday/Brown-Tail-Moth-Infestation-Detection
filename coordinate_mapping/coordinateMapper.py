'''coordinateMapper.py
Map coordinate points using folium Python library
Henry Landay
Brown Tail Moth Project
Spring 2024
'''

import folium
import csv
from datetime import datetime


def getColor(date_time, min_date, max_date):
    '''Calculate a color based on the date's position between min_date and max_date.'''
    # Convert date_time from string to datetime object
    date_format = '%Y:%m:%d %H:%M:%S'  # Adjusted to match your dataset
    current_date = datetime.strptime(date_time, date_format)
    
    # Normalize the current date's position within the date range to a value between 0 and 1
    total_days = (max_date - min_date).days
    position = (current_date - min_date).days / total_days if total_days > 0 else 0
    
    # Convert position to a color using a gradient (here we use a simple red gradient)
    r = 255  # Red value (constant)
    g = int(255 * (1 - position))  # Green value decreases with time
    b = int(255 * (1 - position))  # Blue value decreases with time
    return f'#{r:02x}{g:02x}{b:02x}'


def main(csv_file):
    '''
    This function will loop through all of the images in a csv data set and map their coordinates on a map using folium
    *** Parts of this function were created with the help of ChatGPT 4 ***
    '''

    data = []

    # Open the CSV file
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # print(data)
    # Check if the first row (which now represents the column headers) contains the necessary keys
    if not {'ImageID', 'Latitude', 'Longitude'}.issubset(data[0].keys()):
        raise ValueError(
            'CSV file must contain ImageID, Latitude, and Longitude columns')

    # Adjust date format as needed for parsing
    dates = [datetime.strptime(item['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S') for item in data]
    min_date, max_date = min(dates), max(dates)

    map_center = [float(data[0]['Latitude']), float(data[0]['Longitude'])]
    folium_map = folium.Map(location=map_center, zoom_start=15)

    for item in data:
        color = getColor(item['DateTimeOriginal'], min_date, max_date)
        folium.CircleMarker(
            location=[float(item['Latitude']), float(item['Longitude'])],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(f"{item['ImageID']}<br>Date: {item['DateTimeOriginal']}<br>Latitude: {item['Latitude']}<br>Longitude: {item['Longitude']}", max_width=450)
        ).add_to(folium_map)


    ''' Markers that are pop-ups
    for item in data:
        # print(item)
        # Format the popup message to include image name, latitude, and longitude
        popup_message = f"{item['ImageID']}<br>Latitude: {item['Latitude']}<br>Longitude: {item['Longitude']}"
        folium.Marker(
            location=[float(item['Latitude']), float(item['Longitude'])],
            # Use folium.Popup to allow HTML content
            popup=folium.Popup(popup_message, max_width=450),
            # Using FontAwesome's 'picture' icon
            icon=folium.Icon(icon='picture', prefix='fa')
        ).add_to(folium_map)
    '''
    folium_map.show_in_browser()
    # # Save the map as an HTML file
    # map_file = 'image_map.html'
    # folium_map.save(map_file)
    # print(f'Map saved as {map_file}')


main('summary_image_metadata.csv')
