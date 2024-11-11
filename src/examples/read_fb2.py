import sys
import argparse

from fictionbook.reader import Fb2Reader


def reader_example(file_path):
    # Example usage:
    reader = Fb2Reader(file_path, images_dir='./images')

    # Access extracted data
    print(f"Metadata:\n{reader.metadata}")
    print(f"Number of paragraphs: {len(reader.paragraphs)}")
    print(f"Cover image: {reader.cover}")
    if len(reader.paragraphs) < 10:
        print(f"Structure of body:\n{reader.body.to_yaml()}")
    print(f"Images:\n{reader.images}")

    # Write paragraphs to text file
    with open("output.txt", "w", encoding="utf-8") as f:
        for paragraph in reader.paragraphs:
            f.write(paragraph + "\n\n")


def main():
    parser = argparse.ArgumentParser(description="FB2 Book reader")
    parser.add_argument("file_path",
                        help="Path to the FB2 book file")
    parser.add_argument("--images-dir",
                        required=False,
                        default="images",
                        help="Directory to save the extracted images")
    args = parser.parse_args()

    file_path = args.file_path
    print(f"Reading {file_path}")
    reader_example(file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
