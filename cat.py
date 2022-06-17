import json
import urllib.parse
import urllib.request
import csv


def retrieve_api_json():
    """Connects to thecatapi.com API and returns a dictionary with the json data."""

    header = {"x-api-key": 'api_key=fcc1cd12-af2f-43ba-8773-894964526afa'}
    url = "https://api.thecatapi.com/v1/images/search"

    # allows header with key to be included as per thecatapi.com docs
    request = urllib.request.Request(url, headers=header)

    response = urllib.request.urlopen(request)
    data = response.read()
    json_dict = json.loads(data)

    return json_dict


def get_image_url(json_dict):
    """Dictionary with json data is passed in and the image url is returned."""

    image = json_dict[0]
    return image['url']


def store_new_image_url(csv_file_name):
    """File name of a CSV storing one of the image urls is passed in and a new url is generated and stored with any
    old url overwritten. A check is also made to ensure that both images are not the same and a new image is generated
    if they are."""

    with open(csv_file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([get_image_url(retrieve_api_json())])

    if read_csv_data('data storage/challenger.csv') == read_csv_data('data storage/cutest_cat.csv'):

        store_new_image_url(csv_file_name)


def read_csv_data(csv_file_name):
    """File name of CSV is passed in and the contents are returned as a string."""

    with open(csv_file_name, 'r') as file:
        data = csv.reader(file)
        row = list(data)
        return row[0][0]


def transfer_challenger_to_cutest():
    """Moves the url stored in the challenger csv to the cutest_cat csv. This is used when user clicks challenger cat
    button to indicate they think this cat is cuter."""

    challenger_url = read_csv_data('data storage/challenger.csv')

    with open('data storage/cutest_cat.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([challenger_url])


def increase_win_counter():
    """Retrieves the current win count from the csv, increase the value by 1 and overwrites the old value with this
    new one."""
    win_counter_str = read_csv_data('data storage/win_count.csv')
    win_counter_int = int(win_counter_str)
    win_counter_int += 1

    with open('data storage/win_count.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([win_counter_int])


def set_win_counter(value):
    """Sets the value of the win counter in the csv to the value passed in"""
    with open('data storage/win_count.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([value])


def initialise_images_and_win_counter():
    """Generates new images for both the cutest cat and challenger cat and also sets win count to 0."""
    store_new_image_url('data storage/cutest_cat.csv')
    store_new_image_url('data storage/challenger.csv')

    set_win_counter(0) # set to 0 for new game