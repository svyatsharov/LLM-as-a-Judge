import csv
import json
from pathlib import Path

from dialogue_features import collect_dialogue_features
from mask_personal_data import mask_personal_data

DATA_DIR = Path(__file__).resolve().parent / "data"
DIALOGUES_PATH = DATA_DIR / "dialogues.csv"
FEATURES_PATH = DATA_DIR / "dialogues_features.csv"
FEATURE_FIELDS = ("chat_id", "message_count", "has_stub", "has_profanity")


def load_dialogues(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [
            {
                "chat_id": row["chat_id"],
                "datetime": row["datetime"],
                "history": json.loads(row["history"]),
            }
            for row in reader
        ]


def save_dialogue_features(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FEATURE_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    dialogues = load_dialogues(DIALOGUES_PATH)
    rows = []
    for dialogue in dialogues:
        masked_dialogue = mask_personal_data(dialogue)
        features = collect_dialogue_features(masked_dialogue)
        rows.append({"chat_id": masked_dialogue["chat_id"], **features})
    save_dialogue_features(FEATURES_PATH, rows)


if __name__ == "__main__":
    main()
