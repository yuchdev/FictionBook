import os
import unittest
from fictionbook2.reader import Fb2Reader


class Fictionbook2ReaderTest(unittest.TestCase):

    TEST_ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

    def test_metadata(self):
        test_book_path = os.path.join(self.TEST_ASSETS_PATH, '2020_Sol_Invictus_Book1.fb2')
        expected_metadata = {
            'genre': 'prose_contemporary',
            'author': {'first-name': 'Виктор', 'middle-name': 'Олегович', 'last-name': 'Пелевин'},
            'book-title': 'Непобедимое солнце. Книга 1',
            'annotation': {
                'p': 'Какой стала Саша после встречи с тайной, вы узнаете из книги. Какой стала тайна после встречи с Сашей, вы уже немного в курсе и так.'
            },
            'keywords': 'постмодернизм,тайна,философская проза,духовные поиски,современное искусство',
            'date': '2020',
            'coverpage': {'image': ''},
            'lang': 'ru',
            'sequence': ''
        }
        expected_chapters = 2
        expected_paragraphs = 2596

        reader = Fb2Reader(test_book_path, images_dir='./images')
        reader.read()
        self.assertEqual(reader.metadata, expected_metadata)
        self.assertEqual(len(reader.chapters), expected_chapters)
        self.assertEqual(len(reader.paragraphs), expected_paragraphs)

    def test_images(self):
        test_book_path = os.path.join(self.TEST_ASSETS_PATH, '2020_Sol_Invictus_Book1.fb2')
        expected_cover_image = 'images/cover.jpg'

        reader = Fb2Reader(test_book_path, images_dir='./images')
        reader.read()
        self.assertEqual(reader.cover_image, expected_cover_image)


if __name__ == '__main__':
    unittest.main()
