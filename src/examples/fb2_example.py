import os.path
import sys
import argparse
import json

from fictionbook.writer import Fb2Writer
from fictionbook.reader import Fb2Reader


def reader_example(file_path):
    # Example usage:
    reader = Fb2Reader(file_path, images_dir='./images')

    # Access extracted data
    print("Metadata: ", reader.metadata)
    print("Cover Image: ", reader.cover)
    print("Total chapters: ", len(reader.paragraphs))

    # Length of paragraphs may be different from the length of subchapters
    print("Total paragraphs: ", len(reader.paragraphs))


def writer_example(file_path):
    asset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "test", "assets"))
    test_json = os.path.abspath(os.path.join(asset_dir, "sol_invictus_en.fb2.json"))

    with open(test_json, "r") as f:
        data = json.load(f)
        metadata = data["description"]
        body = data["body"]
        items = body[1]['section']

        # Split the list over elements with the key "empty-line"
        paragraphs = []
        temp_paragraphs = []
        for item in items:
            if 'empty-line' in item:
                if temp_paragraphs:
                    paragraphs.append(temp_paragraphs)
                    temp_paragraphs = []
            elif 'p' in item:
                temp_paragraphs.append(item['p'])
        if temp_paragraphs:
            paragraphs.append(temp_paragraphs)

    writer = Fb2Writer(file_name=file_path, images_dir="./images")
    writer.set_metadata(metadata)
    writer.set_paragraphs(paragraphs)
    writer.write(debug_mode=True, pretty_xml=True)


def main():
    parser = argparse.ArgumentParser(description="FB2 Book reader")
    parser.add_argument("--mode", help="Mode of operation", choices=["read", "write"], default="read")
    parser.add_argument("--file-path", help="Path to the FB2 book file")
    parser.add_argument("--images-dir", help="Directory to save the extracted images", default="images")
    args = parser.parse_args()

    file_path = args.file_path
    if args.mode == "read":
        print(f"Reading {file_path}")
        reader_example(file_path)
    elif args.mode == "write":
        print(f"Writing {file_path}")
        writer_example(file_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
