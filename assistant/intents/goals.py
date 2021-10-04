import os

from dotenv import load_dotenv
# from markdown import markdown

load_dotenv()


def getGoalsOfDay(date):
    if not isinstance(date, str) or len(date.split("-")[0]) != 4 or len(date.split("-")[1]) != 2 or len(
            date.split("-")[2]) != 2:
        print("invalid date format")

    with open(f"{os.environ.get('PATH_TO_VAULT')}/Daily Notes/{date}.md") as date_file:
        text = date_file.read()
    # html = markdown(text)

    afterGoals = False
    goalsString = ""
    for line in text.split("\n"):
        if line.__contains__("## Goals") or line.__contains__("## TO DO"):
            afterGoals = True
            continue
        if afterGoals:
            goalsString += f"{line}\n"

    print(goalsString)

    return goalsString
