#!/usr/bin/env python
"""Unit tests to exercise removing erroneous backslashes from codeblocks."""
import unittest

from fix_code_block_backslashes import process_note


class TestProcessNote(unittest.TestCase):
    def test_single_code_block(self):
        input = """
        ```
        \\<html\\>
        \\<html/\\>
        ```
        """

        output = """
        ```
        <html>
        <html/>
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_multiple_code_blocks(self):
        input = """
        ```
        \\<html\\>
        \\<html/\\>
        ```
        ```
        \\<!DOCTYPE html\\>
        \\<html\\>
        \\<head\\>
        \\<style\\>
        p {
        border-style: solid;
        border-bottom-color: #ff0000;
        }
        \\</style\\>
        \\</head\\>
        \\<body\\>

        \\<p\\>This is some text in a paragraph.\\</p\\>

        \\</body\\>
        \\</html\\>
        ```
        """

        output = """
        ```
        <html>
        <html/>
        ```
        ```
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        p {
        border-style: solid;
        border-bottom-color: #ff0000;
        }
        </style>
        </head>
        <body>

        <p>This is some text in a paragraph.</p>

        </body>
        </html>
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_text_before_code_block(self):
        input = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        \\<html\\>
        \\<html/\\>
        ```
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        <html>
        <html/>
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_text_after_code_block(self):
        input = """
        ```
        \\<html\\>
        \\<html/\\>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        ```
        <html>
        <html/>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)

    def test_text_before_and_after_code_block(self):
        input = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        \\<html\\>
        \\<html/\\>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        <html>
        <html/>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)

    def test_text_between_code_blocks(self):
        input = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        \\<html\\>
        \\<html/\\>
        ```
        text outside of code block
        \\<escaped normal text\\>
        ```
        \\<!DOCTYPE html\\>
        \\<html\\>
        \\<head\\>
        \\<style\\>
        p {
        border-style: solid;
        border-bottom-color: #ff0000;
        }
        \\</style\\>
        \\</head\\>
        \\<body\\>

        \\<p\\>This is some text in a paragraph.\\</p\\>

        \\</body\\>
        \\</html\\>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        <html>
        <html/>
        ```
        text outside of code block
        \\<escaped normal text\\>
        ```
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        p {
        border-style: solid;
        border-bottom-color: #ff0000;
        }
        </style>
        </head>
        <body>

        <p>This is some text in a paragraph.</p>

        </body>
        </html>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_containing_backticks(self):
        input = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        this.items.forEach((item) =\\> {
            console.log(`${item}`)
        })
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        this.items.forEach((item) => {
            console.log(`${item}`)
        })
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_backslashes_without_angles(self):
        input = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        this.items.forEach((item) =\\> {
            console.log(`\\path\\to\\file: ${item}`)
        })
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        this.items.forEach((item) => {
            console.log(`\\path\\to\\file: ${item}`)
        })
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_with_double_backticks(self):
        input = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        this.items.forEach((item) =\\> {
            console.log(``\\path\\to\\file: ${item}``)
        })
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```
        this.items.forEach((item) => {
            console.log(``\\path\\to\\file: ${item}``)
        })
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)


if __name__ == "__main__":
    unittest.main()
