import sys
import argparse

from fictionbook2.writer import Fb2Writer
from fictionbook2.reader import Fb2Reader


def reader_example(file_path):
    # Example usage:
    reader = Fb2Reader(file_path, images_dir='./images')
    reader.read()

    # Access extracted data
    print("Metadata: ", reader.metadata)
    print("Cover Image: ", reader.cover_image)
    print("Chapters: ", reader.chapters)


def writer_example(file_path):
    # Example usage:
    metadata = {
        "title-info": {
            "genre": "prose_contemporary",
            "author": {
                "first-name": "John",
                "last-name": "Doe",
                "home-page": "https://example.com"
            },
            "book-title": "Book Title",
            "annotation": "Book Annotation",
            "keywords": "book, keywords",
            "date": "2021",
            "lang": "en"
        },
        "document-info": {
            "author": "John Doe",
            "program-used": "Python fictionbook2 library",
            "date": "2021",
            "src-url": "https://example.com",
            "id": "123456789",
            "version": "1.0"
        },
        "publish-info": {
            "book-name": "Book Name",
            "publisher": "Publisher",
            "city": "City",
            "year": "2021",
            "isbn": "1234567890"
        }
    }
    chapters = [
        {
            "title": "Chapter 1",
            "paragraphs": ["Chapter 1 Text 1", "Chapter 1 Text 2"]
        }
    ]
    writer = Fb2Writer(file_name=file_path)
    writer.write(metadata=metadata, chapters=chapters, cover="cover.jpg")


def main():
    parser = argparse.ArgumentParser(description="FB2 Book readr")
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
