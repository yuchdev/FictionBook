import json
import os
import unittest
from textwrap import dedent

from fictionbook.intermediary_xml_format import IntermediaryXmlFormat


def dump_to_json(expected_dict, interim_dict):
    """
    Debugging function to dump expected and interim dictionaries to JSON files
    """
    if os.path.isfile("expected_structure.json"):
        os.remove("expected_structure.json")
    if os.path.isfile("interim_structure.json"):
        os.remove("interim_structure.json")

    with open("expected_structure.json", "w") as f:
        json.dump(expected_dict, f, indent=4)

    with open("interim_structure.json", "w") as f:
        json.dump(interim_dict, f, indent=4)


class FictionbookInterimTest(unittest.TestCase):

    def test_simple1(self):
        """
        Test IntermediaryXmlFormat, simple XML with no attributes
        """
        tested_xml = "<root><child1>text1</child1><child2>text2</child2></root>"
        expected_xml = tested_xml
        expected_formatted_xml = dedent("""\
            <root>
                <child1>text1</child1>
                <child2>text2</child2>
            </root>
        """)



if __name__ == '__main__':
    unittest.main()
