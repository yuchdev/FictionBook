import argparse
import os
import sys

__doc__ = """Use xmljson library to convert XML to JSON and vice versa
https://github.com/sanand0/xmljson
"""

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKING_DIR, "../..", "test", "assets")


def get_asset_path(file_name):
    return os.path.join(ASSETS_DIR, file_name)


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
