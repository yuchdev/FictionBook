import os
import sys
import argparse
import xml.etree.ElementTree as et

import xmljson
import xmltodict

__doc__ = """Use xmltodict library to convert XML to JSON and vice versa
https://github.com/martinblech/xmltodict
"""

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKING_DIR, "../..", "test", "assets")


def get_asset_path(file_name):
    return os.path.join(ASSETS_DIR, file_name)


class XmlJsonConverter:

    def __init__(self, file_path):
        switch_extension = {
            ".xml": ".json",
            ".json": ".xml"
        }
        base_name, ext = os.path.splitext(os.path.basename(file_path))
        self.file_path = file_path
        self.converted_path = os.path.join(os.path.dirname(file_path), f"{base_name}_converted.{switch_extension[ext]}")


class XmlJsonCobra(XmlJsonConverter):

    def __init__(self, file_path):
        super().__init__(file_path)

    def convert_xml(self) -> dict:
        """
        Convert an XML file to a dictionary using xmljson
        Read XML into xml.etree and serialize it to a dictionary
        Writes the dictionary to a JSON file
        Skip namespaces in XML
        :return: serialized dictionary
        """
        with open(self.file_path, 'r') as xml_f:
            xml_root = et.parse(xml_f).getroot()
            result = cb.data(xml_root)
        with open(self.converted_path, 'w') as json_f:
            json.dump(result, json_f, indent=4)
        return result

    def convert_json(self):
        """
        Read JSON file and deserialize it to an XML using xmljson
        Write pretty-print XML to a file
        :return:
        """
        with open(file_path, 'r') as f:
            json_content = f.read()
            result = cb.etree(json_content)
        with open(self.converted_path, 'w') as f:
            f.write(et.tostring(result, encoding='unicode'))


class XmlToDict(XmlJsonConverter):

    def __init__(self, file_path):
        super().__init__(file_path)

    def convert_xml_file(self) -> dict:
        """
        Convert an XML file to a dictionary using xmltodict library.
        :return: serialized dictionary
        """
        with open(self.file_path, 'r') as f:
            xml_content = f.read()
            result = xmltodict.parse(xml_content)
        with open(self.converted_path, 'w') as f:
            json.dump(result, f, indent=4)
        return result

    def convert_json_file(self):
        """
        Read JSON file, convert it to an XML using xmltodict library, write it to a pretty-print XML file, and return the XML string.
        :return: XML string
        """
        with open(self.file_path, 'r') as f:
            json_content = f.read()
            json_dict = json.loads(json_content)
            xml_str = xmltodict.unparse(json_dict, pretty=True)
        with open(self.converted_path, 'w') as f:
            f.write(xml_str)
        return xml_str


def main():
    """
    Main entry point
    CLI accept one parameter, if it's an XML file, it will be converted to a dictionary.
    If it's a JSON file, it will be converted to an XML.
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description="XML to JSON and vice versa")
    parser.add_argument("file_path",
                        help="Path to the XML or JSON file")
    parser.add_argument("--tool",
                        choices=["xmltodict", "xmljson"],
                        help="Choose the tool to use")
    args = parser.parse_args()

    tools = {
        "xmltodict": XmlToDict,
        "xmljson": XmlJsonCobra
    }

    # if file is not found in working directory, try to find it in assets directory
    if not os.path.isfile(args.file_path):
        file_path = get_asset_path(args.file_path)
    else:
        file_path = args.file_path

    if args.tool:
        tool = tools[args.tool](file_path)


    return 0


if __name__ == "__main__":
    sys.exit(main())
