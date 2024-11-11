# -*- coding: utf-8 -*-
import os
import json
import base64
from xml.etree.ElementTree import Element, SubElement
from xml.etree.ElementTree import ElementTree as et

import markdown2


class Fb2Writer:

    def __init__(self, file_name, images_dir):
        """
        The book structure is a dictionary that is capable
        of storing sub-dicts and sub-lists.
        If a value is another dictionary, the resulting XML structure will have
        a single element with such a name, e.g.,
        <description>...</description>.
        If a value is a list, e.g., "binary": ["image1.jpg", "image2.jpg"],
        then the XML structure will have multiple elements with the same name, e.g.,
        <binary>image1.jpg</binary>
        <binary>image2.jpg</binary>.
        :param file_name:
        :param images_dir:
        """
        self.file_name = file_name
        self.images_dir = images_dir
        self.metadata = None
        self.body = None
        self.cover_image = None

        # Create root element
        self.root = Element("FictionBook", attrib={
            "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
            "xmlns:l": "http://www.w3.org/1999/xlink"
        })
        # Create 'description' and 'body' elements
        self.description_elem = SubElement(self.root, "description")
        self.body_elem = SubElement(self.root, "body")

    def dict_to_element(self, parent, data):
        """
        Recursively convert a dictionary to XML elements
        :param parent: parent Element
        :param data: dictionary
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    child = SubElement(parent, key)
                    self.dict_to_element(child, value)
                elif isinstance(value, list):
                    for item in value:
                        child = SubElement(parent, key)
                        self.dict_to_element(child, item)
                else:
                    child = SubElement(parent, key)
                    child.text = str(value)
        elif isinstance(data, list):
            for item in data:
                self.dict_to_element(parent, item)
        else:
            parent.text = str(data)

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

        self.metadata = self.description_elem  # for clarity
        self.dict_to_element(self.metadata, metadata)

    def set_paragraphs(self, paragraphs, content_type):
        """
        Wraps the specific paragraph setting methods.
        :param paragraphs: list of paragraphs to set
        :param content_type: type of content to set ('plaintext', 'markdown', 'xml')
        """
        if content_type == 'plaintext':
            self._set_paragraphs_plaintext(paragraphs)
        elif content_type == 'markdown':
            self._set_paragraphs_markdown(paragraphs)
        elif content_type == 'xml':
            self._set_paragraphs_xml(paragraphs)
        else:
            raise ValueError("Unsupported content type")

    def _convert_html_to_fb2(self, html_content):
        """
        Helper method to convert HTML content (derived from Markdown) to FB2 tags.
        """
        # This is a simplified example. Ideally, you would use an HTML parser.
        html_content = html_content.replace("<em>", f'<emphasis>')
        html_content = html_content.replace("</em>", f'</emphasis>')
        html_content = html_content.replace("<strong>", f'<strong>')
        html_content = html_content.replace("</strong>", f'</strong>')
        # Add other conversions as needed
        return html_content

    def _set_paragraphs_plaintext(self, paragraphs):
        """
        Set the book body from a list of paragraphs
        :param paragraphs:
        """
        assert isinstance(paragraphs, list), "paragraphs must be a list"
        assert len(paragraphs) > 0, "paragraphs must not be empty"

        self.body = self.body_elem

        # Get book title from metadata
        book_title_elem = self.metadata.find(".//book-title")
        if book_title_elem is not None:
            book_title = book_title_elem.text
        else:
            book_title = ""

        # Add a title to body
        title_elem = SubElement(self.body, "title")
        p_elem = SubElement(title_elem, "p")
        p_elem.text = book_title

        # Add 'section' element
        section_elem = SubElement(self.body, "section")

        if isinstance(paragraphs[0], list):
            for sub_list in paragraphs:
                for paragraph in sub_list:
                    p_elem = SubElement(section_elem, "p")
                    p_elem.text = paragraph
                # Add an empty-line
                empty_line_elem = SubElement(section_elem, "empty-line")
        elif isinstance(paragraphs[0], str):
            for paragraph in paragraphs:
                p_elem = SubElement(section_elem, "p")
                p_elem.text = paragraph
        else:
            raise ValueError(f"Invalid paragraph type {type(paragraphs[0])}")

    def _set_paragraphs_markdown(self, paragraphs):
        """
        Converts markdown content to FB2 tags, e.g., *text* to <emphasis>text</emphasis>,
        **text** to <strong>text</strong>, and so on.
        """
        md_parser = markdown2.Markdown(extras=["footnotes"])
        for paragraph in paragraphs:
            html_content = md_parser.convert(paragraph)
            p = et.SubElement(self.body, 'p')
            p.text = self._convert_html_to_fb2(html_content)

    def _set_paragraphs_xml(self, paragraphs):
        """
        Writes every list item as is, assuming it's correct XML.
        """
        for paragraph in paragraphs:
            self.body.append(et.fromstring(paragraph))

    def set_body(self, body):
        """
        Advanced method to set the book body without any processing
        :param body: dict
        """
        # Clear current body element
        self.body_elem.clear()
        self.dict_to_element(self.body_elem, body)

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                self.indent(child, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

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

        # Handle images
        self._encode_images()

        if pretty_xml:
            self.indent(self.root)

        # Create XML tree
        tree = ElementTree(self.root)
        tree.write(self.file_name, encoding='utf-8', xml_declaration=True)

        if debug_mode:
            # Create XML and JSON files for debugging
            tree.write(self.file_name + '.xml', encoding='utf-8', xml_declaration=True)
            # For JSON, we need to convert the XML tree to a dict
            root_dict = self.element_to_dict(self.root)
            with open(self.file_name + '.json', 'w', encoding='utf-8') as f:
                json.dump(root_dict, f, ensure_ascii=False, indent=4)

    def element_to_dict(self, elem):
        d = {}
        if elem.attrib:
            d["@attributes"] = elem.attrib
        if elem.text and elem.text.strip():
            d["#text"] = elem.text.strip()
        for child in elem:
            child_dict = self.element_to_dict(child)
            if child.tag not in d:
                d[child.tag] = child_dict
            else:
                if isinstance(d[child.tag], list):
                    d[child.tag].append(child_dict)
                else:
                    d[child.tag] = [d[child.tag], child_dict]
        return d

    def validate(self):
        """
        Validate the book structure before writing to a file
        Check list:
        * if the "description" and "body" elements are present
        * if the "title-info" and "author" elements are present in the "description" element
        * if the values of the "title-info" and "author" elements are not empty
        :return: True if valid, False otherwise
        """
        if self.metadata is None or self.body is None:
            return False
        title_info = self.metadata.find("title-info")
        if title_info is None:
            return False
        book_title = title_info.find("book-title")
        authors = title_info.findall("author")
        if book_title is None or not authors:
            return False
        return True

    def _encode_images(self):
        """
        Encode images from the images directory to base64 and add them to the book structure
        """
        if not os.path.exists(self.images_dir):
            return
        print(f'Encoding images... from {os.path.abspath(self.images_dir)}')
        for filename in os.listdir(self.images_dir):
            ext = filename.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                image_path = os.path.join(self.images_dir, filename)
                with open(image_path, 'rb') as image_file:
                    print(f'Encoding {filename}...')
                    image_data = image_file.read()
                    image_data_base64 = base64.b64encode(image_data).decode('utf-8')
                    image_attributes = {
                        "id": filename,
                        "content-type": f"image/{ext}"
                    }
                    binary_elem = SubElement(self.root, "binary", attrib=image_attributes)
                    binary_elem.text = image_data_base64
