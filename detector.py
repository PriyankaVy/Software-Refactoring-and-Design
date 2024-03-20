import tkinter as tk
import ast
import traceback
import io
import os
from difflib import SequenceMatcher
from tkinter import filedialog

METHOD_LENGTH_THRESHOLD = 15
PARAMETER_LIST_THRESHOLD = 3
JACCARD_SIMILARITY_THRESHOLD = 0.75

class FunctionInfo:
    def __init__(self, name, start_line):
        self.name = name
        self.start_line = start_line
        self.end_line = None

class CodeSmellDetector:

    def __init__(self, root):
        self.root = root
        self.root.title("Code Smell Detector and Refactoring Tool")

        #Title label
        self.title_label = tk.Label(root, text="Code Odor Detector", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=10)

        # Label to display code smell messages
        self.message_label = tk.Label(root, text="", font=("Arial", 12))
        self.message_label.pack()

        #Upload File Button
        self.upload_button = tk.Button(root, text="Upload File", command=self.file_upload)
        self.upload_button.pack(side=tk.TOP, padx=5)

        #Refactor code button (initially disabled)
        self.refactor_button = tk.Button(root, text="Refactor Code", state='disabled', command=self.refactor_duplicate_code)
        self.refactor_button.pack(side=tk.TOP, padx=10)

    def file_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                self.show_message(["You selected an empty file. Please select a non-empty .py file."])
            else:
                self.analyze_code_smells(file_path)
        else:
            self.show_message(["Invalid file type. Please select a .py file."])

    def show_message(self, message):
        # Update the message label with the given message
        message_text = "\n".join(message)
        self.message_label.config(text=message_text)

    def analyze_code_smells(self, file_path):
        print(f"Analyzing {file_path} for code smells.....")
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                parse_tree = ast.parse(code)

                code_smells = []
                long_methods = []
                long_parameter_list_methods = []
                code_fragments = self.extract_code_fragments(code)

                for node in ast.walk(parse_tree):
                    if isinstance(node, ast.FunctionDef):
                        #print(variables)
                        if self.detect_long_parameter_list_methods(node):
                            long_parameter_list_methods.append((node.name, len(node.args.args)))
                        if self.detect_long_methods(code, node):
                            long_methods.append(node.name)

                code_clone = self.detect_code_clone(code_fragments)

                if long_methods:
                    code_smells.append(f"The long method(s) in given file: {', '.join(long_methods)}.")

                if long_parameter_list_methods:
                    code_smells.append(f"The method(s) in given file contain long parameter lists: {', '.join(f'{name} ({count} parameters)' for name, count in long_parameter_list_methods)}.")

                if code_clone:
                    code_smells.append(f"The code clones are detected. Here are the snippets:")
                    code_smells.extend(f"Snippet 1: {snippet[0]}\nSnippet 2: {snippet[1]}\n" for snippet in code_clone)
                    # Enable refactor button
                    self.refactor_button.config(state='normal', command=lambda: self.refactor_duplicate_code(code, code_clone))
                    code_smells.append(f"The code clones are detected. Click 'Refactor Code' button to refactor.")

                if not long_methods and not long_parameter_list_methods and not code_clone:
                    code_smells.append(f"No Code Smells")

                self.show_message(code_smells)

        except Exception as e:
            traceback.print_exc()
            self.show_message(f"An error occurred while analyzing the code: {str(e)}")

    def detect_long_methods(self, code, node):
        start_line = node.lineno
        end_line = node.end_lineno
        code_lines = code.split('\n')[start_line - 1:end_line]
        non_empty_lines = [line for line in code_lines if line.strip()]
        return len(non_empty_lines) > METHOD_LENGTH_THRESHOLD

    def detect_long_parameter_list_methods(self, node):
        return len(node.args.args) > PARAMETER_LIST_THRESHOLD

    def extract_code_fragments(self, code):
        code_fragments = []

        try:
            # Parse the code into an abstract syntax tree (AST)
            parse_tree = ast.parse(code)

            # Traverse the AST to extract code fragments
            for node in ast.walk(parse_tree):
                if isinstance(node, ast.FunctionDef):
                    # Get the starting and ending line numbers of the function
                    start_line = node.lineno
                    end_line = node.end_lineno

                    # Extract the code snippet corresponding to the function
                    function_code = '\n'.join(code.splitlines()[start_line-1:end_line])

                    # Add the code snippet to the list of fragments
                    code_fragments.append(function_code)

        except Exception as e:
            traceback.print_exc()
            self.show_message(f"An error occurred while extracting code fragments: {str(e)}")

        return code_fragments

    def detect_code_clone(self, code_fragments):
        duplicates = set()
        for i, snippet1 in enumerate(code_fragments):
            for j, snippet2 in enumerate(code_fragments):
                if i != j and (snippet2, snippet1) not in duplicates:
                    similarity = self.calculate_similarity(snippet1, snippet2)
                    print(similarity)
                    if similarity > JACCARD_SIMILARITY_THRESHOLD:
                        print(similarity)
                        duplicates.add((snippet1, snippet2))
        return duplicates

    def calculate_similarity(self, snippet1, snippet2):
        matcher = SequenceMatcher(None, snippet1, snippet2)
        return matcher.ratio()

    #Refactors Type 1 and Type 2 code clones
    def refactor_duplicate_code(self, code, duplicates):
        try:
            refactored_code = code
            for i, (snippet1, snippet2) in enumerate(duplicates):
                tree1 = ast.parse(snippet1)
                tree2 = ast.parse(snippet2)

                # Get the name of the function defined in snippet1 and snippet2
                function_name1 = tree1.body[0].name
                function_name2 = tree2.body[0].name

                # Replace the original code snippets with the modified ones
                refactored_code = refactored_code.replace(snippet2, "")
                # Replace the original function call with another function call
                refactored_code = refactored_code.replace(f"{function_name2}", f"{function_name1}")

            self.show_refactored_code(refactored_code)

        except Exception as e:
            traceback.print_exc()
            self.show_message(f"An error occurred while refactoring code: {str(e)}")

    def show_refactored_code(self, refactored_code):
        # Update the message label with the refactored code
        self.message_label.config(text="Refactored Code:")
        text_widget = tk.Text(self.root, wrap="word", width=80, height=20)
        text_widget.insert(tk.END, refactored_code)
        text_widget.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeSmellDetector(root)
    root.mainloop()
