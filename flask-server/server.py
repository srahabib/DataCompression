from flask import Flask, jsonify, request
from textblob import TextBlob

app = Flask(__name__)

# Compression functions


def runlength_encoding(text):
    compressed = ''
    i = 0
    while i < len(text):
        count = 1
        while i + 1 < len(text) and text[i] == text[i + 1]:
            i += 1
            count += 1
        compressed += str(count) + text[i]
        i += 1
    bits_before = len(text) * 8
    bits_after = len(compressed) * 8
    compression_ratio = ((len(text) * 8 - len(compressed)
                         * 8) / (len(text) * 8)) * 100
    return {
        'compressed': compressed,
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio
    }


def huffman_encoding(text):
    # Implement Huffman Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio
    }


def arithmetic_encoding(text):
    # Implement Arithmetic Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio
    }


def golomb_encoding(text):
    # Implement Golomb Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio
    }


def lzw_encoding(text):
    # Implement LZW Encoding logic here
    # Placeholder for actual implementation
    # Simulate results for demonstration purposes
    bits_before = len(text) * 8
    bits_after = bits_before  # Placeholder, actual logic needed
    compression_ratio = 0  # Placeholder, actual logic needed
    return {
        'bits_before': bits_before,
        'bits_after': bits_after,
        'compression_ratio': compression_ratio
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
        'LZW Encoding': lzw_results,
    })


if __name__ == "__main__":
    app.run(debug=True)
