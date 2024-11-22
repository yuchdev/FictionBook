import json
import os
import unittest
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


class JsonInterimTest(unittest.TestCase):

    def test_simple1(self):
        """
        Test IntermediaryXmlFormat with no attributes
        """
        interim = IntermediaryXmlFormat(tag_name='p', text='Paragraph Text')
        expected_dict = {
            "tag": "p",
            "attributes": {},
            "text": "Paragraph Text"
        }
        expected_xml = '<p>Paragraph Text</p>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_simple2(self):
        """
        Test IntermediaryXmlFormat with attributes but no children
        """
        interim = IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph Text')
        expected_dict = {
            "tag": "p",
            "attributes": {"id": "1"},
            "text": "Paragraph Text"
        }
        expected_xml = '<p id="1">Paragraph Text</p>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_children1(self):
        """
        Test IntermediaryXmlFormat with children but no text
        """
        interim = IntermediaryXmlFormat(tag_name='section', attributes={'id': '1'}, children=[
            IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph 1'),
            IntermediaryXmlFormat(tag_name='p', attributes={'id': '2'}, text='Paragraph 2')
        ])
        expected_dict = {
            "tag": "section",
            "attributes": {"id": "1"},
            "text": None,
            "children": [
                {
                    "tag": "p",
                    "attributes": {"id": "1"},
                    "text": "Paragraph 1"
                },
                {
                    "tag": "p",
                    "attributes": {"id": "2"},
                    "text": "Paragraph 2"
                }
            ]
        }
        expected_xml = '<section id="1"><p id="1">Paragraph 1</p><p id="2">Paragraph 2</p></section>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_children2(self):
        """
        Test IntermediaryXmlFormat with children and text
        """
        interim = IntermediaryXmlFormat(tag_name='section', attributes={'id': '1'}, text='Section Text', children=[
            IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph 1'),
            IntermediaryXmlFormat(tag_name='p', attributes={'id': '2'}, text='Paragraph 2'),
            IntermediaryXmlFormat(tag_name='p', attributes={'id': '3'}, text='Paragraph 3')
        ])
        expected_dict = {
            "tag": "section",
            "attributes": {"id": "1"},
            "text": "Section Text",
            "children": [
                {
                    "tag": "p",
                    "attributes": {"id": "1"},
                    "text": "Paragraph 1"
                },
                {
                    "tag": "p",
                    "attributes": {"id": "2"},
                    "text": "Paragraph 2"
                },
                {
                    "tag": "p",
                    "attributes": {"id": "3"},
                    "text": "Paragraph 3"
                }
            ]
        }
        expected_xml = ('<section id="1">Section Text'
                        '<p id="1">Paragraph 1</p>'
                        '<p id="2">Paragraph 2</p>'
                        '<p id="3">Paragraph 3</p>'
                        '</section>')
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_children3(self):
        """
        Test IntermediaryXmlFormat with adding children
        """
        interim = IntermediaryXmlFormat(tag_name='section', attributes={'id': '1'}, text='Section Text')
        interim.add_child(IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph 1'))
        interim.add_child(IntermediaryXmlFormat(tag_name='p', attributes={'id': '2'}, text='Paragraph 2'))
        interim.add_child(IntermediaryXmlFormat(tag_name='p', attributes={'id': '3'}, text='Paragraph 3'))
        expected_dict = {
            "tag": "section",
            "attributes": {"id": "1"},
            "text": "Section Text",
            "children": [
                {
                    "tag": "p",
                    "attributes": {"id": "1"},
                    "text": "Paragraph 1"
                },
                {
                    "tag": "p",
                    "attributes": {"id": "2"},
                    "text": "Paragraph 2"
                },
                {
                    "tag": "p",
                    "attributes": {"id": "3"},
                    "text": "Paragraph 3"
                }
            ]
        }
        expected_xml = ('<section id="1">Section Text'
                        '<p id="1">Paragraph 1</p>'
                        '<p id="2">Paragraph 2</p>'
                        '<p id="3">Paragraph 3</p>'
                        '</section>')
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_attributes1(self):
        """
        Test adding attributes
        """
        interim = IntermediaryXmlFormat(tag_name='section', attributes={'id': '1'}, text='Section Text')
        interim.add_attribute('class', 'section-class')
        interim.add_attribute('style', 'color: red')
        expected_dict = {
            "tag": "section",
            "attributes": {"id": "1", "class": "section-class", "style": "color: red"},
            "text": "Section Text"
        }
        expected_xml = '<section id="1" class="section-class" style="color: red">Section Text</section>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_text1(self):
        """
        Set setting text
        """
        interim = IntermediaryXmlFormat(tag_name='section', attributes={'id': '1'}, text='Section Text')
        interim.set_text('New Section Text')
        expected_dict = {
            "tag": "section",
            "attributes": {"id": "1"},
            "text": "New Section Text"
        }
        expected_xml = '<section id="1">New Section Text</section>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_from_xml1(self):
        """
        Test IntermediaryXmlFormat.from_xml with a simple XML
        Compare the result with the expected IntermediaryXmlFormat object using dict
        """
        test_xml = '<p>Paragraph Text</p>'
        expected_intermediary = IntermediaryXmlFormat(tag_name='p', text='Paragraph Text')
        interim_xml = IntermediaryXmlFormat.from_xml(test_xml)
        self.assertEqual(interim_xml.to_dict(), expected_intermediary.to_dict())

    def test_from_xml2(self):
        """
        Test IntermediaryXmlFormat.from_xml with a complex XML
        Compare the result with the expected IntermediaryXmlFormat object using dict
        """
        test_xml = ('<section id="1">Section Text'
                    '<p id="1">Paragraph 1</p>'
                    '<p id="2">Paragraph 2</p>'
                    '<p id="3">Paragraph 3</p>'
                    '</section>')

        expected_intermediary = IntermediaryXmlFormat(
            tag_name='section',
            attributes={'id': '1'},
            text='Section Text',
            children=[
                IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph 1'),
                IntermediaryXmlFormat(tag_name='p', attributes={'id': '2'}, text='Paragraph 2'),
                IntermediaryXmlFormat(tag_name='p', attributes={'id': '3'}, text='Paragraph 3')
            ]
        )

        interim_xml = IntermediaryXmlFormat.from_xml(test_xml)

        self.assertEqual(interim_xml.to_dict(), expected_intermediary.to_dict())

    def test_from_xml3(self):
        """
        Test IntermediaryXmlFormat.from_xml with a complex XML
        Compare the result with the IntermediaryXmlFormat.__eq__ method
        """
        test_xml = ('<section id="1">Section Text'
                    '<p id="1">Paragraph 1</p>'
                    '<p id="2">Paragraph 2</p>'
                    '<p id="3">Paragraph 3</p>'
                    '</section>')

        interim_xml = IntermediaryXmlFormat.from_xml(test_xml)

        expected_intermediary = IntermediaryXmlFormat(
            tag_name='section',
            attributes={'id': '1'},
            text='Section Text',
            children=[
                IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph 1'),
                IntermediaryXmlFormat(tag_name='p', attributes={'id': '2'}, text='Paragraph 2'),
                IntermediaryXmlFormat(tag_name='p', attributes={'id': '3'}, text='Paragraph 3')
            ]
        )

        self.assertEqual(interim_xml, expected_intermediary)
