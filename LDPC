import numpy as np
from scipy.sparse import random as sparse_random, csr_matrix
from scipy.sparse.linalg import lsqr

class LDPC:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.H = sparse_random(n - k, n, density=0.1, format='csr', dtype=float).astype(int)
        self.G = self.generate_G(self.H)

    def generate_G(self, H):
        I_k = np.eye(self.k, dtype=int)
        P = H[:, :self.k].toarray()
        G = np.hstack((I_k, P.T))
        return G

    def encode(self, message):
        return np.dot(message, self.G) % 2

    def decode(self, received):
        received_sparse = csr_matrix(received)
        syndrome = (received_sparse.dot(self.H.T).toarray() % 2).flatten()
        if np.count_nonzero(syndrome) == 0:
            return received[:self.k]
        else:
            correction = lsqr(self.H, syndrome)[0]
            corrected = (received + correction) % 2
            return corrected[:self.k]
