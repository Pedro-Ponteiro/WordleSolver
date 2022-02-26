from dataclasses import dataclass


@dataclass
class AnalyzedGuess:
    


class Wordle:
    def __init__(self) -> None:
        self.num_of_chars = 5
        self.num_of_tries = 6

    def choose_word(self) -> None:
        ...

    def compare_guess_to_answer(self, guess: str) -> AnalyzedGuess:
        ...
