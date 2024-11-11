import sys
import argparse
import json

from fictionbook.writer import Fb2Writer


def writer_example(json_content_file, result_file_path):
    with open(json_content_file, "r") as f:
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

    writer = Fb2Writer(file_name=result_file_path, images_dir="./images")
    writer.set_metadata(metadata)
    writer.set_paragraphs(paragraphs, 'plaintext')
    writer.write(debug_mode=True, pretty_xml=True)


def main():
    parser = argparse.ArgumentParser(description="FB2 Book reader")
    parser.add_argument("--input-file",
                        help="Path to JSON file with the content of the book")
    parser.add_argument("--output-file",
                        help="Path to the FB2 book file")
    parser.add_argument("--images-dir",
                        help="Directory to save the extracted images",
                        default="images")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    print(f"Writing FB2 book from {input_file} to {output_file}")
    writer_example(json_content_file=input_file, result_file_path=output_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
