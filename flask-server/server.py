from flask import Flask, jsonify, request
from collections import Counter
import heapq
import math

app = Flask(__name__)


# CODE FROM KAREEM

def probability(message):
    frequencies = {}
    for char in message:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    message_length = len(message)
    prob = {}
    for key, frequency in frequencies.items():
        prob[key] = frequency / message_length
    return prob


def average_length(message):
    frequencies = {}
    for char in message:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    result = 0
    message_length = len(message)
    for key, frequency in frequencies.items():
        probability = frequency / message_length
        result += probability * len(str(key))
    return result


def compression_ratio(original_data, compressed_data, compression_type):
    global original_size_h, original_size
    if compression_type == "Huffman":  # can work for GOLOMB in some examples
        if isinstance(original_data, str):
            # Assuming 8 bits per character
            original_size_h = len(original_data) * 8
        elif isinstance(original_data, int):
            # Assuming binary representation
            original_size_h = len(bin(original_data)) - 2
        if isinstance(compressed_data, list):
            # Sum of lengths of each code
            compressed_size_h = sum(len(str(code)) for code in compressed_data)
        else:
            # Assuming it's already a binary string
            compressed_size_h = len(compressed_data)
        return original_size_h / compressed_size_h if compressed_size_h > 0 else 0
    elif compression_type == "RLE":
        original_size_r = len(original_data) * 8
        letters, numbers = zip(*compressed_data)
        compressed_size_r = len(compressed_data) * \
            (8 + math.ceil(math.log2(max(numbers) + 1)))
        return original_size_r / compressed_size_r
    elif compression_type == "LZW":  # can work for GOLOMB in some examples
        if isinstance(original_data, str):
            # Assuming 8 bits per character
            original_size = len(original_data) * 8
        elif isinstance(original_data, int):
            # Assuming 8 bits per character
            original_size = len(original_data) * len(bin(original_data)) - 2
        compressed_size = len(compressed_data) * (
            len(bin(max(compressed_data))) - 2)  # Assuming its binary bits per code (for simplicity)
        return original_size / compressed_size
    elif compression_type == "AE" or compression_type == "Golomb":
        return "Out of the course scope"


def calculate_entropy(message):
    # Calculate the frequency of each character
    frequencies = {}
    for char in message:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    # Calculate the entropy
    entropy = 0
    message_length = len(message)
    for frequency in frequencies.values():
        probability = frequency / message_length
        entropy -= probability * math.log2(probability)

    return entropy


class LZW:
    def __init__(self, ascii_limit):
        # HOW MUCH ASCII YOU WANT
        self.ascii_limit = ascii_limit

    @staticmethod
    def lzw_compress(data):
        dictionary = {chr(i): i for i in range(127)}
        next_code = 128
        result = []
        current_sequence = ""

        for char in data:
            new_sequence = current_sequence + char
            if new_sequence in dictionary:
                current_sequence = new_sequence
            else:
                result.append(dictionary[current_sequence])
                dictionary[new_sequence] = next_code
                next_code += 1
                current_sequence = char

        if current_sequence:
            result.append(dictionary[current_sequence])

        return result

    def lzw_decompress(self, compressed_data):
        dictionary = {i: chr(i) for i in range(127)}
        next_code = 128
        result = []
        previous_code = compressed_data[0]
        result.append(dictionary[previous_code])
        previous_entry = dictionary[previous_code]

        for code in compressed_data[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = previous_entry + previous_entry[0]
            else:
                raise ValueError("Bad compressed sequence")

            result.append(entry)
            dictionary[next_code] = previous_entry + entry[0]
            next_code += 1
            previous_entry = entry

        return ''.join(result)


class GolombCodec:
    def __init__(self, m):
        self.m = m  # Golomb parameter

    def encode(self, n):
        q, r = divmod(n, self.m)
        unary_code = "1" * q + "0"

        b = math.ceil(math.log2(self.m))
        if r < pow(2, b) - self.m:
            b = b - 1
        binary_representation = bin(r)[2:]
        binary_length = len(binary_representation)
        padding = '0' * (b - binary_length)
        binary_code = str(padding + binary_representation)

        return unary_code + binary_code

    def decode(self, bitstream):
        q_length = bitstream.find("0") + 1
        q = len(bitstream[:q_length]) - 1
        r = int(bitstream[q_length:], 2)  # Corrected this line
        value = q * self.m + r
        return value


class ArithmeticCodec:
    def __init__(self):
        self.symbol_probabilities = {}

    def calculate_symbol_probabilities(self, text):
        symbol_counts = {}
        for symbol in text:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        total_symbols = len(text)
        for symbol, count in symbol_counts.items():
            self.symbol_probabilities[symbol] = count / total_symbols

    def encode(self, text):
        self.calculate_symbol_probabilities(text)
        low = 0.0
        high = 1.0
        range_size = 1.0
        for symbol in text:
            symbol_prob = self.symbol_probabilities[symbol]
            low += range_size * sum(
                self.symbol_probabilities[prev_symbol] for prev_symbol in self.symbol_probabilities if
                prev_symbol < symbol)
            high = low + range_size * symbol_prob
            range_size = high - low
        encoded_value = (low + high) / 2
        return encoded_value

    def decode(self, encoded_value, text_length):
        decoded_text = ""
        low = 0.0
        high = 1.0
        range_size = 1.0
        tolerance = 1e-9  # Tolerance level for floating-point comparisons

        for _ in range(text_length):
            for symbol, symbol_prob in self.symbol_probabilities.items():
                symbol_low = low + range_size * sum(
                    self.symbol_probabilities[prev_symbol] for prev_symbol in self.symbol_probabilities if
                    prev_symbol < symbol)
                symbol_high = symbol_low + range_size * symbol_prob
                if abs(encoded_value - symbol_low) < tolerance:
                    decoded_text += symbol
                    low = symbol_low
                    high = symbol_high
                    range_size = high - low
                    break
                elif symbol_low <= encoded_value < symbol_high:
                    decoded_text += symbol
                    low = symbol_low
                    high = symbol_high
                    range_size = high - low
                    break

        return decoded_text


class HuffmanCodec:
    class Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def __init__(self):
        self.root = None
        self.mapping = {}

    def build_huffman_tree(self, text):
        freq_counter = Counter(text)
        priority_queue = [self.Node(char, freq)
                          for char, freq in freq_counter.items()]
        heapq.heapify(priority_queue)
        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = self.Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)
        self.root = priority_queue[0]

    def generate_huffman_codes(self, root, code=""):
        if root is None:
            return
        if root.char is not None:
            self.mapping[root.char] = code
            return
        self.generate_huffman_codes(root.left, code + "0")
        self.generate_huffman_codes(root.right, code + "1")

    def huffman_encode(self, text):
        encoded_text_list = []  # List to store each encoded character
        for char in text:
            # Append each encoded character to the list
            encoded_text_list.append(self.mapping[char])
        return encoded_text_list

    def huffman_decode(self, encoded_text_list):
        decoded_text = ""
        current_node = self.root
        for code in encoded_text_list:
            for bit in code:
                if bit == "0":
                    current_node = current_node.left
                else:
                    current_node = current_node.right
                if current_node.char is not None:
                    decoded_text += current_node.char
                    current_node = self.root
                    break  # Move to the next encoded character
        return decoded_text


