import reedsolo

class ReedSolomon:
    @staticmethod
    def encode_text_rs(bits, nsym):
        """
        Encodes bits using Reed-Solomon code.

        Parameters:
        bits (list[int]): List of bits to be encoded.
        nsym (int): Number of error correction symbols.

        Returns:
        list[int]: Encoded data as a list of bits.
        """
        # Convert bits to bytes
        byte_data = bytes(int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
        rs = reedsolo.RSCodec(nsym)
        encoded_data = rs.encode(byte_data)

        # Convert encoded bytes to bits
        encoded_bits = [int(bit) for byte in encoded_data for bit in format(byte, '08b')]
        return encoded_bits

    @staticmethod
    def decode_text_rs(encoded_bits, nsym):
        """
        Decodes bits using Reed-Solomon code.

        Parameters:
        encoded_bits (list[int]): List of encoded bits with error correction symbols.
        nsym (int): Number of error correction symbols.

        Returns:
        list[int]: Original data as a list of bits.
        """
        # Convert bits back to bytes
        encoded_data = bytes(int(''.join(map(str, encoded_bits[i:i + 8])), 2) for i in range(0, len(encoded_bits), 8))
        rs = reedsolo.RSCodec(nsym)
        decoded_data = rs.decode(encoded_data)[0]  # Returns a tuple, first element is the data

        # Convert decoded bytes back to bits
        decoded_bits = [int(bit) for byte in decoded_data for bit in format(byte, '08b')]
        return decoded_bits