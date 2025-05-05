Python syntax and data types for security scripts

### Basic Python syntax

- **Comments:** 
    - Single-line comments start with `#`.
    - Multi-line comments are enclosed in triple quotes (`'''` or `"""`).

- **Variables:** 
    - Variables are created by assigning a value to a name using the `=` operator.
    - Variable names must start with a letter or underscore and can contain letters, numbers, and underscores.
    - Example: `my_variable = 10`

- **Control structures:**
    - if-else statements:
    - ```python
        if condition:
            # code to execute if condition is true
        else:
            # code to execute if condition is false
        ```
    - for loops:
    - ```python
        for item in iterable:
            # code to execute for each item in the iterable
        ```
    - while loops:
    - ```python
        while condition:
            # code to execute while condition is true
        ```

### Data types

### Working with files

Working with files in Python involves reading from, writing to, and manipulating data stored in various formats, which is essential for tasks such as log analysis, data processing, and security automation. By mastering file handling techniques, we can manage and analyze the data that drives our security operations efficiently. Here is the syntax for reading and writing files:

- **Reading files:**
    - To read a file, we can use the `open()` function with the `'r'` mode (read mode). We can then read the contents of the file using methods like `read()`, `readline()`, or `readlines()`.
    - Example:
    ```python
     with open('log.txt', 'r') as file:
        logs = file.readlines()
        for line in logs:
            print(line.strip())
    ```
- **Writing files:**
    - To write to a file, we can use the `open()` function with the `'w'` mode (write mode) or `'a'` mode (append mode). We can then write data to the file using the `write()` or `writelines()` methods.
    - Example:
    ```python
    with open('output.txt', 'w') as file:
        file.write('This is a test.\n')
        file.write('Writing to a file.\n')
    ```