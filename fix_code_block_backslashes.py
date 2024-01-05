#!/usr/bin/env python
"""Recursively processes Markdown files in a directory and removes backslashes
preceding opening or closing angle brackets inside code blocks."""
import argparse
import os

CODE_BLOCK_BACKTICK_COUNT: int = 3


def process_note(text: str) -> str:
    """Removes erroneous backslashes inside code blocks.

    Any backslashes preceding opening or closing angle brackets inside of a code
    block will be removed.

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
    consecutive_backticks = 0
    in_code_block = False
    char_idx = 0

    for c in text:
        if c == "`":
            consecutive_backticks += 1
        else:
            if consecutive_backticks == CODE_BLOCK_BACKTICK_COUNT:
                in_code_block = not in_code_block
            consecutive_backticks = 0

        if in_code_block:
            if c == "\\" and char_idx < len(text) - 1:
                # Only perform a backslash replacement when the next character
                # is an opening or closing angle bracket
                if text[char_idx + 1] == "<" or text[char_idx + 1] == ">":
                    char_idx += 1
                    continue

        modified_text += c
        char_idx += 1

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
