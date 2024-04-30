import React, { useState } from 'react';

function CompressionApp() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [bestTechnique, setBestTechnique] = useState('');

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const compressText = async () => {
    // Send a POST request to the Flask server to compress the text
    const response = await fetch('/compress_text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    // Get the compression results from the server response
    const compressionResults = await response.json();

    // Update state with the compression results
    setResults(compressionResults);

    // Find the best compression technique
    let bestCompressionRatio = 0;
    let bestTechnique = '';

    Object.keys(compressionResults).forEach((technique) => {
      const compressionRatio = compressionResults[technique].compression_ratio;
      if (compressionRatio > bestCompressionRatio) {
        bestCompressionRatio = compressionRatio;
        bestTechnique = technique;
      }
    });

    setBestTechnique(bestTechnique);
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
