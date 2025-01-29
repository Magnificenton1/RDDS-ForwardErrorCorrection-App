# FEC Transmission Simulation

This project simulates data transmission using various error correction codes and channel models. The main goal is to analyze the performance of different error correction codes over different channel conditions.

## Project Structure

```
project/
│
├── codes/
│   ├── __init__.py
│   ├── bch.py
│   ├── ldpc.py
│   └── reed_solomon.py
│
├── channels/
│   ├── __init__.py
│   ├── bsc.py
│   └── gilbert_elliott.py
│
├── simulation/
│   ├── __init__.py
│   └── simulate.py
│
└── main.py
```

## Requirements

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

## Usage

To run the data transmission simulation, execute the `main.py` script:

```sh
python main.py
```

## Modules

### Codes

- **BCH Code**: Implementation of BCH encoding and decoding.
- **LDPC Code**: Implementation of LDPC encoding and decoding.
- **Reed-Solomon Code**: Implementation of Reed-Solomon encoding and decoding.

### Channels

- **BSC Channel**: Binary Symmetric Channel model.
- **Gilbert-Elliott Channel**: Gilbert-Elliott Channel model.

### Simulation

- **simulate.py**: Manages the interaction between modules, runs simulations, and collects results.

## Example

Here is an example of how to use the simulation:

1. Get user input for the data to be transmitted.
2. Choose the transmission channel (BSC or Gilbert-Elliott).
3. Choose the error correction code (Reed-Solomon, Hamming, BCH, or LDPC).
4. Encode the data using the chosen error correction code.
5. Transmit the encoded data through the chosen channel.
6. Decode the received data.
7. Analyze the results, including the number of bit errors and the Bit Error Rate (BER).
