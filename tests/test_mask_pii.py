import unittest
import re
from minicahe.compressor import Compressor

class TestMaskPII(unittest.TestCase):
    def setUp(self):
        self.compressor = Compressor(mask_pii=True)

    def test_emails(self):
        cases = [
            ("Contact test@example.com for help.", "Contact [EMAIL] for help."),
            ("My email is foo.bar+baz@sub.domain.co.uk.", "My email is [EMAIL]."),
            ("Email: admin@site.org, test@site.net", "Email: [EMAIL], [EMAIL]"),
        ]
        for original, expected in cases:
            self.assertEqual(self.compressor.compress(original), expected)

    def test_phones_and_cards(self):
        cases = [
            ("Call me at 123-456-7890 tomorrow.", "Call me at [REDACTED] tomorrow."),
            ("My card is 1234 5678 1234 5678.", "My card is [REDACTED]."),
            ("Phone: (123) 456-7890", "Phone: [REDACTED]"),
            ("No spaces: 12345678901234", "No spaces: [REDACTED]"),
        ]
        for original, expected in cases:
            self.assertEqual(self.compressor.compress(original), expected)

if __name__ == '__main__':
    unittest.main()
