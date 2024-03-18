import sys
import argparse

from fictionbook.reader import Fb2Reader


def reader_example(file_path):
    # Example usage:
    reader = Fb2Reader(file_path, images_dir='./images')

    # Access extracted data
    print("Metadata: ", reader.metadata)
    print("Body: ", reader.body)
    print("Cover Image: ", reader.cover)
    print("Total paragraphs: ", len(reader.body))


def main():
    parser = argparse.ArgumentParser(description="FB2 Book reader")
    parser.add_argument("--file-path", help="Path to the FB2 book file")
    parser.add_argument("--images-dir", help="Directory to save the extracted images", default="images")
    args = parser.parse_args()

    file_path = args.file_path
    print(f"Reading {file_path}")
    reader_example(file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
