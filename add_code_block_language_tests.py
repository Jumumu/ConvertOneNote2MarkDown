#!/usr/bin/env python
"""Unit tests to exercise adding the language to code blocks."""
import unittest

from add_code_block_language import process_note


class TestProcessNote(unittest.TestCase):
    def test_single_code_block(self):
        input = """
        ```
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        output = """
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_multiple_code_blocks(self):
        input = """
        ```
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        ```
        <html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

        </body>
        </html>
        ```
        """

        output = """
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        ```html
        <html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

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
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_text_after_code_block(self):
        input = """
        ```
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
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
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
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
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        text outside of code block
        \\<escaped normal text\\>
        ```
        <html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

        </body>
        </html>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        output = """
        text outside of code block
        \\<escaped normal text\\>
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        text outside of code block
        \\<escaped normal text\\>
        ```html
        <html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

        </body>
        </html>
        ```
        text outside of code block
        \\<escaped normal text\\>
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_with_existing_language(self):
        input = """
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        ```html
        <html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

        </body>
        </html>
        ```
        """

        output = """
        ```rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        ```html
        <html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

        </body>
        </html>
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_with_trailing_space(self):
        input = """
        ``` 
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        output = """
        ```rust 
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_with_trailing_spaces(self):
        input = """
        ```   
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        output = """
        ```rust   
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_code_block_with_existing_language_and_spaces(self):
        input = """
        ```   rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        output = """
        ```   rust
        // This is the main function.
        fn main() {
            // Statements here are executed when the compiled binary is called.

            // Print text to the console.
            println!("Hello World!");
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_python_language(self):
        input = """
        ```
        def main():
            print("Hello, World!")
        ```
        """

        output = """
        ```python
        def main():
            print("Hello, World!")
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_typescript_language(self):
        input = """
        ```
        interface User {
            name: string;
            id: number;
        }
        ```
        """

        output = """
        ```typescript
        interface User {
            name: string;
            id: number;
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_go_language(self):
        input = """
        ```
        package main
        import "fmt"
        func main() {
            fmt.Println("hello world")
        }
        ```
        """

        output = """
        ```go
        package main
        import "fmt"
        func main() {
            fmt.Println("hello world")
        }
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_bash_language(self):
        input = """
        ```
        if [ 1 -eq 1 ]; then
            echo "Hello, World!"
        fi
        ```
        """

        output = """
        ```shell
        if [ 1 -eq 1 ]; then
            echo "Hello, World!"
        fi
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_css_language(self):
        input = """
        ```
        body {
        background-color: linen;
        }

        h1 {
        color: maroon;
        margin-left: 40px;
        } 
        ```
        """

        output = """
        ```css
        body {
        background-color: linen;
        }

        h1 {
        color: maroon;
        margin-left: 40px;
        } 
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_yaml_language(self):
        input = """
        ```
        services:
        web:
            build: .
            ports:
            - "8000:5000"
        redis:
            image: "redis:alpine"
        ```
        """

        output = """
        ```yaml
        services:
        web:
            build: .
            ports:
            - "8000:5000"
        redis:
            image: "redis:alpine"
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_json_language(self):
        input = """
        ```
        {"name":"John", "age":30, "car":null}
        ```
        """

        output = """
        ```json
        {"name":"John", "age":30, "car":null}
        ```
        """

        self.assertEqual(process_note(input), output)

    def test_assembly_language(self):
        input = """
        ```
        mov r0, pc
        mov r1, #2
        add r2, r1, r1
        ```
        """

        output = """
        ```assembly
        mov r0, pc
        mov r1, #2
        add r2, r1, r1
        ```
        """

        self.assertEqual(process_note(input), output)


if __name__ == "__main__":
    unittest.main()
