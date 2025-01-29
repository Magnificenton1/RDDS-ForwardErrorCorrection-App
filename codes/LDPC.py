import numpy as np
from scipy.sparse import random as sparse_random, csr_matrix
from scipy.sparse.linalg import lsqr

class LDPC:
    """
    The LDPC class implements encoding and decoding of binary data using Low-Density Parity-Check codes.

    Attributes:
        n (int): Length of the code (total number of bits in the encoded word).
        k (int): Length of the data (number of information bits).
        H (csr_matrix): Parity-check matrix.
        G (np.array): Generator matrix.
    """

    def __init__(self, n, k):
        """
        Initializes an LDPC object with the given code length and data length.

        Args:
            n (int): Length of the code (total number of bits in the encoded word).
            k (int): Length of the data (number of information bits).
        """
        self.n = n
        self.k = k
        self.H = sparse_random(n - k, n, density=0.1, format='csr', dtype=float).astype(int)
        self.G = self.generate_G(self.H)

    def generate_G(self, H):
        """
        Generates the generator matrix G from the parity-check matrix H.

        Args:
            H (csr_matrix): Parity-check matrix.

        Returns:
            np.array: Generator matrix.
        """
        I_k = np.eye(self.k, dtype=int)
        P = H[:, :self.k].toarray()
        G = np.hstack((I_k, P.T))
        return G

    def encode(self, message):
        """
        Encodes the given binary message using the LDPC code.

        Args:
            message (np.array): A numpy array containing the binary data (information bits).

        Returns:
            np.array: The encoded array of bits.
        """
        return np.dot(message, self.G) % 2

    def decode(self, received):
        """
        Decodes the received binary data and corrects errors using the LDPC code.

        Args:
            received (np.array): A numpy array of received bits (data + parity bits).

        Returns:
            np.array: The original binary data after decoding and correcting errors.
        """
        received_sparse = csr_matrix(received)
        syndrome = (received_sparse.dot(self.H.T).toarray() % 2).flatten()
        if np.count_nonzero(syndrome) == 0:
            return received[:self.k]
        else:
            correction = lsqr(self.H, syndrome)[0]
            corrected = (received + correction) % 2
            return corrected[:self.k]