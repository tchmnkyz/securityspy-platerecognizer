# SecuritySpy Plate Recognizer

`securityspy-platerecognizer` is a Python script that uses the [Plate Recognizer API](https://www.platerecognizer.com/) to recognize license plates in [SecuritySpy][https://bensoftware.com/securityspy/] CCTV footage.

## Installation

To use `securityspy-platerecognizer`, you'll need to have Python 3 installed on your computer. You can download Python 3 from the [official Python website](https://www.python.org/downloads/).

You'll also need to install the `requests` library. You can do this by running the following command in your terminal:

```pip install requests```

## Usage

To use `securityspy-platerecognizer`, you'll need to edit the `platerecognizer.py` file to include your Plate Recognizer API key and the ID of the SecuritySpy camera you want to analyze.

You can then run the script by running the following command in your terminal:

```python3 platerecognizer.py```



The script will then analyze the specified SecuritySpy footage and recognize any license plates in the footage using the Plate Recognizer API.

## Contributing

If you'd like to contribute to `securityspy-platerecognizer`, feel free to submit a pull request!

## License

`securityspy-platerecognizer` is released under the MIT License.
