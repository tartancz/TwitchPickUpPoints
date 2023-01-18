from twitch import TwitchAPI
import json
from time import sleep


def main():
    # get settings from init json
    with open("init.json", "r") as f:
        conf = json.load(f)
    api = TwitchAPI(**conf)
    while True:
        if not api.isStreamerOnline():
            sleep(3600)
            continue
        for _ in range(12):
            api.getPoints()
            sleep(300)


if __name__ == "__main__":
    main()
