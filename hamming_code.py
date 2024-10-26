import numpy as np


class HammingCode:
    """
    The HammingCode class implements encoding, error correction, and decoding
    of binary data using Hamming codes for various configurations.

    Attributes:
        m (int): Length of the data (number of information bits).
        n (int): Length of the code (total number of bits in the encoded word).
    """

    def __init__(self, m):
        """
        Initializes a HammingCode object based on the number of data bits.

        Args:
            m (int): Number of data bits, e.g., 4 for (7,4) code or 11 for (15,11).
        """
        self.m = m
        self.n = int(2 ** np.ceil(np.log2(m + np.ceil(np.log2(m)) + 1)) - 1)
        self.r = int(np.log2(self.n + 1))  # Number of parity bits

    def encode(self, data):
        """
        Encodes the given binary data using the Hamming code algorithm.

        Args:
            data (np.array): A numpy array containing the binary data (information bits).

        Returns:
            np.array: The encoded array of bits, including data and parity bits.
        """
        encoded_data = np.zeros(self.n, dtype=int)  # Initialize the encoded_data array with zeros

        # Place data bits in their respective positions
        bit_position = 0
        for bit in range(1, self.n + 1):
            if bit & (bit - 1) == 0: # Check if the bit position is a power of 2
                continue # Skip parity bit positions
            else:
                encoded_data[bit - 1] = data[bit_position]
                bit_position += 1

        # Calculate parity bits
        for i in range(self.r):
            parity_position = 2 ** i
            parity = 0

            # Calculate the parity for the current parity bit position
            for bit in range(1, self.n + 1):
                if bit & parity_position: # If j's binary representation includes the parity position
                    parity ^= encoded_data[bit - 1] # Make XOR of the bits

            # Set the parity bit in the encoded array
            encoded_data[parity_position - 1] = parity

        return encoded_data


    def decode(self, encoded_data):
        """
        Decodes the encoded binary data and corrects any single-bit errors.

        Args:
            encoded_data (np.array): A numpy array of encoded bits (data + parity bits).

        Returns:
            tuple: The original binary data after decoding and correcting errors, the number of detected errors
        """
        corrected_data, error_count = self.correct_error(encoded_data) # Correct any errors in the encoded data if possible

        if corrected_data is None: # If there are too many errors to correct
            return None, error_count

        # Extract the original data bits from the corrected encoded_data
        original_data = []
        for bit in range(1, self.n + 1):
            if bit & (bit - 1) == 0: # Skip parity bits
                continue
            else:
                original_data.append(corrected_data[bit - 1])

        return np.array(original_data), error_count


    def correct_error(self, encoded_data):
        """
        Detects and corrects single-bit errors in the encoded binary data.

        Args:
            encoded_data (np.array): A numpy array of encoded bits (data + parity bits).

        Returns:
            tuple: The encoded data with corrected errors and the number of detected errors.
        """
        error_position = 0  # Number of parity bits
        error_count = 0  # Number of detected errors

        # Check each parity bit
        for parity_bit in range(self.r):
            parity_position = 2 ** parity_bit
            parity = 0

            # Calculate the parity for the current parity bit position
            for bit in range(1, self.n + 1):
                if bit & parity_position:  # If j's binary representation includes the parity position
                    parity ^= encoded_data[bit - 1]  # Make XOR of the bits

            if parity != 0:  # If parity isn't' t zero, there must be an error
                error_position += parity_position
                error_count += 1

        if error_count == 1:  # If error_count is 1, make the single error correction (1-indexed position)
            encoded_data[error_position - 1] ^= 1
            return encoded_data, error_count
        elif error_count > 1:
            print("Multiple errors detected! Unable to correct data.")
            return None, error_count
        else:
            return encoded_data, error_count
