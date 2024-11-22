import galois
import numpy as np

class BCHCode:
    def __init__(self, n, k, t):
        """
        Initialize the BCH code parameters.

        Args:
            n (int): Length of the codeword.
            k (int): Length of the message (information bits).
            t (int): Error correction capability (number of errors that can be corrected).
        """
        self.n = n  # Length of the codeword
        self.k = k  # Length of the message (number of information bits)
        self.t = t  # Error correction capability
        self.galois_field = galois.GF(2)  # GF(2) field for binary operations

        self.bch = galois.BCH(n=self.n, k=self.k, field=self.galois_field)

    def encode(self, data):
        """
        Encodes the given binary data using the BCH code algorithm.

        Args:
            data (np.array): A numpy array containing the binary data (information bits).

        Returns:
            np.array: The encoded array of bits, including data and parity bits.
        """
        """
            Encodes the given binary data using the BCH code algorithm.
            """
        # Convert the input data to a Galois field element
        data_poly = galois.Poly(data, field=self.galois_field)

        # Get the coefficients from the polynomial and encode the data
        encoded_data = self.bch.encode(data_poly.coeffs)

        # Return the encoded data as a numpy array or list
        return np.array(encoded_data)

    def decode(self, encoded_data):
        """
        Decodes the encoded data using the BCH code algorithm.
        """
        # Convert the input data to a Galois field element (if it's not already)
        encoded_poly = galois.Poly(encoded_data, field=self.galois_field)

        # Get the coefficients from the polynomial and decode the data
        decoded_data = self.bch.decode(encoded_poly.coeffs)

        # Return the decoded data
        return np.array(decoded_data)

