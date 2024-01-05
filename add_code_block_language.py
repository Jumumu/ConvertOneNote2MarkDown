#!/usr/bin/env python
"""Recursively processes Markdown files in a directory and adds the programming
language to Markdown code blocks."""
import argparse
import os

from guesslang import Guess

guess = Guess()

CODE_BLOCK_BACKTICK_COUNT: int = 3


def process_note(text: str) -> str:
    """Appends the language to the start of a code block.

    If an existing language is already specified, it will skip the addition.

    Parameters
    ----------
    text : str
        The text to process.

    Returns
    -------
    str
        The modified text.
    """
    modified_text = ""
    code_block_text = ""
    code_block_start_idx = 0
    consecutive_backticks = 0
    in_code_block = False
    skip_addition = False

    text_idx = 0
    modified_text_idx = 0

    for c in text:
        if c == "`":
            consecutive_backticks += 1

            if consecutive_backticks == CODE_BLOCK_BACKTICK_COUNT and not in_code_block:
                i = 1
                while ((text_idx + i) < len(text) - 1) and text[text_idx + i] == " ":
                    i += 1

                # Only append the language to the code block if a language
                # hasn't already been specified
                if ((text_idx + i) < len(text) - 1) and text[text_idx + i] != "\n":
                    skip_addition = True
        else:
            if consecutive_backticks == CODE_BLOCK_BACKTICK_COUNT:
                in_code_block = not in_code_block

                if in_code_block:
                    code_block_start_idx = modified_text_idx
                else:
                    if not skip_addition:
                        # Remove the closing backticks
                        code_block_text = code_block_text[
                            : len(code_block_text) - CODE_BLOCK_BACKTICK_COUNT
                        ]

                        lang = guess.language_name(code_block_text).lower()
                        modified_text = (
                            modified_text[:code_block_start_idx]
                            + lang
                            + modified_text[code_block_start_idx:]
                        )
                        # Need to update the position since we are inserting new characters
                        modified_text_idx += len(lang)

                    skip_addition = False
                    code_block_text = ""

            consecutive_backticks = 0

        if in_code_block:
            code_block_text += c

        modified_text += c
        text_idx += 1
        modified_text_idx += 1

    return modified_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", help="Path to the directory containing Markdown files"
    )
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    text = file.read()

                modified_text = process_note(text)

                with open(
                    filepath, "w", encoding="utf-8", newline="\n", errors="ignore"
                ) as file:
                    file.write(modified_text)

                print(f"Processed: {filepath}")

    print("Done!")


if __name__ == "__main__":
    main()
