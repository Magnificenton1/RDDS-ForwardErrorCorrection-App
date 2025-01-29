import unittest
import numpy as np
from codes.BCH_code import BCHCode


class TestBCHCode(unittest.TestCase):
    def setUp(self):
        # Initialize BCH parameters (n=15, k=5, t=3)
        self.bch = BCHCode(n=15, k=5, t=3)

    def test_encode(self):
        """
        Tests if BCH code correctly encodes data into a 15-bit codeword.
        """
        data = np.array([1, 0, 1, 0, 1], dtype=int)  # Example input data (5 bits)
        encoded_data = self.bch.encode(data)
        # Check the length of the encoded data (should be 15 bits)
        self.assertEqual(len(encoded_data), 15)
        print(f"Encoded data: {encoded_data}")

    def test_decode_without_error(self):
        """
        Tests if BCH code correctly decodes data without errors.
        """
        data = np.array([1, 0, 1, 0, 1], dtype=int)  # Example input data
        encoded_data = self.bch.encode(data)  # Encode the data

        # Decode the data without introducing any errors
        decoded_data = self.bch.decode(encoded_data)
        # The decoded data should match the original data
        np.testing.assert_array_equal(decoded_data, data)
        print(f"Decoded data (no errors): {decoded_data}")

    def test_decode_with_single_error(self):
        """
        Tests if BCH code correctly detects and corrects a single error in the data.
        """
        data = np.array([1, 0, 1, 0, 1], dtype=int)
        encoded_data = self.bch.encode(data)  # Encode the data

        # Introduce a single error in the encoded data
        encoded_data_with_error = np.copy(encoded_data)
        encoded_data_with_error[3] = 1 - encoded_data_with_error[3]  # Flip one bit

        # Decode the data with the error
        decoded_data = self.bch.decode(encoded_data_with_error)
        # The decoded data should match the original data
        np.testing.assert_array_equal(decoded_data, data)
        print(f"Decoded data (with single error): {decoded_data}")

    def test_decode_with_double_error(self):
        """
        Tests if BCH code correctly detects errors in the case of multiple errors in the data.
        """
        data = np.array([1, 0, 1, 0, 1])  # Original data
        encoded_data = self.bch.encode(data)  # Encode the data

        # Introduce two errors by flipping bits at positions 1 and 3
        encoded_data_with_errors = encoded_data.copy()
        encoded_data_with_errors[1] = 1 - encoded_data_with_errors[1]  # Flip bit at position 1
        encoded_data_with_errors[3] = 1 - encoded_data_with_errors[3]  # Flip bit at position 3

        # Decode the data
        decoded_data = self.bch.decode(encoded_data_with_errors)
        self.assertEqual(decoded_data.tolist(), data.tolist())


if __name__ == '__main__':
    unittest.main()
