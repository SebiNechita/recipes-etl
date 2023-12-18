import pandas as pd
import re
import requests


def clean_json_file(response, filename: str):
    """
    This function cleans the json file downloaded from the url.
    :param response: The response from the GET request
    :param filename: The name of the file to be saved
    """
    # Write the response content to a file
    with open(filename, 'w') as file:
        file.write(response.text)

    # Replace the enter character with a comma plus an enter character
    with open(filename, 'r+') as file:
        text = file.read()
        text = text.replace('\n', ',\n')
        file.seek(0)
        file.write(text)
        file.truncate()

    # Eliminate the last character and add a '[' at the beginning of the file and a ']' at the end of the file
    with open(filename, 'r+') as file:
        text = file.read()
        text = text[:-2]
        file.seek(0)
        file.write('[' + text + ']')
        file.truncate()


def get_minutes(time: str) -> int:
    """
    This function returns the minutes of a time string.
    :param time: The time string
    :return: The minutes of the time string
    """
    if len(time) == 2:
        return -1
    else:
        time = str(time[2:])
        pattern = re.compile(r'(?:(\d+)H)?(?:(\d+)M)?')

        # Match the pattern in the time string
        match = pattern.match(time)

        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            total_minutes = hours * 60 + minutes
            return total_minutes
        else:
            return -1


def transform_time_to_minutes(time: pd.Series) -> pd.Series:
    """
    This function transforms a time series into a series of minutes.
    :param time: The time series which has to be transformed (e.g., PT1H30M into 90)
    :return: new_time: The new time series with the minutes expressed as integers
    """
    new_time = []
    for index, row in time.items():
        new_time.append(get_minutes(row))
    return pd.Series(new_time)


def transform_time_to_difficulty(time: pd.Series, indexes) -> pd.Series:
    """
    This function transforms a time series into a series of difficulty.
    :param time: The time series which has to be transformed (e.g., 90 into Hard), where time over 60 minutes is Hard,
    time between 30 (inclusive) and 60 minutes (inclusive) is Medium, time between 0 and 30 minutes (exclusive) is Easy,
    and time less than 0 is Unknown.
    :param indexes: The indexes of the chilies series
    :return: new_time: The new time series with the difficulty expressed as strings
    """
    new_time = []
    for index, row in time.items():
        if row > 60:
            new_time.append('Hard')
        elif row >= 30:
            new_time.append('Medium')
        elif row > 0:
            new_time.append('Easy')
        else:
            new_time.append('Unknown')
    return pd.Series(new_time, index=indexes)


def get_chilies_dataset(url_chilies: str, csv_filename: str):
    """
    This function extracts every recipe that has “Chilies” as one of the ingredients and saves it as a csv file. It also
    adds an extra field to each of the extracted recipes with the name difficulty based on their time duration.
    :param url_chilies: The url of the json file
    :param csv_filename: The name of the csv file
    """

    filename = 'downloaded_file.json'

    # Make a GET request to the URL
    response = requests.get(url_chilies)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert the cleaned file into a dataframe
        clean_json_file(response, filename)
        df = pd.read_json(filename)

        # Extracts every recipe that has “Chilies” as one of the ingredients
        df_chilies = df[df['ingredients'].str.contains("Chilies|Chiles|Chile|Chilie|Cili")].copy()

        # Add an extra field to each of the extracted recipes with the name difficulty.
        duration = transform_time_to_minutes(df_chilies['prepTime']) + transform_time_to_minutes(df_chilies['cookTime'])
        df_chilies['difficulty'] = pd.Series(transform_time_to_difficulty(duration, df_chilies.index))

        # Make the resulting dataframe saved as a csv file
        df_chilies.to_csv(csv_filename, index=False)

        print('The csv file has been created successfully.')


if __name__ == '__main__':
    url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
    csv = 'chilies.csv'
    get_chilies_dataset(url, csv)
