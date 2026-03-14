import logging
from pathlib import Path

import requests

logging.basicConfig(
    filename="dictionary.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "word_history.txt"


class DictionaryService:
    def __init__(self, word: str):
        self.word = word.lower().strip()
        self.api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"

    def get_meaning(self) -> str:
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                meanings = data[0]["meanings"]
                definitions = []
                all_synonyms = set()
                all_antonyms = set()

                for meaning in meanings:
                    part_of_speech = meaning["partOfSpeech"]
                    all_synonyms.update(meaning.get("synonyms", []))
                    all_antonyms.update(meaning.get("antonyms", []))

                    for definition in meaning["definitions"]:
                        definition_text = definition["definition"]
                        all_synonyms.update(definition.get("synonyms", []))
                        all_antonyms.update(definition.get("antonyms", []))
                        definitions.append(f"({part_of_speech}) {definition_text}")

                synonyms_text = ", ".join(all_synonyms) if all_synonyms else "No synonyms available"
                antonyms_text = ", ".join(all_antonyms) if all_antonyms else "No antonyms available"

                result = "\n".join(definitions)
                result += f"\n\nSynonyms: {synonyms_text}\nAntonyms: {antonyms_text}"
                self.save_to_file(self.word)
                return result
            return "Word not found in the dictionary."
        except Exception as error:
            logging.error(str(error))
            return "An error occurred while fetching the meaning."

    @staticmethod
    def save_to_file(word: str) -> None:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with HISTORY_FILE.open("a", encoding="utf-8") as file:
            file.write(f"{word}\n")


def get_history() -> list[str]:
    if not HISTORY_FILE.exists():
        return []
    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def clear_history() -> None:
    HISTORY_FILE.write_text("", encoding="utf-8")
