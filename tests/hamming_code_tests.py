import unittest
import numpy as np

from codes.hamming_code import HammingCode


class TestHammingCode(unittest.TestCase):

    def test_hamming_encode(self):
        """
        Tests whether the encode function correctly encodes binary data
        for a Hamming code.
        """
        # Test cases for encoding binary data into Hamming code
        test_cases = [
            (4, np.array([1, 0, 1, 1]), np.array([0, 1, 1, 0, 0, 1, 1])),  # 4-bit input
            (4, np.array([0, 1, 0, 1]), np.array([0, 1, 0, 0, 1, 0, 1])),  # 4-bit input
            (4, np.array([1, 1, 0, 0]), np.array([0, 1, 1, 1, 1, 0, 0])),  # 4-bit input
            (4, np.array([1, 0, 1, 0]), np.array([1, 0, 1, 1, 0, 1, 0])),  # 4-bit input
            (4, np.array([0, 0, 1, 1]), np.array([1, 0, 0, 0, 0, 1, 1])),  # 4-bit input
            (4, np.array([1, 1, 1, 1]), np.array([1, 1, 1, 1, 1, 1, 1])),  # 4-bit input
            (11, np.array([1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]), np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0])),  # 11-bit input
            (11, np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1]), np.array([0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1])),  # 11-bit input
            (11, np.array([0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1]), np.array([0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1])),  # 11-bit input
            (11, np.array([1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1]), np.array([0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1])),  # 11-bit input
        ]

        for m, data, expected_encoded in test_cases:
            hamming = HammingCode(m)
            encoded = hamming.encode(data)
            np.testing.assert_array_equal(encoded, expected_encoded)

    def test_hamming_decode_no_error(self):
        """
        Tests whether decoding works correctly when there are no errors in the encoded data.
        """
        # Test cases for decoding valid encoded data with no errors
        test_cases = [
            (4, np.array([0, 1, 1, 0, 0, 1, 1]), np.array([1, 0, 1, 1])),  # 4-bit input
            (4, np.array([0, 1, 0, 0, 1, 0, 1]), np.array([0, 1, 0, 1])),  # 4-bit input
            (4, np.array([0, 1, 1, 1, 1, 0, 0]), np.array([1, 1, 0, 0])),  # 4-bit input
            (4, np.array([1, 0, 1, 1, 0, 1, 0]), np.array([1, 0, 1, 0])),  # 4-bit input
            (4, np.array([1, 0, 0, 0, 0, 1, 1]), np.array([0, 0, 1, 1])),  # 4-bit input
            (4, np.array([1, 1, 1, 1, 1, 1, 1]), np.array([1, 1, 1, 1])),  # 4-bit input
            (11, np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0]), np.array([1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0])), # 11-bit input
            (11, np.array([0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1]), np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1])), # 11-bit input
            (11, np.array([0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1]), np.array([0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1])), # 11-bit input
            (11, np.array([0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1]), np.array([1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1])), # 11-bit input
        ]

        for m, encoded_data, expected_decoded in test_cases:
            hamming = HammingCode(m)
            decoded = hamming.decode(encoded_data)
            np.testing.assert_array_equal(decoded, expected_decoded)

    def test_hamming_correct_error(self):
        """
        Tests the detection and correction of a single error in the encoded data.
        """
        # Test cases for correcting a single-bit error in encoded data
        test_cases = [
            (4, np.array([1, 0, 1, 0, 0, 1, 1]), np.array([0, 0, 1, 1])),  # Error introduced in 4-bit word
            (4, np.array([0, 0, 1, 1, 0, 1, 1]), np.array([1, 0, 0, 1])),  # Error introduced in 4-bit word
            (4, np.array([1, 1, 1, 0, 1, 1, 1]), np.array([1, 1, 1, 1])),  # Error introduced in 4-bit word
            (4, np.array([1, 0, 0, 1, 0, 1, 1]), np.array([0, 0, 1, 1])),  # Error introduced in 4-bit word
            (11, np.array([1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0]), np.array([0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0])),  # Error introduced in 11-bit word
            (11, np.array([1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1]), np.array([1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1])),  # Error introduced in 11-bit word
            (11, np.array([1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]), np.array([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1])),  # Error introduced in 11-bit word
            (11, np.array([1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1]), np.array([0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1])),  # Error introduced in 11-bit word
        ]

        for m, encoded_data, expected_corrected in test_cases:
            hamming = HammingCode(m)
            corrected_data = hamming.decode(encoded_data)
            np.testing.assert_array_equal(corrected_data, expected_corrected)


if __name__ == '__main__':
    unittest.main()
