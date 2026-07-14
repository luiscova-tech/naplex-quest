import json
from pathlib import Path
from dataclasses import asdict

from game.player import Player


SAVE_FILE = Path("saves/player.json")


def save_player(player: Player) -> None:
    SAVE_FILE.parent.mkdir(exist_ok=True)

    with open(SAVE_FILE, "w") as f:
        json.dump(asdict(player), f, indent=4)


def load_player() -> Player:
    if not SAVE_FILE.exists():
        return Player()

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    return Player(**data)