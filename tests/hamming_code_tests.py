import unittest
import numpy as np
from hamming_code import HammingCode


class TestHammingCode(unittest.TestCase):

    def test_hamming_encode(self):
        """
        Tests whether the encode function correctly encodes binary data
        for a Hamming code.
        """
        hamming = HammingCode(m=4)
        data = np.array([1, 0, 1, 1])
        encoded = hamming.encode(data)
        # Expected data after encoding (e.g., for Hamming (7,4) code)
        expected_encoded = np.array([1, 0, 1, 1, 0, 1, 1])
        np.testing.assert_array_equal(encoded, expected_encoded)
        #TODO: Add more test cases

    def test_hamming_decode_no_error(self):
        """
        Tests whether decoding works correctly when there are no errors in the encoded data.
        """
        hamming = HammingCode(m=4)
        encoded_data = np.array([1, 0, 1, 1, 0, 1, 1])
        decoded = hamming.decode(encoded_data)
        expected_decoded = np.array([1, 0, 1, 1])
        np.testing.assert_array_equal(decoded, expected_decoded)
        #TODO: Add more test cases

    def test_hamming_correct_error(self):
        """
        Tests the detection and correction of a single error in the encoded data.
        """
        hamming = HammingCode(m=4)
        encoded_data = np.array([1, 0, 1, 0, 0, 1, 1])  # Error at position 4
        corrected_data = hamming.correct_error(encoded_data)
        # Expected data after error correction
        expected_corrected = np.array([1, 0, 1, 1, 0, 1, 1])
        np.testing.assert_array_equal(corrected_data, expected_corrected)
        #TODO: Add more test cases


if __name__ == '__main__':
    unittest.main()
