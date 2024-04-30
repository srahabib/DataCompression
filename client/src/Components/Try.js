import React, { useState } from 'react';

function CompressionApp() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [bestTechnique, setBestTechnique] = useState('');

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const compressText = () => {
    // Simulate compression results for each technique
    const runlengthResults = runlengthEncoding(text);
    const huffmanResults = huffmanEncoding(text);
    const arithmeticResults = arithmeticEncoding(text);
    const golombResults = golombEncoding(text);
    const lzwResults = lzwEncoding(text);

    // Find the best compression ratio and technique
    const techniques = [
      { name: 'Runlength Encoding', results: runlengthResults },
      { name: 'Huffman Encoding', results: huffmanResults },
      { name: 'Arithmetic Encoding', results: arithmeticResults },
      { name: 'Golomb Encoding', results: golombResults },
      { name: 'LZW Encoding', results: lzwResults },
    ];
    let bestCompressionRatio = 0;
    let bestTechnique = '';

    techniques.forEach((technique) => {
      if (technique.results.compression_ratio > bestCompressionRatio) {
        bestCompressionRatio = technique.results.compression_ratio;
        bestTechnique = technique.name;
      }
    });

    setResults({
      'Runlength Encoding': runlengthResults,
      'Huffman Encoding': huffmanResults,
      'Arithmetic Encoding': arithmeticResults,
      'Golomb Encoding': golombResults,
      'LZW Encoding': lzwResults,
    });
    setBestTechnique(bestTechnique);
  };

  const runlengthEncoding = (text) => {
    const compressed = text.replace(/(.)\1*/g, (match, char) => {
      const count = match.length;
      return count === 1 ? char : `${count}${char}`;
    });
    const bits_before = text.length * 8;
    const bits_after = compressed.length * 8;
    const compression_ratio = ((text.length * 8 - compressed.length * 8) / (text.length * 8)) * 100;
    const probability =0
    const entropy =0
    const average_length =0
    const efficiency =0
    return { compressed, bits_before, bits_after, compression_ratio ,probability ,entropy, average_length , efficiency };
  };

  const huffmanEncoding = (text) => {
    // Implement Huffman Encoding logic here
    // This is a placeholder for the actual implementation
    // Simulating results for demonstration purposes
    const bits_before = text.length * 8;
    const bits_after = Math.ceil(text.length * 0.6) * 8;
    const compression_ratio = ((text.length * 8 - Math.ceil(text.length * 0.6) * 8) / (text.length * 8)) * 100;
    const probability =0
    const entropy =0
    const average_length =0
    const efficiency =0
    return { bits_before, bits_after, compression_ratio ,probability ,entropy, average_length , efficiency };
  };

  const arithmeticEncoding = (text) => {
    // Implement Arithmetic Encoding logic here
    // This is a placeholder for the actual implementation
    // Simulating results for demonstration purposes
    const bits_before = text.length * 8;
    const bits_after = Math.ceil(text.length * 0.7) * 8;
    const compression_ratio = ((text.length * 8 - Math.ceil(text.length * 0.7) * 8) / (text.length * 8)) * 100;
    const probability =0
    const entropy =0
    const average_length =0
    const efficiency =0
    return { bits_before, bits_after, compression_ratio ,probability ,entropy, average_length , efficiency };
  };

  const golombEncoding = (text) => {
    // Implement Golomb Encoding logic here
    // This is a placeholder for the actual implementation
    // Simulating results for demonstration purposes
    const bits_before = text.length * 8;
    const bits_after = Math.ceil(text.length * 0.8) * 8;
    const compression_ratio = ((text.length * 8 - Math.ceil(text.length * 0.8) * 8) / (text.length * 8)) * 100;
    const probability =0
    const entropy =0
    const average_length =0
    const efficiency =0
    return { bits_before, bits_after, compression_ratio ,probability ,entropy, average_length , efficiency };
  };

  const lzwEncoding = (text) => {
    // Implement LZW Encoding logic here
    // This is a placeholder for the actual implementation
    // Simulating results for demonstration purposes
    const bits_before = text.length * 8;
    const bits_after = Math.ceil(text.length * 0.9) * 8;
    const compression_ratio = ((text.length * 8 - Math.ceil(text.length * 0.9) * 8) / (text.length * 8)) * 100;
    const probability =0
    const entropy =0
    const average_length =0
    const efficiency =0
    return { bits_before, bits_after, compression_ratio ,probability ,entropy, average_length ,efficiency };
  };

  return (
    <div className="container mx-auto py-8">
      <div className="max-w-lg mx-auto">
        <h1 className="font-black p-2 text-blue-500">Enter Text to Compress</h1>
        <div className="mb-4">
          <textarea
            value={text}
            onChange={handleTextChange}
            placeholder="Enter text to compress..."
            rows={4}
            cols={50}
            className="w-full p-4 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <button
            onClick={compressText}
            className="px-6 py-3 bg-blue-500 text-white rounded-md transition duration-300 ease-in-out hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Compress Text
          </button>
        </div>
        {results && (
          <div>
            <h2 className="text-xl font-semibold mb-2 text-yellow-500">Compression Results</h2>
            {Object.keys(results).map((technique, index) => (
              <div key={index} className="border border-gray-300 rounded-md p-4 mb-4">
                <h3 className="text-pink-500 text-xl">{technique}</h3>
                <p>Bits Before Encoding: {results[technique].bits_before}</p>
                <p>Bits After Encoding: {results[technique].bits_after}</p>
                <p>Compression Ratio (%): {results[technique].compression_ratio.toFixed(2)}</p>
                <p>Probability of Occurrence: {JSON.stringify(results[technique].probability)}</p>
                <p>Entropy: {results[technique].entropy.toFixed(2)}</p>
                <p>Average Length: {results[technique].average_length.toFixed(2)}</p>
                <p>Efficiency: {results[technique].efficiency.toFixed(2)}%</p>
                {/* Add more details as needed */}
              </div>
            ))}
            {bestTechnique && (
              <p className="mt-4">Best Technique: {bestTechnique}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default CompressionApp;
