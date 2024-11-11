import os
import re
import sys
import json
import argparse

from pypdf import PdfReader
from fictionbook.writer import Fb2Writer


def process_page_text(page_text, page_number, preserve_references, references_dict):
    """
    Process the text of a single page to remove or preserve references.
    :param page_text: Text of the page
    :param page_number: Page number
    :param preserve_references: Boolean flag to preserve references
    :param references_dict: Dictionary to store references if preserve_references is True
    :return: Processed page text
    """
    matches = re.findall(r'\b\w+\d\b', page_text)
    for match in matches:
        # Find the reference text starting with the same number from the end of the page text
        ref_pattern = re.compile(r'\b' + re.escape(match[-1]) + r' \w+\b')
        ref_match = ref_pattern.search(page_text[::-1])
        if ref_match:
            ref_match = ref_pattern.search(page_text, len(page_text) - ref_match.end())
            if preserve_references:
                position = (page_number, page_text.find(match))
                references_dict[position] = ref_match.group()
            # Replace only the reference index with an empty string
            page_text = page_text.replace(match, match[:-1])
            page_text = page_text.replace(ref_match.group(), '')
    return page_text


def extract_text(file_path, preserve_references=False):
    """
    Extract text from a PDF file
    :param file_path: Path to the PDF file
    :param preserve_references: Boolean flag to preserve references
    :return: Extracted text without references or references dictionary
    """
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    print(f"Number of pages: {number_of_pages}")
    text = ""
    references_dict = {}

    for page_number, page in enumerate(reader.pages):
        page_text = page.extract_text()
        processed_text = process_page_text(page_text, page_number, preserve_references, references_dict)
        text += processed_text

    if preserve_references:
        with open('references.json', 'w', encoding='utf-8') as f:
            json.dump(references_dict, f, ensure_ascii=False, indent=4)
        return references_dict
    else:
        return text


def process_extracted_text(text):
    """
    Extract paragraphs from the text
    The sequence '{EndOfSentenceSymbol}\n{AnySymbol}' is considered as a paragraph separator,
    :param text: Text extracted from PDF
    :return: list of paragraphs
    """
    paragraphs = []
    paragraph = ""
    i = 0
    while i < len(text):
        # Check if the current character is an end of sentence symbol
        # and the next two characters form the sequence '\n{AnySymbol}'
        if i < len(text) - 2 and text[i] in {'.', '?', '!'} and text[i+1] == '\n' and text[i+2].isprintable():
            paragraph += text[i]
            paragraphs.append(paragraph)
            paragraph = ""

            # Skip the next two characters
            i += 2
        else:
            # Add the current character to paragraph
            paragraph += text[i]
            i += 1
    # Add the last paragraph if it's not empty
    if paragraph:
        paragraphs.append(paragraph)

    # Post-process each paragraph to remove redundant newline characters
    for i in range(len(paragraphs)):
        paragraphs[i] = paragraphs[i].replace('\n', ' ')

    return paragraphs


def main():
    parser = argparse.ArgumentParser(description="FB2 Book reader")
    parser.add_argument("--extract-text",
                        help="Extract PDF text and save it to text file")
    parser.add_argument("--output-file",
                        default="output.txt",
                        help="Path to the text file")
    parser.add_argument("--split-paragraphs",
                        action="store_true",
                        help="Split the extracted text into paragraphs")
    parser.add_argument("--to-fb2",
                        help="Convert list of paragraphs to FB2 file")
    args = parser.parse_args()

    if args.extract_text:
        file_path = args.extract_text
        text = extract_text(file_path)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(text)

    if args.split_paragraphs:
        with open(args.output_file, "r", encoding="utf-8") as f:
            text = f.read()
            paragraphs = process_extracted_text(text)
            with open("temp.txt", "w", encoding="utf-8") as f:
                for paragraph in paragraphs:
                    f.write(paragraph + "\n\n")

    if os.path.isfile('temp.txt'):
        # read paragraphs from temp file
        with open('temp.txt', 'r', encoding='utf-8') as f:
            paragraphs = f.readlines()
            paragraphs = [p.strip('\n\n') for p in paragraphs]
        # remove empty lines
        paragraphs = [p for p in paragraphs if p]
    else:
        print("ERROR: No paragraphs found")
        return 1

    if args.to_fb2:
        writer = Fb2Writer(file_name=args.to_fb2, images_dir="./Invasive_Species")
        writer.set_metadata({
            "title-info": {
                "book-title": "Инвазивные виды",
                "author": "Джордж Райт",
                "keywords": "фантастика,инвазия,война,человечество,технологии,будущее,космос,планеты,хоррор,пришельцы",
                "date": "2019-01-01",
                "lang": "ru"
            }
        })
        writer.set_paragraphs(paragraphs)
        writer.write(debug_mode=True, pretty_xml=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