class RunLengthCodec:
    @staticmethod
    def run_length_encode(text):
        encoded_text = []
        count = 1
        for i in range(1, len(text)):
            if text[i] == text[i - 1]:
                count += 1
            else:
                encoded_text.append((text[i - 1], count))
                count = 1
        encoded_text.append((text[-1], count))
        return encoded_text

    @staticmethod
    def run_length_decode(encoded_text):
        decoded_text = ""
        for char, count in encoded_text:
            decoded_text += char * count
        return decoded_text


# CODE FROM KAREEM

# Compression functions Example


def runlength_encoding(text):
    # Add Code Here
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0
    # Calculate probability
    probability = 0
    entropy = 0
    average_length = "out of course scope"
    efficiency = "out of course scope"

    # Catch the values so I can print it
    return {

        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio,
        'probability': probability,
        'entropy': entropy,
        'average_length': average_length,
        'efficiency': efficiency

    }


def huffman_encoding(text):
    # Implement Huffman Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    probability = 0
    entropy = 1
    average_length = 1
    efficiency = (entropy/average_length)*100

    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio,
        'probability': probability,
        'entropy': entropy,
        'average_length': average_length,
        'efficiency': efficiency
    }


def arithmetic_encoding(text):
    # Implement Arithmetic Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = "Out of the course scope"
    probability = 0
    entropy = 1
    average_length = "out of course scope"
    efficiency = "out of course scope"

    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio,
        'probability': probability,
        'entropy': entropy,
        'average_length': average_length,
        'efficiency': efficiency
    }


def golomb_encoding(text):
    # Implement Golomb Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    probability = 0
    entropy = 1
    average_length = 1
    efficiency = (entropy/average_length)*100
    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio,
        'probability': probability,
        'entropy': entropy,
        'average_length': average_length,
        'efficiency': efficiency
    }


def lzw_encoding(text):
    # Implement LZW Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes

    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    probability = 0
    entropy = 1
    average_length = "out of course scope"
    efficiency = "out of course scope"
    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio,
        'probability': probability,
        'entropy': entropy,
        'average_length': average_length,
        'efficiency': efficiency
    }

# Route to calculate compression results


@app.route("/compress_text", methods=["POST"])
def compress_text():
    # Get the text from the request data
    text = request.json.get("text")

    # Calculate compression results using each technique
    runlength_results = runlength_encoding(text)
    huffman_results = huffman_encoding(text)
    arithmetic_results = arithmetic_encoding(text)
    golomb_results = golomb_encoding(text)
    lzw_results = lzw_encoding(text)

    # Return the compression results as JSON
    return jsonify({
        'Runlength Encoding': runlength_results,
        'Huffman Encoding': huffman_results,
        'Arithmetic Encoding': arithmetic_results,
        'Golomb Encoding': golomb_results,
        'LZW Encoding': lzw_results
    })


if __name__ == "__main__":
    app.run(debug=True)
