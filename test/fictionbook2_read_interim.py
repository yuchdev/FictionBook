import json
import os
import unittest
from fictionbook.intermediary_format import IntermediaryXmlFormat


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


class Fictionbook2InterimTest(unittest.TestCase):

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

    def test_from_dict1(self):
        """
        Test IntermediaryXmlFormat.from_dict with a complex dictionary
        Compare the result with the expected IntermediaryXmlFormat object
        """
        test_dict = {
            "description": {
                "title-info": {
                    "genre": "prose_contemporary",
                    "author": {
                        "first-name": "Victor",
                        "last-name": "Pelevin",
                        "home-page": "https://example.com"
                    },
                    "book-title": "Sol Invictus Book 1",
                    "annotation": "Sol Invictus Book 1",
                    "keywords": "book, keywords",
                    "date": "2020",
                    "lang": "en"
                },
                "document-info": {
                    "author": "Victor Pelevin",
                    "program-used": "Python fictionbook2 library",
                    "date": "2024",
                    "src-url": "https://example.com",
                    "id": "123456789",
                    "version": "1.0"
                },
                "publish-info": {
                    "book-name": "Book Name",
                    "publisher": "Publisher",
                    "city": "City",
                    "year": "2024",
                    "isbn": "1234567890"
                }
            }
        }

        # Create expected IntermediaryXmlFormat object with all the expected children
        expected_intermediary = IntermediaryXmlFormat(
            tag_name='description',
            children=[
                IntermediaryXmlFormat(
                    tag_name='title-info',
                    children=[
                        IntermediaryXmlFormat(tag_name='genre', text='prose_contemporary'),
                        IntermediaryXmlFormat(
                            tag_name='author',
                            children=[
                                IntermediaryXmlFormat(tag_name='first-name', text='Victor'),
                                IntermediaryXmlFormat(tag_name='last-name', text='Pelevin'),
                                IntermediaryXmlFormat(tag_name='home-page', text='https://example.com')
                            ]
                        ),
                        IntermediaryXmlFormat(tag_name='book-title', text='Sol Invictus Book 1'),
                        IntermediaryXmlFormat(tag_name='annotation', text='Sol Invictus Book 1'),
                        IntermediaryXmlFormat(tag_name='keywords', text='book, keywords'),
                        IntermediaryXmlFormat(tag_name='date', text='2020'),
                        IntermediaryXmlFormat(tag_name='lang', text='en')
                    ]
                ),
                IntermediaryXmlFormat(
                    tag_name='document-info',
                    children=[
                        IntermediaryXmlFormat(tag_name='author', text='Victor Pelevin'),
                        IntermediaryXmlFormat(tag_name='program-used', text='Python fictionbook2 library'),
                        IntermediaryXmlFormat(tag_name='date', text='2024'),
                        IntermediaryXmlFormat(tag_name='src-url', text='https://example.com'),
                        IntermediaryXmlFormat(tag_name='id', text='123456789'),
                        IntermediaryXmlFormat(tag_name='version', text='1.0')
                    ]
                ),
                IntermediaryXmlFormat(
                    tag_name='publish-info',
                    children=[
                        IntermediaryXmlFormat(tag_name='book-name', text='Book Name'),
                        IntermediaryXmlFormat(tag_name='publisher', text='Publisher'),
                        IntermediaryXmlFormat(tag_name='city', text='City'),
                        IntermediaryXmlFormat(tag_name='year', text='2024'),
                        IntermediaryXmlFormat(tag_name='isbn', text='1234567890')
                    ]
                )
            ]
        )

        # Convert test_dict to IntermediaryXmlFormat
        interim_xml = IntermediaryXmlFormat.from_dict(test_dict)

        # Compare structures
        self.assertEqual(interim_xml.to_dict(), expected_intermediary.to_dict())

    def test_from_dict2(self):
        """
        Test IntermediaryXmlFormat.from_dict with a complex dictionary
        Compare the result with the expected dictionary
        """
        test_dict = {
            "description": {
                "title-info": {
                    "genre": "prose_contemporary",
                    "author": {
                        "first-name": "Victor",
                        "last-name": "Pelevin",
                        "home-page": "https://example.com"
                    },
                    "book-title": "Sol Invictus Book 1",
                    "annotation": "Sol Invictus Book 1",
                    "keywords": "book, keywords",
                    "date": "2020",
                    "lang": "en"
                },
                "document-info": {
                    "author": "Victor Pelevin",
                    "program-used": "Python fictionbook2 library",
                    "date": "2024",
                    "src-url": "https://example.com",
                    "id": "123456789",
                    "version": "1.0"
                },
                "publish-info": {
                    "book-name": "Book Name",
                    "publisher": "Publisher",
                    "city": "City",
                    "year": "2024",
                    "isbn": "1234567890"
                }
            }
        }
        expected_structure = {
            "tag": "description",
            "attributes": {},
            "text": None,
            "children": [
                {
                    "tag": "title-info",
                    "attributes": {},
                    "text": None,
                    "children": [
                        {"tag": "genre", "attributes": {}, "text": "prose_contemporary"},
                        {
                            "tag": "author",
                            "attributes": {},
                            "text": None,
                            "children": [
                                {"tag": "first-name", "attributes": {}, "text": "Victor"},
                                {"tag": "last-name", "attributes": {}, "text": "Pelevin"},
                                {"tag": "home-page", "attributes": {}, "text": "https://example.com"}
                            ]
                        },
                        {"tag": "book-title", "attributes": {}, "text": "Sol Invictus Book 1"},
                        {"tag": "annotation", "attributes": {}, "text": "Sol Invictus Book 1"},
                        {"tag": "keywords", "attributes": {}, "text": "book, keywords"},
                        {"tag": "date", "attributes": {}, "text": "2020"},
                        {"tag": "lang", "attributes": {}, "text": "en"}
                    ]
                },
                {
                    "tag": "document-info",
                    "attributes": {},
                    "text": None,
                    "children": [
                        {"tag": "author", "attributes": {}, "text": "Victor Pelevin"},
                        {"tag": "program-used", "attributes": {}, "text": "Python fictionbook2 library"},
                        {"tag": "date", "attributes": {}, "text": "2024"},
                        {"tag": "src-url", "attributes": {}, "text": "https://example.com"},
                        {"tag": "id", "attributes": {}, "text": "123456789"},
                        {"tag": "version", "attributes": {}, "text": "1.0"}
                    ]
                },
                {
                    "tag": "publish-info",
                    "attributes": {},
                    "text": None,
                    "children": [
                        {"tag": "book-name", "attributes": {}, "text": "Book Name"},
                        {"tag": "publisher", "attributes": {}, "text": "Publisher"},
                        {"tag": "city", "attributes": {}, "text": "City"},
                        {"tag": "year", "attributes": {}, "text": "2024"},
                        {"tag": "isbn", "attributes": {}, "text": "1234567890"}
                    ]
                }
            ]
        }

        interim_xml = IntermediaryXmlFormat.from_dict(test_dict)
        interim_dict = interim_xml.to_dict()
        # Dump dictionaries to JSON files
        with open("expected_structure.json", "w") as f:
            json.dump(expected_structure, f, indent=4)

        with open("interim_structure.json", "w") as f:
            json.dump(interim_dict, f, indent=4)

        self.assertEqual(interim_dict, expected_structure)

    def test_from_dict3(self):
        """
        Test IntermediaryXmlFormat.from_dict with a complex dictionary
        Compare the result with the IntermediaryXmlFormat.__eq__ method
        """
        test_dict = {
            "description": {
                "title-info": {
                    "genre": "prose_contemporary",
                    "author": {
                        "first-name": "Victor",
                        "last-name": "Pelevin",
                        "home-page": "https://example.com"
                    },
                    "book-title": "Sol Invictus Book 1",
                    "annotation": "Sol Invictus Book 1",
                    "keywords": "book, keywords",
                    "date": "2020",
                    "lang": "en"
                },
                "document-info": {
                    "author": "Victor Pelevin",
                    "program-used": "Python fictionbook2 library",
                    "date": "2024",
                    "src-url": "https://example.com",
                    "id": "123456789",
                    "version": "1.0"
                },
                "publish-info": {
                    "book-name": "Book Name",
                    "publisher": "Publisher",
                    "city": "City",
                    "year": "2024",
                    "isbn": "1234567890"
                }
            }
        }

        # Convert test_dict to IntermediaryXmlFormat
        interim_xml = IntermediaryXmlFormat.from_dict(test_dict)

        # Create expected IntermediaryXmlFormat object with all the expected children
        expected_intermediary = IntermediaryXmlFormat(
            tag_name='description',
            children=[
                IntermediaryXmlFormat(
                    tag_name='title-info',
                    children=[
                        IntermediaryXmlFormat(tag_name='genre', text='prose_contemporary'),
                        IntermediaryXmlFormat(
                            tag_name='author',
                            children=[
                                IntermediaryXmlFormat(tag_name='first-name', text='Victor'),
                                IntermediaryXmlFormat(tag_name='last-name', text='Pelevin'),
                                IntermediaryXmlFormat(tag_name='home-page', text='https://example.com')
                            ]
                        ),
                        IntermediaryXmlFormat(tag_name='book-title', text='Sol Invictus Book 1'),
                        IntermediaryXmlFormat(tag_name='annotation', text='Sol Invictus Book 1'),
                        IntermediaryXmlFormat(tag_name='keywords', text='book, keywords'),
                        IntermediaryXmlFormat(tag_name='date', text='2020'),
                        IntermediaryXmlFormat(tag_name='lang', text='en')
                    ]
                ),
                IntermediaryXmlFormat(
                    tag_name='document-info',
                    children=[
                        IntermediaryXmlFormat(tag_name='author', text='Victor Pelevin'),
                        IntermediaryXmlFormat(tag_name='program-used', text='Python fictionbook2 library'),
                        IntermediaryXmlFormat(tag_name='date', text='2024'),
                        IntermediaryXmlFormat(tag_name='src-url', text='https://example.com'),
                        IntermediaryXmlFormat(tag_name='id', text='123456789'),
                        IntermediaryXmlFormat(tag_name='version', text='1.0')
                    ]
                ),
                IntermediaryXmlFormat(
                    tag_name='publish-info',
                    children=[
                        IntermediaryXmlFormat(tag_name='book-name', text='Book Name'),
                        IntermediaryXmlFormat(tag_name='publisher', text='Publisher'),
                        IntermediaryXmlFormat(tag_name='city', text='City'),
                        IntermediaryXmlFormat(tag_name='year', text='2024'),
                        IntermediaryXmlFormat(tag_name='isbn', text='1234567890')
                    ]
                )
            ]
        )

        # Compare structures
        self.assertEqual(interim_xml, expected_intermediary)

    def test_from_dict4(self):
        test_dict = {
            'body': [
                {
                    'section': {'title': "Sol Invictus Book 1"}
                },
                {
                    'section': [
                        {
                            'p': "I decided to face my thirtieth birthday, riding down the highway on a motorcycle."
                        },
                        {
                            'p': "Daddy showed up — probably, he sensed that I was thinking about his pasta. He even came to my house. At first, I couldn't understand what it was all of a sudden, until he said it himself. Thirty years. Well, yeah, the anniversary."
                        }
                    ]
                }
            ]
        }

        expected_dict = {
            'tag': 'body',
            'attributes': {},
            'text': 'Sol Invictus Book 1',
            'children': [
                {
                    'tag': 'section',
                    'attributes': {},
                    'text': None,
                    'children': [
                        {
                            'tag': 'title',
                            'attributes': {},
                            'text': 'Sol Invictus Book 1'
                        }
                    ]
                },
                {
                    'tag': 'section',
                    'attributes': {},
                    'text': None,
                    'children': [
                        {
                            'tag': 'p',
                            'attributes': {},
                            'text': 'I decided to face my thirtieth birthday, riding down the highway on a motorcycle.'
                        },
                        {
                            'tag': 'empty-line',
                            'attributes': {},
                            'text': ''
                        },
                        {
                            'tag': 'p',
                            'attributes': {},
                            'text': "Daddy showed up — probably, he sensed that I was thinking about his pasta. He even came to my house. At first, I couldn't understand what it was all of a sudden, until he said it himself. Thirty years. Well, yeah, the anniversary."
                        }
                    ]
                }
            ]
        }
        interim_xml = IntermediaryXmlFormat.from_dict(test_dict)
        dump_to_json(expected_dict, interim_xml.to_dict())
        self.assertEqual(interim_xml.to_dict(), expected_dict)

        if __name__ == '__main__':
            unittest.main()
