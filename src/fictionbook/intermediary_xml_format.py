from lxml import etree


class IntermediaryXmlFormat:

    def __init__(self, tag_name=None, attributes=None, children=None, text=None):
        """
        Initialize the IntermediaryXmlFormat object using lxml elements
        """
        if tag_name:
            self.element = etree.Element(tag_name)
            if attributes:
                for key, value in attributes.items():
                    self.element.attrib[key] = value
            if children:
                for child in children:
                    self.element.append(child.element)
            if text:
                self.element.text = text

    def __repr__(self):
        """
        XML representation of the object
        :return: XML string
        """
        return etree.tostring(self.element, encoding='unicode')

    def __str__(self):
        """
        XML representation of the object
        :return: XML string
        """
        return etree.tostring(self.element, pretty_print=True, encoding='unicode')

    def __eq__(self, other):
        """
        Check if two IntermediaryXmlFormat objects are equal.
        :param other: IntermediaryXmlFormat object
        :return: True if the objects are equal, False otherwise
        """
        return self.element == other.element

    def __ne__(self, other):
        """
        Check if two IntermediaryXmlFormat objects are not equal.
        :param other: IntermediaryXmlFormat object
        :return: True if the objects are not equal, False otherwise
        """
        return not self == other

    def add_child(self, child):
        """
        Add a child object to the current object.
        :param child: IntermediaryXmlFormat object
        """
        assert isinstance(child, IntermediaryXmlFormat), "child must be IntermediaryXmlFormat"
        self.element.append(child.element)

    def add_attribute(self, key, value):
        """
        Add an attribute to the current object.
        :param key: attribute name
        :param value: attribute value
        """
        self.element.attrib[key] = value

    def set_text(self, text):
        """
        Set the content of the current object.
        :param text: content of the element
        """
        self.element.text = text.strip()

    def to_dict(self):
        """
        Convert the IntermediaryXmlFormat object to a dictionary format.
        Children are represented as a list of dictionaries, each with one element.
        """
        result = {}
        children_list = []
        for child in self.element:
            child_intermediary = IntermediaryXmlFormat(child.tag)
            child_intermediary.element = child
            children_list.append(child_intermediary.to_dict())

        if children_list:
            result[self.element.tag] = children_list
        else:
            result[self.element.tag] = self.element.text if self.element.text else None
        return result

    def to_xml(self):
        """
        Convert the IntermediaryXmlFormat object to an XML string.
        """
        return self.__str__()

    @classmethod
    def from_dict(cls, data):
        """
        Recreate an IntermediaryXmlFormat object from a dictionary.
        Assumes each child is represented as a dictionary in a list, each containing exactly one element.
        """
        tag_name, content = next(iter(data.items()))
        if isinstance(content, list):
            children = [cls.from_dict(child) for child in content]
            return cls(tag_name, children=children)
        else:
            return cls(tag_name, text=content)

    @classmethod
    def from_xml(cls, xml_str):
        """
        Create an IntermediaryXmlFormat object from an XML string.
        :param xml_str: XML string
        """
        element = etree.fromstring(xml_str)
        return cls._from_element(element)

    @classmethod
    def _from_element(cls, element):
        """
        Helper method to create an IntermediaryXmlFormat from an lxml element.
        :param element: lxml Element
        """
        children = [cls._from_element(child) for child in element]
        return cls(element.tag, element.text, children)
