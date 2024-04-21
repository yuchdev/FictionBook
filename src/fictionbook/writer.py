# -*- coding: utf-8 -*-
import os
import shutil
import json
import xml.etree.ElementTree as et
from base64 import b64encode

from fictionbook.intermediary_xml_format import IntermediaryXmlFormat


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
        self.metadata = None
        self.body = None
        self.cover_image = None
        self.root = IntermediaryXmlFormat(
            tag_name="FictionBook",
            attributes={
                "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
                "xmlns:l": "http://www.w3.org/1999/xlink"
            },
            children=[
                IntermediaryXmlFormat("description"),
                IntermediaryXmlFormat("body")
            ])

    def set_metadata(self, metadata):
        """
        Check for required elements in title-info and set metadata
        :param metadata:
        """
        assert isinstance(metadata, dict), "metadata must be a dictionary"
        assert len(metadata) > 0, "metadata must not be empty"

        title_info_data = metadata.get("title-info", {})
        if "book-title" not in title_info_data or "author" not in title_info_data:
            raise ValueError("Both 'book-title' and 'author' are required in title-info")

        print(f"METADATA 1: {metadata}")
        interim = IntermediaryXmlFormat.from_dict(metadata)
        print(f"METADATA 2: {interim.to_dict()}")
        self.root.add_child(interim)
        self.metadata = interim

    def set_paragraphs(self, paragraphs):
        """
        Set the book body from a list of paragraphs
        :param paragraphs:
        """
        assert isinstance(paragraphs, list), "paragraphs must be a list"
        assert len(paragraphs) > 0, "paragraphs must not be empty"

        self.body = self.root.filter_tag("body")[0]

        # Add a section with the book title and subtitle
        body = {
            "title": self.metadata.filter_tag("book-title")[0].text,
            "section": []
        }

        # Check if paragraphs is a list of lists (chapters), or just a list of paragraphs
        # and add an "empty-line" item after each chapter
        if isinstance(paragraphs[0], list):
            for sub_list in paragraphs:
                for paragraph in sub_list:
                    body["section"].append({"p": paragraph})
                body["section"].append({"empty-line": ""})
        else:
            for paragraph in paragraphs:
                body["section"].append({"p": paragraph})

        print("BODY: ", body)
        intermediate_xml = IntermediaryXmlFormat.from_dict(body)
        print("INTERMEDIATE XML", intermediate_xml.to_dict())

        self.root.add_child(intermediate_xml)
        self.body = body

    def set_body(self, body):
        """
        Advanced method to set the book body without any processing
        :param body: dict
        """
        self.body = IntermediaryXmlFormat.from_dict(body)

    def write(self, metadata=None, paragraphs=None, debug_mode=False, pretty_xml=True):
        """
        Write the book to a file
        :param metadata: Book metadata containing title, author, etc.
        :param paragraphs: Book content, either list of paragraphs or list of lists of paragraphs
        :param debug_mode: If true, create XML and JSON files for debugging
        :param pretty_xml: If true, create a pretty XML structure inside the FB2 file
        """
        if metadata is not None:
            self.set_metadata(metadata)
        if paragraphs is not None:
            self.set_paragraphs(paragraphs)
        # Validate the book structure
        if not self.validate():
            raise ValueError("Invalid book structure")

        xml_str = self.root.to_xml()
        xml_root = et.fromstring(xml_str)

        # Create XML tree
        if pretty_xml:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                f.write(xml_str)
        else:
            tree = et.ElementTree(xml_root)
            tree.write(self.file_name, encoding='utf-8', xml_declaration=True)

        if debug_mode:
            # Create XML and JSON files for debugging
            shutil.copyfile(self.file_name, self.file_name + '.xml')
            with open(self.file_name + '.json', 'w', encoding='utf-8') as f:
                json.dump(self.root.to_dict(), f, ensure_ascii=False, indent=4)

    def validate(self):
        """
        Validate the book structure before writing to a file
        Check list:
        * if the "description" and "body" keys are present in the book_structure dictionary
        * if the "title-info" and "author" keys are present in the "description" dictionary
        * if the values of the "title-info" and "author" keys are not empty
        :return: True if valid, False otherwise
        """
        if not self.metadata or not self.body:
            return False
        if not self.metadata.filter_tag("title-info") or not self.metadata.filter_tag("author"):
            return False
        if not self.metadata.filter_tag("book-title") or not self.metadata.filter_tag("author"):
            return False
        return True

    def _encode_images(self):
        """
        Encode images from the images directory to base64 and add them to the book structure
        """
        self.images_dir = os.path.abspath(self.images_dir)
        assert os.path.isdir(self.images_dir), "Images directory does not exist"
        print(f'Encoding images... from {self.images_dir}')

        for filename in os.listdir(self.images_dir):
            ext = filename.split('.')[-1]
            if ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
                image_path = os.path.join(self.images_dir, filename)
                with open(image_path, 'rb') as image_file:
                    print(f'Encoding {filename}...')
                    image_data = b64encode(image_file.read()).decode('utf-8')
                    image_attributes = {
                        "id": filename,
                        "content-type": f"image/{ext}"
                    }
                    self.root.add_child(
                        IntermediaryXmlFormat(tag_name="binary", attributes=image_attributes, text=image_data)
                    )
