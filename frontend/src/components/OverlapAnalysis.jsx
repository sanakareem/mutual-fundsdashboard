"use client"

import React, { useState } from 'react';

const OverlapAnalysis = () => {
  const [selectedFund, setSelectedFund] = useState(null);

  // Handle fund selection
  const handleFundClick = (fundId) => {
    setSelectedFund(selectedFund === fundId ? null : fundId);
  };

  return (
    <div className="mt-16">
      <div className="flex items-center mb-6">
        <h2 className="text-2xl font-normal text-white">Overlap Analysis</h2>
        <button className="ml-2 text-gray-400 hover:text-gray-300">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>
      
      <div className="text-white mb-5">Comparing : Motilal Large Cap Fund and Nippon Large Cap Fund</div>
      <div className="mb-8">
        <div className="flex items-start mb-2">
          <div className="text-yellow-500 mr-2 mt-1 text-sm">•</div>
          <div className="text-white">X Stocks Overlap across these funds.</div>
        </div>
        <div className="flex items-start">
          <div className="text-yellow-500 mr-2 mt-1 text-sm">•</div>
          <div className="text-white">Y% Average Overlap in holdings.</div>
        </div>
      </div>

      {/* Sankey diagram with exact design matching image */}
      <div className="w-full bg-[#0f172a] p-6 rounded-lg relative">
        <div className="relative h-[600px]">
          {/* Nippon */}
          <div 
            className={`absolute top-8 left-8 bg-[#b19259] rounded-md p-4 w-64 text-white cursor-pointer z-10 ${selectedFund === 1 ? 'ring-1 ring-white' : ''}`}
            onClick={() => handleFundClick(1)}
          >
            <div className="text-base font-normal">Nippon Large</div>
            <div className="text-base font-normal">Cap Fund -</div>
            <div className="text-base font-normal">Direct Plan</div>
          </div>
          <div className="absolute top-8 left-72 bg-yellow-500 h-[75px] w-2"></div>
          
          {/* Motilal */}
          <div 
            className={`absolute top-[136px] left-8 bg-[#1e3d6b] rounded-md p-4 w-64 text-white cursor-pointer z-10 ${selectedFund === 2 ? 'ring-1 ring-white' : ''}`}
            onClick={() => handleFundClick(2)}
          >
            <div className="text-base font-normal">Motilal Large</div>
            <div className="text-base font-normal">Cap Fund -</div>
            <div className="text-base font-normal">Direct Plan</div>
          </div>
          <div className="absolute top-[136px] left-72 bg-blue-500 h-[75px] w-2"></div>
          
          {/* HDFC */}
          <div 
            className={`absolute top-[265px] left-8 bg-[#59391f] rounded-md p-4 w-64 text-white cursor-pointer z-10 ${selectedFund === 3 ? 'ring-1 ring-white' : ''}`}
            onClick={() => handleFundClick(3)}
          >
            <div className="text-base font-normal">HDFC Large</div>
            <div className="text-base font-normal">Cap Fund</div>
          </div>
          <div className="absolute top-[265px] left-72 bg-orange-600 h-[52px] w-2"></div>
          
          {/* ICICI */}
          <div 
            className={`absolute top-[365px] left-8 bg-[#4d582a] rounded-md p-4 w-64 text-white cursor-pointer z-10 ${selectedFund === 4 ? 'ring-1 ring-white' : ''}`}
            onClick={() => handleFundClick(4)}
          >
            <div className="text-base font-normal">ICICI</div>
            <div className="text-base font-normal">Prudential</div>
            <div className="text-base font-normal">Midcap Fund</div>
          </div>
          <div className="absolute top-[365px] left-72 bg-lime-600 h-[75px] w-2"></div>
          
          {/* Right side stocks - Exactly aligned vertically */}
          <div className={`absolute top-[50px] right-8 flex items-center ${selectedFund && !([1, 3].includes(selectedFund)) ? 'opacity-40' : ''}`}>
            <div className="h-6 w-2 mr-3 bg-yellow-500"></div>
            <div className="text-white text-base font-normal">HDFC LTD.</div>
          </div>
          
          <div className={`absolute top-[150px] right-8 flex items-center ${selectedFund && !([1, 2, 4].includes(selectedFund)) ? 'opacity-40' : ''}`}>
            <div className="h-6 w-2 mr-3 bg-green-500"></div>
            <div className="text-white text-base font-normal">RIL</div>
          </div>
          
          <div className={`absolute top-[250px] right-8 flex items-center ${selectedFund && !([1, 2].includes(selectedFund)) ? 'opacity-40' : ''}`}>
            <div className="h-6 w-2 mr-3 bg-purple-500"></div>
            <div className="text-white text-base font-normal">INFY</div>
          </div>
          
          <div className={`absolute top-[350px] right-8 flex items-center ${selectedFund && !(selectedFund === 2) ? 'opacity-40' : ''}`}>
            <div className="h-6 w-2 mr-3 bg-teal-500"></div>
            <div className="text-white text-base font-normal">TCS</div>
          </div>
          
          <div className={`absolute top-[450px] right-8 flex items-center ${selectedFund && !([2, 3].includes(selectedFund)) ? 'opacity-40' : ''}`}>
            <div className="h-6 w-2 mr-3 bg-red-500"></div>
            <div className="text-white text-base font-normal">HDFCBANK</div>
          </div>
          
          <div className={`absolute top-[550px] right-8 flex items-center ${selectedFund && !([3, 4].includes(selectedFund)) ? 'opacity-40' : ''}`}>
            <div className="h-6 w-2 mr-3 bg-orange-500"></div>
            <div className="text-white text-base font-normal">BHARTIARTL</div>
          </div>
          
          {/* Connection lines - with improved alignment */}
          <svg className="absolute inset-0 w-full h-full z-0">
            {/* Nippon connections */}
            <path d="M 310 50 L 850 50" className={`stroke-gray-500 ${selectedFund === 1 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 50 L 850 150" className={`stroke-gray-500 ${selectedFund === 1 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 50 L 850 250" className={`stroke-gray-500 ${selectedFund === 1 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            
            {/* Motilal connections */}
            <path d="M 310 175 L 850 150" className={`stroke-gray-500 ${selectedFund === 2 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 175 L 850 250" className={`stroke-gray-500 ${selectedFund === 2 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 175 L 850 350" className={`stroke-gray-500 ${selectedFund === 2 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 175 L 850 450" className={`stroke-gray-500 ${selectedFund === 2 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            
            {/* HDFC connections */}
            <path d="M 310 290 L 850 50" className={`stroke-gray-500 ${selectedFund === 3 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 290 L 850 450" className={`stroke-gray-500 ${selectedFund === 3 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 290 L 850 550" className={`stroke-gray-500 ${selectedFund === 3 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            
            {/* ICICI connections */}
            <path d="M 310 395 L 850 150" className={`stroke-gray-500 ${selectedFund === 4 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
            <path d="M 310 395 L 850 550" className={`stroke-gray-500 ${selectedFund === 4 ? 'opacity-80' : 'opacity-30'}`} strokeWidth="1" fill="none" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default OverlapAnalysis;