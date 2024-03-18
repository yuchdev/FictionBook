import json
import xml.etree.ElementTree as et


class IntermediaryXmlFormat:
    """
    Intermediary format for storing book data
    Can be serialized and deserialized to/from XML or JSON

    Examples:
    1. Intermediary format of paragraph with id=1 and no children:
    XML:
        <p id="1">Paragraph Text</p>
    JSON:
        {
            "tag": "p",
            "attributes": {"id": "1"},
            "text": "Paragraph Text"
        }

    2.  Intermediary format of section with id=1 and children (2 paragraphs):
    XML:
        <section id="1">
            <p id="1">Paragraph 1</p>
            <p id="2">Paragraph 2</p>
        </section>
    JSON:
        {
            "tag": "section",
            "attributes": {"id": "1"},
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
    """

    def __init__(self, tag_name, attributes=None, children=None, text=None):
        """
        Initialize the IntermediaryXmlFormat object
        :param tag_name: element tag name, e.g. "description", "section", "p"
        :param attributes: element attributes, e.g. {"id": "1", "class": "chapter"}
        :param children: list of child objects of IntermediaryXmlFormat type
        :param text: content of the element
        """
        assert isinstance(tag_name, str), "tag_name must be a string"
        self.tag_name = tag_name
        self.attributes = attributes or {}
        self.children = children or []
        self.text = text

    def __repr__(self):
        """
        XML representation of the object
        :return: XML string
        """
        return self.to_xml()

    def __str__(self):
        """
        XML representation of the object
        :return: XML string
        """
        return self.to_xml()

    def add_child(self, child):
        """
        Add a child object to the current object
        E.g.
        <section>
            <p>...</p>
        </section>
        :param child: IntermediaryXmlFormat object
        """
        self.children.append(child)

    def add_children(self, children):
        """
        Add multiple child objects to the current object
        :param children: list of IntermediaryXmlFormat objects
        """
        self.children.extend(children)

    def add_attribute(self, key, value):
        """
        Add an attribute to the current object
        e.g. <p class="chapter">...</p>
        :param key: unique attribute key
        :param value: e.g. "chapter", "1"
        """
        self.attributes[key] = value

    def set_text(self, text):
        """
        Set the content of the current object
        E.g. <p>content</p>
        :param text: content of the element
        """
        self.text = text

    def to_xml(self):
        """
        Convert the object to XML string
        :return: unformatted XML string
        """
        attributes_str = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        opening_tag = f'<{self.tag_name} {attributes_str}>' if attributes_str else f'<{self.tag_name}>'
        closing_tag = f'</{self.tag_name}>'
        children_str = ''.join(child.to_xml() for child in self.children)
        text_str = self.text or ''
        return f"{opening_tag}{text_str}{children_str}{closing_tag}"

    def to_dict(self):
        """
        Convert the object to Python dictionary
        Warning: we lose attributes while converting to JSON
        :return: Python dictionary
        """
        result = {
                "tag": self.tag_name,
                "attributes": self.attributes,
                "text": self.text
            }
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result

    def to_json(self):
        """
        Convert the object to JSON string
        :return: JSON string
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_xml(cls, xml_str):
        """
        Create IntermediaryXmlFormat object from XML string
        :param xml_str: XML string
        """
        root = et.fromstring(xml_str)
        return cls._from_element(root)

    @classmethod
    def from_dict(cls, json_dict):
        """
        Create IntermediaryXmlFormat object from dictionary
        Created format looks like IntermediaryXmlFormat without attributes
        (attributes are not supported in JSON)

        Example JSON:
        {
            "description": {
                "title-info": {
                    "book-title": "Title",
                    "author": "Author"
                }
            },
            "body": {
                "section": [
                    {
                        "title": "Title",
                        "p": "Paragraph"
                    }
                ]
            }
        }

        Resulting intermediary format:
        <description>
            <title-info>
                <book-title>Title</book-title>
                <author>Author</author>
            </title-info>
            <body>
                <section>
                    <title>Title</title>
                    <p>Paragraph</p>
                </section>
            </body>
        </description>

        :param json_dict: JSON as a dictionary
        :return: IntermediaryXmlFormat object
        """
        tag_name, data = list(json_dict.items())[0]
        children = [IntermediaryXmlFormat.from_dict(child) for child in data]
        return cls(tag_name, children=children)

    @classmethod
    def from_json(cls, json_str):
        """
        Create IntermediaryXmlFormat object from JSON string
        :param json_str: JSON string
        """
        json_dict = json.loads(json_str)
        return cls.from_dict(json_dict)

    @classmethod
    def _from_element(cls, element):
        """
        Create IntermediaryXmlFormat object from XML element
        :param element: XML element
        :return: IntermediaryXmlFormat object
        """
        children = [cls._from_element(child) for child in element]
        return cls(element.tag, children=children)
