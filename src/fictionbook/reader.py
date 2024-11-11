# -*- coding: utf-8 -*-
import os
import base64
import urllib.request
import xml.etree.ElementTree as et


class Fb2Reader:
    """
    FictionBook2 reader
    """

    def __init__(self, file_path: str, images_dir: str, download_images=False):
        """
        :param file_path:
        :param images_dir:
        :param download_images:
        """
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not isinstance(images_dir, str):
            raise TypeError("images_dir must be a string")
        self.file_path = file_path
        self.images_dir = images_dir
        self.root = None
        self.metadata = None
        self.body = None
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

    @property
    def paragraphs(self):
        """
        Collect all paragraphs from the body.
        Iterate body recursively and collect all paragraphs, including nested tags.
        :return: list of paragraphs
        """
        if self.body is None:
            return []

        paragraphs = []
        for p in self.body.findall('.//{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
            text_content = ''.join(p.itertext())
            if text_content:
                paragraphs.append(text_content.strip())

        return paragraphs

    def _read(self, download_images=False):
        tree = et.parse(self.file_path)
        self.root = tree.getroot()

        self._extract_metadata()
        self._extract_body()
        self._extract_binary()
        if download_images:
            self._download_images()

    def _extract_metadata(self):
        """
        Extract metadata ('description' tag) recursively from the root element
        """
        self.metadata = self.root.find('{http://www.gribuser.ru/xml/fictionbook/2.0}description')
        if self.metadata is None:
            raise ValueError("Metadata not found")
        self.cover_image = self._extract_cover()

    def _extract_body(self):
        """
        Extract body recursively from the root element
        """
        self.body = self.root.find('{http://www.gribuser.ru/xml/fictionbook/2.0}body')
        if self.body is None:
            raise ValueError("Body not found")

    def _extract_binary(self):
        """
        Extract all <binary> elements from root
        """
        binary_elements = self.root.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}binary')
        for binary in binary_elements:
            binary_id = binary.get('id')
            binary_content = binary.text
            binary_content_type = binary.get('content-type')
            if binary_id and binary_content:
                self._save_image(binary_content, binary_content_type, binary_id)

    def _extract_cover(self):
        """
        Find the first coverpage element, extract first image element and get the href attribute
        Trim '#' prefix if present
        """
        # Navigate to 'title-info/coverpage/image'
        title_info = self.metadata.find('{http://www.gribuser.ru/xml/fictionbook/2.0}title-info')
        if title_info is None:
            return None
        coverpage = title_info.find('{http://www.gribuser.ru/xml/fictionbook/2.0}coverpage')
        if coverpage is None:
            return None
        cover_image = coverpage.find('{http://www.gribuser.ru/xml/fictionbook/2.0}image')
        if cover_image is None:
            return None
        href = cover_image.get('{http://www.w3.org/1999/xlink}href')
        if href and href.startswith('#'):
            href = href[1:]
        return href

    def _download_images(self):
        """
        Download images from the book if <image l:href="http..."> tag is used
        and points to a URL on the internet
        Note: Images may repeat so we use set() to avoid duplicates
        """
        images = set()
        image_elements = self.root.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image")
        for image_elem in image_elements:
            href_attr = image_elem.get('{http://www.w3.org/1999/xlink}href', '')
            if href_attr.startswith("http"):
                images.add(href_attr)
        # Download images
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

    def _save_image(self, image_data, content_type, image_id):
        image_extension = content_type.split("/")[-1]
        image_name, ext = os.path.splitext(image_id)

        if not ext:
            ext = f".{image_extension.lower()}"

        image_path = os.path.abspath(os.path.join(self.images_dir, image_name + ext))

        with open(image_path, 'wb') as image_file:
            image_file.write(base64.b64decode(image_data))

