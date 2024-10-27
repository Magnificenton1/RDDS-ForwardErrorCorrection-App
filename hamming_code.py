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
        r = 1
        # Calculate the number of parity bits `r` such that 2^r >= m + r + 1
        while 2 ** r < m + r + 1:
            r += 1

        self.r = r
        self.n = m + r  # Total bits = data bits + parity bits

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
            np.array: The original binary data after decoding and correcting errors
        """
        corrected_data = self.correct_error(encoded_data) # Correct any errors in the encoded data if possible

        if corrected_data is None: # If there are too many errors to correct
            return encoded_data
        # Extract the original data bits from the corrected encoded_data
        original_data = []
        for bit in range(1, self.n + 1):
            if bit & (bit - 1) == 0: # Skip parity bits
                continue
            else:
                original_data.append(corrected_data[bit - 1])

        return np.array(original_data)


    def correct_error(self, encoded_data):
        """
        Detects and corrects single-bit errors in the encoded binary data.

        Args:
            encoded_data (np.array): A numpy array of encoded bits (data + parity bits).

        Returns:
            np.array: The encoded data with corrected errors.
        """
        error_position = 0  # 1-indexed position of the error

        # Check each parity bit
        for parity_bit in range(self.r):
            parity_position = 2 ** parity_bit
            calculated_parity = 0

            # Calculate the parity for the current parity bit position
            for bit in range(1, self.n + 1):
                if bit & parity_position:  # If j's binary representation includes the parity position
                    if (bit - 1) != (parity_position - 1):  # Exclude parity bit
                        calculated_parity ^= encoded_data[bit - 1]  # Make XOR of the bits

            if calculated_parity != encoded_data[parity_position - 1]:  # Compare the calculated parity with the encoded parity bit
                error_position += parity_position

        if error_position == 0: # No errors detected
            return encoded_data
        elif 1 <= error_position <= self.n:  # If an error position is found, attempt to correct
            encoded_data[error_position - 1] ^= 1
            return encoded_data
        else:   # Error position is out of bounds, meaning too many errors
            return None