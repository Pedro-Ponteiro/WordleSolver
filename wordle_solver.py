import pickle
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd


@dataclass
class WordRestriction:
    excluded_letters: List[str]

    # letters_occurence:
    # List of tuples containing:
    # letter [str]
    # number_of_occurrences [int] (min 1)
    # exact_num_of_occurrences [bool]
    letters_occurrence: List[Tuple[str, int, bool]]

    # letter_position_restriction:
    # List of tuples containing:
    # letter [str]
    # letter_position [int] (1 indexed)
    letter_position_restriction: List[Tuple[str, int]]


def get_word_positional_regex(letter: str, position: int) -> str:
    word_right_size = 5 - position
    word_left_size = 4 - word_right_size

    word_left_regex = "^" if not word_left_size else "^.{" + str(word_left_size) + "}"
    word_right_regex = (
        "$" if not word_right_size else ".{" + str(word_right_size) + "}$"
    )

    word_search_regex = word_left_regex + letter + word_right_regex

    return word_search_regex


def exclude_words(words_df: pd.DataFrame, excluded_words: List[str]) -> pd.DataFrame:
    words_cp = words_df
    words_cp.drop(
        words_cp.loc[words_cp["words"].isin(excluded_words)].index, inplace=True
    )

    return words_cp


def exclude_letters(
    words_df: pd.DataFrame, excluded_letters: List[str]
) -> pd.DataFrame:
    words_cp = words_df.copy()

    excluded_letters_regex = "|".join(excluded_letters)
    words_cp = words_cp.loc[~words_cp["words"].str.contains(excluded_letters_regex)]

    return words_cp


def get_words_by_letters_occurrence(
    words_df: pd.DataFrame, letters_occurrence: List[Tuple[str, int, bool]]
) -> pd.DataFrame:
    words_cp = words_df.copy()

    for letter, num_of_occurrences, exact_count in letters_occurrence:
        words_cp = words_cp.loc[
            words_cp["words"].apply(
                lambda x: x.count(letter) == num_of_occurrences
                if exact_count
                else x.count(letter) >= num_of_occurrences
            )
        ]

    return words_cp


def exclude_by_letter_pos(
    words_df: pd.DataFrame, letter_position_restriction: List[Tuple[str, int]]
) -> pd.DataFrame:
    words_cp = words_df.copy()

    for letter, position in letter_position_restriction:

        word_search_regex = get_word_positional_regex(letter, position)

        words_cp = words_cp.loc[
            words_cp["words"].str.contains(word_search_regex)
        ].copy()

    return words_cp


def get_possible_words(
    words_df: pd.DataFrame,
    word_restrictions: WordRestriction,
) -> str:

    words_cp = words_df.copy()

    words_cp = exclude_letters(words_cp, word_restrictions.excluded_letters)

    words_cp = get_words_by_letters_occurrence(
        words_cp, word_restrictions.letters_occurrence
    )

    words_cp = exclude_by_letter_pos(
        words_cp, word_restrictions.letter_position_restriction
    )

    return words_cp


def main() -> None:

    with open("df_words_5chars.pickle", "rb") as f:
        df = pickle.load(f)

    wr = WordRestriction(
        excluded_letters=[],
        letters_occurrence=[],
        letter_position_restriction=[],
    )

    possible_words = get_possible_words(df, wr)

    print(possible_words)


if __name__ == "__main__":
    main()
