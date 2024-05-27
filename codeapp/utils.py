# built-in imports
import csv
import pickle

# standard library imports
import requests

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import IgnGames

# from flask import current_app
# from sklearn.utils import Bunch


def get_data_list() -> list[IgnGames]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """
    # Database configuration
    if db.exists("dataset_list") > 0:
        current_app.logger.info("The dataset has already been downloaded!")
        dataset_stored: list[IgnGames] = []
        first_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)
        for item in first_dataset:
            dataset_stored.append(pickle.loads(item))
        return dataset_stored

    url = "https://onu1.s2.chalmers.se/datasets/IGN_games.csv"
    response = requests.get(url, timeout=10)
    return_dataset: list[IgnGames] = []
    csv_data = response.content.decode("utf-8")
    csv_reader = csv.DictReader(csv_data.splitlines())

    for row in csv_reader:
        new_ign_games: IgnGames = IgnGames(
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
        return_dataset.append(new_ign_games)
        db.rpush("dataset_list", pickle.dumps(new_ign_games))
    return return_dataset


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
