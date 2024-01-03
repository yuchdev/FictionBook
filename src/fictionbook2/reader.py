# -*- coding: utf-8 -*-
import base64
import os
import urllib.request
import urllib.error
from xml.etree.ElementTree import parse


class Fb2Reader:
    """
    FictionBook2 reader
    """

    def __init__(self, file_path: str, images_dir: str, download_images=False):
        """
        :param file_path:
        :param images_dir:
        """
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not isinstance(images_dir, str):
            raise TypeError("images_dir must be a string")
        self.file_path = file_path
        self.images_dir = images_dir
        self.metadata = {}
        self.chapters = []
        self.paragraphs = []
        self.cover_image = None
        if not os.path.isdir(self.images_dir):
            os.mkdir(self.images_dir)
        self._read(download_images)

    @property
    def cover(self):
        return os.path.join(self.images_dir, self.cover_image) if self.cover_image else None

    @property
    def images(self):
        return [os.path.join(self.images_dir, image) for image in os.listdir(self.images_dir)]

    def _read(self, download_images=False):
        tree = parse(self.file_path)
        root = tree.getroot()

        self._extract_metadata(root)
        self._extract_chapters(root)
        self.paragraphs = self._chapters_to_paragraphs(self.chapters)
        self._extract_images(root)
        if download_images:
            self._download_images(root)

    def _chapters_to_paragraphs(self, chapters):
        """
        Convert list of chapters to lost of paragraphs (strings ended with EOL)
        :return: list of paragraphs
        """
        if not isinstance(chapters, list):
            raise TypeError("chapters must be a list")
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

    def _extract_metadata(self, root):
        """
        Extract metadata from the root element
        :param root: xml.etree.ElementTree.Element pointing to the root element of metadata
        """
        description_tag = root.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}description")

        # Extract metadata properties recursively
        self._extract_metadata_properties(description_tag, self.metadata)

    def _extract_metadata_properties(self, parent_elem, metadata_dict):
        """
        Convert metadata properties recursively from xml.etree.ElementTree.Element to dict
        :param parent_elem: xml.etree.ElementTree.Element pointing to the parent element of metadata
        :param metadata_dict: Dictionary to store metadata properties
        :return:
        """
        for elem in parent_elem:
            if len(elem) > 0:
                # Recursively set nested properties
                sub_dict = {}
                # Set current property with the correct namespace
                tag = elem.tag.split("}")[1] if '}' in elem.tag else elem.tag
                metadata_dict[tag] = sub_dict
                self._extract_metadata_properties(elem, sub_dict)
            else:
                # Set current property with the correct namespace
                tag = elem.tag.split("}")[1] if '}' in elem.tag else elem.tag
                metadata_dict[tag] = elem.text.strip() if elem.text else ""

            # Handle cover image
            if elem.tag.endswith("coverpage"):
                self._extract_cover(elem)

    def _extract_cover(self, elem):
        """
        Find the image element directly within the coverpage
        """
        if (image_elem := elem.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image")) is not None:
            if (href_attr := image_elem.attrib.get("{http://www.w3.org/1999/xlink}href")) is not None:
                # Remove the # character
                self.cover_image = href_attr[1:]

    def _extract_chapters(self, root):
        body_tag = root.find(".//{http://www.gribuser.ru/xml/fictionbook/2.0}body")
        for section_tag in body_tag.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}section"):
            chapter = []
            for p_tag in section_tag.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}p"):
                paragraph = p_tag.text.strip() if p_tag.text else ""
                chapter.append(paragraph)
            self.chapters.append(chapter)

    def _extract_images(self, root):
        binary_elements = root.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}binary")
        for binary_elem in binary_elements:
            content_type = binary_elem.attrib.get("content-type", "")
            image_data = binary_elem.text.strip() if binary_elem.text else ""
            image_id = binary_elem.attrib.get("id", "")

            if image_data and image_id and content_type.startswith("image/"):
                # Save binary images using the specified id
                self._save_image_from_binary(image_data, content_type, image_id)

    def _save_image_from_binary(self, image_data, content_type, image_id):
        image_extension = content_type.split("/")[-1]
        image_name, ext = os.path.splitext(image_id)

        if not ext:
            ext = f".{image_extension.lower()}"

        image_path = os.path.abspath(os.path.join(self.images_dir, image_name + ext))

        with open(image_path, 'wb') as image_file:
            image_file.write(base64.b64decode(image_data))

    def _download_images(self, root):
        """
        Download images from the book if <image l:href="https..."> tag is used
        and points to URL in the internet
        Note: Images may repeat so we use set() to avoid duplicates
        """
        images = set()
        image_elements = root.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image")
        for image_elem in image_elements:
            href_attr = image_elem.attrib.get("{http://www.w3.org/1999/xlink}href", "")
            if href_attr.startswith("http"):
                images.add(href_attr)
        # download images
        for image_url in images:
            self._download_image(image_url)

    def _download_image(self, image_url):
        try:
            with urllib.request.urlopen(image_url) as response:
                if response.code == 200:
                    image_name = os.path.basename(image_url)
                    image_path = os.path.join(self.images_dir, image_name)

                    with open(image_path, 'wb') as image_file:
                        image_file.write(response.read())
        except urllib.error.URLError as e:
            print(f"Error downloading image from {image_url}: {e}")
