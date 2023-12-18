# HelloFresh - Case Study

## Introduction
The following is a case study for HelloFresh. Below you will find the following:
- ['Usage'](#usage)
- ['Explanation'](#explanation)

## Usage

### Prerequisites

- Python 3.9
- Pandas 2.1.4
- Numpy 1.26.2

### Installation

Install the prerequisites using the following command:

```bash
pip install -r requirements.txt
```
After installing the prerequisites, you can run the following command to run the script:

```bash
python main.py
```

## Explanation

The following is an explanation of the code and the thought process behind it.

Every method is documented with a docstring, so you can read the documentation for more information.
The methods are the following:

- `get_chilies_dataset()` - This method is used to create the chilies recipes CSV file.
- `clean_json_file()` - This method is used to clean the JSON file (e.g., adding commas after every line) and create a new JSON file with the cleaned data. The name of the json file is `downloaded_file.json`.
- `get_minutes()` - This method is used to get the minutes from the `cookTime` and `prepTime` keys. Instead of having 'PT1H' as a value, we will have 60 minutes.
- `transform_time_to_minutes()` - This method is used to transform the time series to minutes series.
- `transform_time_to_difficulty()` - This method is used to transform the time series to difficulty series.

The `chilies.csv` file is the final result of the script. The script will also print a message to indicate that the file was created successfully.