import React from 'react';

function Hero() {
  return (
    <div className="relative overflow-hidden rounded-lg bg-cover bg-no-repeat p-12 text-center" style={{ height: '500px', backgroundImage: "url('/HERO.jpg')" }}>
      <div className="absolute bottom-0 left-0 right-0 top-0 h-full w-full overflow-hidden bg-fixed bg-black bg-opacity-50">
        <div className="flex h-full items-center justify-center">
          <div className="text-white">
            <h2 className="mb-4 text-4xl font-semibold">Data Squeeze </h2>
            <h4 className="mb-6 text-xl font-semibold"> Explore Lossless Data Compression Techniques</h4>

          </div>
        </div>
      </div>
    </div>
  );
}

export default Hero;
