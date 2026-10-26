"""Motor pequeño y explicable para un chatbot basado en reglas."""

from __future__ import annotations

import json
import random
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nltk.tokenize import wordpunct_tokenize


DEFAULT_RULES = Path(__file__).parent / "data" / "intents.json"


def normalize(text: str) -> str:
    """Convierte texto a minúsculas y elimina acentos para comparar reglas."""
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


@dataclass(frozen=True)
class Match:
    intent: str
    score: int


class RuleBasedChatbot:
    """Clasifica mensajes por coincidencia de palabras y frases configurables."""

    def __init__(self, rules_path: str | Path = DEFAULT_RULES, seed: int | None = None):
        with Path(rules_path).open(encoding="utf-8") as rules_file:
            self.rules: dict[str, Any] = json.load(rules_file)
        self.random = random.Random(seed)

    @staticmethod
    def _score(message: str, patterns: list[str]) -> int:
        normalized = normalize(message)
        tokens = set(wordpunct_tokenize(normalized))
        score = 0
        for raw_pattern in patterns:
            pattern = normalize(raw_pattern)
            if " " in pattern:
                if pattern in normalized:
                    score += 3
            elif pattern in tokens:
                score += 1
        return score

    def classify(self, message: str) -> Match:
        best = Match(intent="fallback", score=0)
        for intent in self.rules["intents"]:
            score = self._score(message, intent["patterns"])
            if score > best.score:
                best = Match(intent=intent["tag"], score=score)
        return best

    def respond(self, message: str) -> str:
        match = self.classify(message)
        if match.score == 0:
            responses = self.rules["fallback"]
        else:
            intent = next(item for item in self.rules["intents"] if item["tag"] == match.intent)
            responses = intent["responses"]
        return self.random.choice(responses)


def main() -> None:
    chatbot = RuleBasedChatbot()
    print("Asistente: Hola. Escribe tu duda sobre el Avance 1 o 'salir'.")
    while True:
        try:
            message = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAsistente: Hasta luego.")
            break
        if normalize(message) in {"salir", "adios", "hasta luego"}:
            print("Asistente: Hasta luego. ¡Éxito con tu proyecto!")
            break
        if message:
            print(f"Asistente: {chatbot.respond(message)}")


if __name__ == "__main__":
    main()
