# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et


class Fb2Reader:
    def __init__(self, file_path, images_dir):
        self.file_path = file_path
        self.images_dir = images_dir
        self.metadata = {}
        self.chapters = []
        self.cover_image = None

    def chapter_count(self):
        return len(self.chapters)

    def read(self):
        tree = et.parse(self.file_path)
        root = tree.getroot()

        self._extract_metadata(root)
        self._extract_chapters(root)

    def _extract_metadata(self, root):
        description_tag = root.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}description")
        title_info_tag = description_tag.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}title-info")

        # Extract metadata properties recursively
        self._extract_metadata_properties(title_info_tag, self.metadata)

    def _extract_metadata_properties(self, parent_elem, metadata_dict):
        for elem in parent_elem:
            if len(elem) > 0:
                # Recursively set nested properties
                sub_dict = {}
                metadata_dict[elem.tag] = sub_dict
                self._extract_metadata_properties(elem, sub_dict)
            else:
                # Set current property
                metadata_dict[elem.tag] = elem.text.strip() if elem.text else ""

            # Handle cover image
            if elem.tag.endswith("coverpage") and elem.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image") is not None:
                href = elem.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image").attrib["l:href"]
                self.cover_image = href[1:]  # Remove the '#' character

    def _extract_chapters(self, root):
        body_tag = root.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}body")

        for section_tag in body_tag.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}section"):
            chapter = []
            for p_tag in section_tag.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}p"):
                paragraph = p_tag.text.strip() if p_tag.text else ""
                chapter.append(paragraph)
            self.chapters.append(chapter)
