import os
import sys
import argparse

import xmltodict

__doc__ = """Use xmltodict library to convert XML to JSON and vice versa
https://github.com/martinblech/xmltodict
"""

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKING_DIR, "../..", "test", "assets")


def get_asset_path(file_name):
    return os.path.join(ASSETS_DIR, file_name)


def convert_xml_file(file_path) -> dict:
    """
    Convert an XML file to a dictionary using xmltodict library.
    :param file_path:
    :return: serialized dictionary
    """
    with open(file_path, 'r') as f:
        xml_content = f.read()
        return xmltodict.parse(xml_content)


def convert_json_file(file_path):
    """
    Read SON file and deserialize it to an XML using xmltodict library.
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        json_content = f.read()
        return xmltodict.unparse(json_content)


def main():
    """
    Main entry point
    CLI accept one parameter, if it's an XML file, it will be converted to a dictionary.
    If it's a JSON file, it will be converted to an XML.
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description="XML to JSON and vice versa")
    parser.add_argument("file_path", help="Path to the XML or JSON file")
    args = parser.parse_args()

    # if file is not found in working directory, try to find it in assets directory
    if not os.path.isfile(args.file_path):
        file_path = get_asset_path(args.file_path)
    else:
        file_path = args.file_path

    if file_path.endswith(".xml"):
        result = convert_xml_file(file_path)
        print(result)
    elif file_path.endswith(".json"):
        result = convert_json_file(file_path)
        print(result)
    else:
        raise ValueError("File must be either XML or JSON")

    return 0


if __name__ == "__main__":
    sys.exit(main())
