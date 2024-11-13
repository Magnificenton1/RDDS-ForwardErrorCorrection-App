import reedsolo

class ReedSolomon:
    @staticmethod
    def encode_text_rs(bits, nsym):
        """
        Kodowanie bitów przy użyciu kodu Reed-Solomon.
        bits: list[int] - lista bitów do zakodowania
        nsym: int - liczba symboli kontrolnych (korekcji błędów)
        Zwraca zakodowane dane jako listę bitów.
        """
        # Konwersja bitów do bajtów
        byte_data = bytes(int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
        rs = reedsolo.RSCodec(nsym)
        encoded_data = rs.encode(byte_data)

        # Konwersja zakodowanych bajtów do bitów
        encoded_bits = [int(bit) for byte in encoded_data for bit in format(byte, '08b')]
        return encoded_bits

    @staticmethod
    def decode_text_rs(encoded_bits, nsym):
        """
        Dekodowanie bitów przy użyciu kodu Reed-Solomon.
        encoded_bits: list[int] - lista bitów zakodowanych z symbolami kontrolnymi
        nsym: int - liczba symboli kontrolnych (korekcji błędów)
        Zwraca oryginalne dane jako listę bitów.
        """
        # Konwersja bitów z powrotem do bajtów
        encoded_data = bytes(int(''.join(map(str, encoded_bits[i:i + 8])), 2) for i in range(0, len(encoded_bits), 8))
        rs = reedsolo.RSCodec(nsym)
        decoded_data = rs.decode(encoded_data)[0]  # Zwraca tuple, pierwszy element to dane

        # Konwersja zdekodowanych bajtów z powrotem do bitów
        decoded_bits = [int(bit) for byte in decoded_data for bit in format(byte, '08b')]
        return decoded_bits