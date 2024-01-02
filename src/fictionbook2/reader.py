# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et


class Fb2Reader:
    def __init__(self, file_path, images_dir):
        self.file_path = file_path
        self.images_dir = images_dir
        self.metadata = {}
        self.chapters = []
        self.paragraphs = []
        self.cover_image = None

    def chapter_count(self):
        return len(self.chapters)

    def _chapters_to_paragraphs(self, chapters):
        """
        Convert list of chapters to lost of paragraphs (strings ended with EOL)
        :return: list of paragraphs
        """
        paragraphs = []
        for chapter in chapters:
            if isinstance(chapter, list):
                # If the chapter is a list, it contains subchapters, so recursively process it
                subchapter_paragraphs = self._chapters_to_paragraphs(chapters=chapter)
                paragraphs.extend(subchapter_paragraphs)
            elif isinstance(chapter, str):
                # If the chapter is a string, it's a leaf node (paragraph)
                paragraphs.append(chapter)
        return paragraphs

    def read(self):
        tree = et.parse(self.file_path)
        root = tree.getroot()

        self._extract_metadata(root)
        self._extract_chapters(root)
        self.paragraphs = self._chapters_to_paragraphs(self.chapters)

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
                # clean elem.tag from namespace
                elem.tag = elem.tag.split("}")[1]
                metadata_dict[elem.tag] = sub_dict
                self._extract_metadata_properties(elem, sub_dict)
            else:
                # clean elem.tag from namespace
                elem.tag = elem.tag.split("}")[1]
                # Set current property
                metadata_dict[elem.tag] = elem.text.strip() if elem.text else ""

            # Handle cover image
            if elem.tag.endswith("coverpage") and elem.find(
                    ".//{http://www.gribuser.ru/xml/fictionbook/2.0}image") is not None:
                image_elem = elem.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image")
                href_attr = image_elem.attrib.get("{http://www.w3.org/1999/xlink}href")
                if href_attr is not None:
                    self.cover_image = href_attr[1:]  # Remove the '#' character

    def _extract_chapters(self, root):
        body_tag = root.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}body")

        for section_tag in body_tag.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}section"):
            chapter = []
            for p_tag in section_tag.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}p"):
                paragraph = p_tag.text.strip() if p_tag.text else ""
                chapter.append(paragraph)
            self.chapters.append(chapter)
