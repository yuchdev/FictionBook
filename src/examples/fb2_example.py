import sys
import argparse

from fictionbook2.writer import Fb2Writer
from fictionbook2.reader import Fb2Reader


def reader_example(file_path):

    # Example usage:
    reader = Fb2Reader(file_path, images_dir='./images')

    # Access extracted data
    print("Metadata: ", reader.metadata)
    print("Cover Image: ", reader.cover)
    print("Total chapters: ", len(reader.chapters))

    # Calculate and print the length of subchapters
    print("Total subchapters: ", sum(len(chapter) for chapter in reader.chapters))

    # Length of paragraphs may be different from the length of subchapters
    print("Total paragraphs: ", len(reader.paragraphs))


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
            "paragraphs": [
                "I decided to face my thirtieth birthday, riding down the highway on a motorcycle.",
                "I love all kinds of symbolism. I mean, when life rhymes. "
                "It even seems to me that these rhymes can be forged — this is a kind of magic called sympathetic, "
                "and it's very sympathetic to me. We sort of explain to the thick-assed, clumsy fate "
                "what we want her to look like, and sometimes she takes the hint.",
                "But not always, which I'll come back to soon."
            ]
        },
        {
            "title": "Chapter 2",
            "paragraphs": [
                "Daddy showed up — probably, he sensed that I was thinking about his pasta. "
                "He even came to my house. At first, I couldn't understand what it was all of a sudden, "
                "until he said it himself. Thirty years. Well, yeah, the anniversary.",
                "He didn't notice my birthdays before. But after all, "
                "a businessman is mainly interested in the zeros to the right of the digit. "
                "There were no zeros for a long time.",
                "'Whose paintings are these?' he asked from the doorway. 'What huge ones. Yours?'"
            ]
        }
    ]
    writer = Fb2Writer(file_name=file_path, images_dir="./images")
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
