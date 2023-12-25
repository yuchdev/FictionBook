# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as et


class Fb2Writer:
    def __init__(self, file_name):
        if not file_name.endswith(".fb2"):
            file_name += ".fb2"
        self.file_name = file_name
        # Create root element
        self.fiction_book = et.Element("FictionBook", attrib={
            "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
            "xmlns:l": "http://www.w3.org/1999/xlink"
        })

    def set_metadata(self, metadata):
        description = et.SubElement(self.fiction_book, "description")

        # Check for required elements in title-info
        title_info_data = metadata.get("title-info", {})
        if "book-title" not in title_info_data or "author" not in title_info_data:
            raise ValueError("Both 'book-title' and 'author' are required in title-info")

        for info_type, info_data in metadata.items():
            info_type_elem = et.SubElement(description, info_type)

            # Set metadata properties for the current info_type
            self._set_metadata_properties(info_data, info_type_elem)

    def _set_metadata_properties(self, properties, parent_elem):
        for key, value in properties.items():
            if isinstance(value, dict):
                # Recursively set nested properties
                sub_elem = et.SubElement(parent_elem, key)
                self._set_metadata_properties(value, sub_elem)
            else:
                # Set current property
                elem = et.SubElement(parent_elem, key)
                elem.text = value

    def add_coverpage(self, image_file):
        title_info = self.fiction_book.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}title-info")

        if title_info is None:
            raise ValueError("Title-info element not found")

        coverpage_elem = et.SubElement(title_info, "coverpage")
        image_elem = et.SubElement(coverpage_elem, "image", attrib={"l:href": f"#{image_file}"})

    def set_chapters(self, chapters):
        body = et.SubElement(self.fiction_book, "body")
        for chapter_text in chapters:
            section = et.SubElement(body, "section")
            title = et.SubElement(section, "title")
            title.text = chapter_text.get("title")

            # Add chapter text paragraphs
            for paragraph in chapter_text.get("paragraphs", []):
                p = et.SubElement(section, "p")
                p.text = paragraph

    def write(self, cover, chapters, metadata):

        # Set metadata and chapters
        self.set_metadata(metadata)
        self.add_coverpage(cover)
        self.set_chapters(chapters)

        # Create XML tree
        tree = et.ElementTree(self.fiction_book)
        tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
