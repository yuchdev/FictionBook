import os.path
import sys
import argparse
import json
from pypdf import PdfReader

from fictionbook.writer import Fb2Writer


def extract_text(file_path):
    """
    Extract text from a PDF file
    :param file_path:
    :return:
    """
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    print(f"Number of pages: {number_of_pages}")
    text = ""
    for page in reader.pages:
        text += page.extract_text()
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
            # Add the end of sentence symbol to the paragraph,
            # then add the paragraph to paragraphs and reset paragraph
            paragraph += text[i]
            paragraphs.append(paragraph)
            paragraph = ""
            i += 2  # Skip the next two characters
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
        with open(args.output_file, "w") as f:
            f.write(text)

    if args.split_paragraphs:
        with open(args.output_file, "r") as f:
            text = f.read()
            paragraphs = process_extracted_text(text)
            # write list to temp file
            with open("temp.txt", "w") as f:
                for paragraph in paragraphs:
                    f.write(paragraph + "\n\n")

    if os.path.isfile('temp.txt'):
        # read paragraphs from temp file
        with open('temp.txt', 'r') as f:
            paragraphs = f.readlines()
            paragraphs = [p.strip('\n\n') for p in paragraphs]
        # remove empty lines
        paragraphs = [p for p in paragraphs if p]

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
