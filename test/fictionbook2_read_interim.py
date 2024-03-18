import unittest
from fictionbook.intermediary_format import IntermediaryXmlFormat


class Fictionbook2InterimTest(unittest.TestCase):

    def test_intermediary1(self):
        interim = IntermediaryXmlFormat(tag_name='p', text='Paragraph Text')
        expected_dict = {
            "tag": "p",
            "attributes": {},
            "text": "Paragraph Text"
        }
        expected_xml = '<p>Paragraph Text</p>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_intermediary2(self):
        interim = IntermediaryXmlFormat(tag_name='p', attributes={'id': '1'}, text='Paragraph Text')
        expected_dict = {
            "tag": "p",
            "attributes": {"id": "1"},
            "text": "Paragraph Text"
        }
        expected_xml = '<p id="1">Paragraph Text</p>'
        self.assertEqual(interim.to_dict(), expected_dict)
        self.assertEqual(interim.to_xml(), expected_xml)

    def test_intermediary_children1(self):
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

    def test_intermediary_children2(self):
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


if __name__ == '__main__':
    unittest.main()
