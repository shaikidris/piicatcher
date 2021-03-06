from unittest import TestCase

from piicatcher.scanner import RegexScanner, NERScanner
from piicatcher.piitypes import PiiTypes


class RegexTestCase(TestCase):
    def setUp(self):
        self.parser = RegexScanner()

    def test_phones(self):
        matching = ["12345678900", "1234567890", "+1 234 567 8900", "234-567-8900",
                    "1-234-567-8900", "1.234.567.8900", "5678900", "567-8900",
                    "(123) 456 7890", "+41 22 730 5989", "(+41) 22 730 5989",
                    "+442345678900"]
        for text in matching:
            self.assertEqual(self.parser.scan(text), [PiiTypes.PHONE])

    def test_emails(self):
        matching = ["john.smith@gmail.com", "john_smith@gmail.com", "john@example.net"]
        non_matching = ["john.smith@gmail..com"]
        for text in matching:
            self.assertEqual(self.parser.scan(text), [PiiTypes.EMAIL])
        for text in non_matching:
            self.assertEqual(self.parser.scan(text), [])

    def test_creditcards(self):
        matching = ["0000-0000-0000-0000", "0123456789012345",
                    "0000 0000 0000 0000", "012345678901234"]
        for text in matching:
            self.assertTrue(PiiTypes.CREDIT_CARD in self.parser.scan(text))

    def test_street_addresses(self):
        matching = ["checkout the new place at 101 main st.",
                    "504 parkwood drive", "3 elm boulevard",
                    "500 elm street "]
        non_matching = ["101 main straight"]

        for text in matching:
            self.assertEqual(self.parser.scan(text), [PiiTypes.ADDRESS])
        for text in non_matching:
            self.assertEqual(self.parser.scan(text), [])


class NERTests(TestCase):
    def setUp(self):
        self.parser = NERScanner()

    def test_person(self):
        types = self.parser.scan("Jonathan is in the office")
        self.assertTrue(PiiTypes.PERSON in types)

    def test_location(self):
        types = self.parser.scan("Jonathan is in Bangalore")
        self.assertTrue(PiiTypes.LOCATION in types)
