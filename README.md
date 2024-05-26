# Code-Transcode

A tool for converting code from one programming language to another.

**NEW**: experimental multi-function support and various other improvement on the `multiple-functions` branch (see PRs).

## Usage

### 1. Install project dependencies

Set up a Python virtual environment, activate it and install the dependencies within it.

```
python3.12 -m venv /path/of/your/venv
source /path/of/your/venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Create input file

At present, only JavaScript and Python are supported. Your file must contain a single function called `main`.

You can skip this step by using the `output.py` that ships with this repo.

### 3. (Optional) create test cases

Create a file called `test_cases.dat` that contains a list of inputs for the function under test. Each line in the file must be a JSON-serialized array of input values.

For example, for a function that takes a single float argument, `test_cases.dat` might be:

```
[1]
[100]
[0.9999999999]
```

**Known issue:**: this file must end with a blank line/newline character.

# 4. Run the CLI

You'll need to make sure that values for the following environment variables are set:

**AI_API_KEY**: OpenAI API key.
**AI_MODEL**: OpenAI model, e.g. `gpt-4o`.
**AI_PROVIDER=**open_ai

```
python -m cli transcode <input_file> <input_language> <output_file> <output_language>
```

Using the included output.py:

```
python -m cli transcode output.py python output.js javascript
```

**Known issue:** the names of the input and output files must be `output.{js/py}`. TODO make this configurable.

The results of running the `test_cases.dat` will be in `input_results.dat` and `output_results.dat`. Any discrepencies will be in a file called `compare_results.dat`.
