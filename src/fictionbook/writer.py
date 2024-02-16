# -*- coding: utf-8 -*-
import base64
import os
import shutil
import json
import xml.etree.ElementTree as et
from intermediary_format import IntermediaryXmlFormat


class Fb2Writer:

    def __init__(self, file_name, images_dir):
        """
        The book structure is a dictionary that is capable
        storing sub-dicts and sub-lists.
        If value is another dictionary, resulting XML structure will have
        single element with such a name, e.g.
        <description>...</description>.
        If value is a list, e.g. "binary": ["image1.jpg", "image2.jpg"],
        then XML structure will have multiple elements with the same name, e.g.
        <binary>image1.jpg</binary>
        <binary>image2.jpg</binary>.
        :param file_name:
        :param images_dir:
        """
        if not file_name.endswith(".fb2"):
            file_name += ".fb2"
        self.file_name = file_name
        self.images_dir = images_dir
        self.book_structure = IntermediaryXmlFormat.from_dict(
            {"description": {}, "body": {}, "binary": []}
        )
        self.fiction_book = None

    def set_metadata(self, metadata):
        # Check for required elements in title-info
        title_info_data = metadata.get("title-info", {})
        if "book-title" not in title_info_data or "author" not in title_info_data:
            raise ValueError("Both 'book-title' and 'author' are required in title-info")

        for info_type, info_data in metadata.items():
            self.book_structure["description"][info_type] = info_data

    def set_paragraphs(self, paragraphs):
        self.book_structure["body"] = []

        # Add a section with the book title and subtitle
        self.book_structure["body"].append({'section': {
            "title": self.book_structure["description"]["title-info"]["book-title"]
        }})

        # Create a section for paragraphs
        section = {"section": []}

        # Check if paragraphs is a list of lists (chapters), or just a list of paragraphs
        # and add an "empty-line" item after each chapter
        if isinstance(paragraphs[0], list):
            for sub_list in paragraphs:
                for paragraph in sub_list:
                    section["section"].append({"p": paragraph})
                section["section"].append({"empty-line": ""})
        else:
            for paragraph in paragraphs:
                section["section"].append({"p": paragraph})

        self.book_structure["body"].append(section)

    def set_body(self, body):
        """
        Advanced method to set the book body without any processing
        :param body: dict
        """
        self.book_structure["body"] = body

    def write(self, metadata=None, paragraphs=None, debug_mode=False, pretty_xml=True):
        """
        Write the book to a file
        :param metadata: Book metadata containing title, author, etc.
        :param paragraphs: Book content, either list of paragraphs or list of lists of paragraphs
        :param debug_mode: If true, create XML and JSON files for debugging
        :param pretty_xml: If true, create a pretty XML structure inside the FB2 file
        """
        # Create root element
        # TODO: replace self.fiction_book with IntermediaryXmlFormat
        self.fiction_book = et.Element("FictionBook", attrib={
            "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
            "xmlns:l": "http://www.w3.org/1999/xlink"
        })

        if metadata is not None:
            self.set_metadata(metadata)
        if paragraphs is not None:
            self.set_paragraphs(paragraphs)

        # Validate the book structure
        if not self.validate():
            raise ValueError("Invalid book structure")

        # Set metadata and chapters
        self._to_xml(self.book_structure, self.fiction_book)

        # Create XML tree
        if pretty_xml:
            tree = et.ElementTree(self.fiction_book)
            xml_str = et.tostring(self.fiction_book, encoding='utf-8')
            pretty_xml_str = parseString(xml_str).toprettyxml(indent="  ")
            with open(self.file_name, 'w', encoding='utf-8') as f:
                f.write(pretty_xml_str)
        else:
            tree = et.ElementTree(self.fiction_book)
            tree.write(self.file_name, encoding='utf-8', xml_declaration=True)

        if debug_mode:
            # Create XML and JSON files for debugging
            shutil.copyfile(self.file_name, self.file_name + '.xml')
            with open(self.file_name + '.json', 'w', encoding='utf-8') as f:
                json.dump(self.book_structure, f, ensure_ascii=False, indent=4)

    def validate(self):
        """
        Validate the book structure before writing to a file
        Check list:
        * if the "description" and "body" keys are present in the book_structure dictionary
        * if the "title-info" and "author" keys are present in the "description" dictionary
        * if the values of the "title-info" and "author" keys are not empty
        :return: True if valid, False otherwise
        """
        if "description" not in self.book_structure or "body" not in self.book_structure:
            print("The tag 'description' or 'body' is missing")
            return False
        if "title-info" not in self.book_structure["description"] or "author" not in self.book_structure["description"]["title-info"]:
            print("The tag 'title-info' or 'author' is missing")
            return False
        if not self.book_structure["description"]["title-info"]["author"]:
            print("The author name is missing")
            return False
        if not self.book_structure["description"]["title-info"]["book-title"]:
            print("The book title is missing")
            return False
        return True

    def _encode_images(self):
        """
        Encode images from the images directory to base64 and add them to the book structure
        """
        for filename in os.listdir(self.images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(self.images_dir, filename)
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_data_base64 = base64.b64encode(image_data).decode('utf-8')
                    self.book_structure["binary"].append(image_data_base64)

    def _to_xml(self, properties, parent_elem):
        for key, value in properties.items():
            # Create a new XML element for this key
            sub_elem = et.SubElement(parent_elem, key)
            if isinstance(value, dict):
                # Recursively set nested properties
                self._to_xml(value, sub_elem)
            elif isinstance(value, list):
                # Iterate over the list
                for item in value:
                    # Call _to_xml() for each item in the list
                    self._to_xml(item, sub_elem)
            else:
                # Set current property
                sub_elem.text = value
