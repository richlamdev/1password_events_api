import datetime
import requests
import os
import json
import time
import pandas as pd


def main():

    with open("item_usages.json", "r") as input_file:
        json_data = json.load(input_file)

    # print(json_data)

    df = pd.read_json("item_usages.json")
    df.to_csv("item_usages.csv")

    # print(df)


if __name__ == "__main__":
    main()
