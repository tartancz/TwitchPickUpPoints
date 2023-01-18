from twitch import TwitchAPI
import json
from time import sleep


def main():
    # get settings from init json
    with open("init.json", "r") as f:
        conf = json.load(f)
    api = TwitchAPI(**conf)
    while True:
        if not api.is_streamer_online():
            sleep(3600)
            continue
        for _ in range(12):
            api.get_points()
            sleep(300)


if __name__ == "__main__":
    main()
