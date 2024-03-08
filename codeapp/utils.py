# built-in imports
# standard library imports
import csv

import requests

# internal imports
# from codeapp import db
from codeapp.models import IgnGames

# external imports
# from flask import current_app
# from sklearn.utils import Bunch


def get_data_list() -> list[IgnGames]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """
    ##### check if dataset already exists, and if so, return the existing dataset  #####
    # db.delete("dataset_list")  # uncomment if you want to force deletion
    # if db.exists("dataset_list") > 0:  # checks if the `dataset` key already exists
    # current_app.logger.info("Dataset already downloaded.")
    # dataset_stored: list[IGN_games] = []  # empty list to be returned
    # raw_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)  # get list from DB
    # for item in raw_dataset:
    # dataset_stored.append(pickle.loads(item))  # load item from DB
    # return dataset_stored
    # current_app.logger.info("Downloading dataset.")
    response = requests.get(
        "https://onu1.s2.chalmers.se/datasets/IGN_games.csv", timeout=10
    )

    with open("IGN_games.csv", "wt", encoding="utf-8") as file:
        file.write(response.text)

    dataset_base: list[IgnGames] = []  # list to store the items
    # for each item in the dataset...
    with open("IGN_games.csv", "rt", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            new_ign_games = IgnGames(
                title=row["title"],
                score=float(row["score"]),
                score_phrase=row["score_phrase"],
                platform=row["platform"],
                genre=row["genre"],
                release_year=int(row["release_year"]),
                release_month=int(row["release_month"]),
                release_day=int(row["release_day"]),
            )
            # create a new object
            # push object to the database list
            # db.rpush("dataset_list", pickle.dumps(new_ign_games))
            dataset_base.append(new_ign_games)  # append to the list
            print(new_ign_games)
    return dataset_base


def calculate_statistics(dataset: list[IgnGames]) -> dict[str, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    gamedict: dict[str, int] = {}

    for i in dataset:
        if i.platform in gamedict:
            gamedict[i.platform] += 1
        else:
            gamedict[i.platform] = 1

    sorting = sorted(gamedict.items(), key=lambda item: item[1], reverse=True)
    cutted = sorting[:20]
    cutdict: dict[str, int] = dict(cutted)
    print(cutdict)
    return cutdict


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
