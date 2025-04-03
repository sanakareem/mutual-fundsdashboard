"use client";

import React, { useState } from 'react';

const AllocationBlocks = () => {
  const [isFinancialHovered, setIsFinancialHovered] = useState(false);
  const [isHealthcareHovered, setIsHealthcareHovered] = useState(false);

  return (
    <div>
      <h2 className="text-xl font-normal text-white mb-6">Sector Allocation</h2>
      
      <div className="grid grid-cols-12 gap-4">
        {/* Financial Section */}
        <div
          className="col-span-8 bg-[#a4b3d2] rounded-lg p-4 relative h-40 transition-all duration-300 overflow-hidden"
          onMouseEnter={() => setIsFinancialHovered(true)}
          onMouseLeave={() => setIsFinancialHovered(false)}
        >
          {isFinancialHovered ? (
            // Expanded View (on hover)
            <div className="grid grid-cols-2 gap-4 h-full">
              {/* HDFC Bank */}
              <div className="bg-[#8ca2c9] rounded-lg p-3 relative">
                <div className="text-black text-sm">HDFC Bank</div>
                <div className="text-black text-xs">₹78,000</div>
                <div className="absolute bottom-2 right-2 text-3xl font-normal text-black">40%</div>
              </div>
              {/* Bajaj Finance */}
              <div className="bg-[#8ca2c9] rounded-lg p-3 relative">
                <div className="text-black text-sm">Bajaj Finance</div>
                <div className="text-black text-xs">₹19,500</div>
                <div className="absolute bottom-2 right-2 text-xl font-normal text-black">10%</div>
              </div>
              {/* ICICI Bank */}
              <div className="bg-[#8ca2c9] rounded-lg p-3 relative">
                <div className="text-black text-sm">ICICI Bank</div>
                <div className="text-black text-xs">₹58,500</div>
                <div className="absolute bottom-2 right-2 text-2xl font-normal text-black">30%</div>
              </div>
              {/* Kotak Mahindra Bank */}
              <div className="bg-[#8ca2c9] rounded-lg p-3 relative">
                <div className="text-black text-sm">Kotak Mahindra Bank</div>
                <div className="text-black text-xs">₹39,000</div>
                <div className="absolute bottom-2 right-2 text-xl font-normal text-black">20%</div>
              </div>
            </div>
          ) : (
            // Collapsed View (default)
            <>
              <div className="text-black text-base">Financial</div>
              <div className="text-black text-sm">₹1,95,000</div>
              <div className="absolute bottom-6 left-6 text-3xl font-normal text-black">34%</div>
            </>
          )}
        </div>

        {/* Healthcare Section */}
<div
  className="col-span-4 bg-[#a4b3d2] rounded-lg p-4 relative h-40 transition-all duration-300 overflow-hidden"
  onMouseEnter={() => setIsHealthcareHovered(true)}
  onMouseLeave={() => setIsHealthcareHovered(false)}
>
  {isHealthcareHovered ? (
    // Expanded View (on hover) - Matching Design 1
    <div className="flex h-full gap-2">
      {/* Infosys - 40% (large block on left) */}
      <div className="w-1/2 bg-[#8ca2c9] rounded-lg p-3 relative">
        <div className="text-black text-sm">Infosys</div>
        <div className="text-black text-xs">₹44,400</div>
        <div className="absolute bottom-4 right-4 text-4xl font-normal text-black">40%</div>
      </div>
      
      {/* Right Side - TCS, HCL Tech, and Wipro */}
      <div className="w-1/2 flex flex-col gap-2">
        {/* TCS - 25% (top right block) */}
        <div className="h-1/2 bg-[#8ca2c9] rounded-lg p-3 relative">
          <div className="text-black text-sm">TCS</div>
          <div className="text-black text-xs">₹27,750</div>
          <div className="absolute bottom-4 right-4 text-3xl font-normal text-black">25%</div>
        </div>
        
        {/* Bottom Right - HCL Tech and Wipro */}
        <div className="h-1/2 flex gap-2">
          {/* HCL Tech - 20% (bottom left on right side) */}
          <div className="w-3/5 bg-[#8ca2c9] rounded-lg p-3 relative">
            <div className="text-black text-sm">HCL Tech</div>
            <div className="text-black text-xs">₹22,200</div>
            <div className="absolute bottom-4 right-4 text-2xl font-normal text-black">20%</div>
          </div>
          
          {/* Wipro - 15% (bottom right) */}
          <div className="w-2/5 bg-[#8ca2c9] rounded-lg p-3 relative">
            <div className="text-black text-sm">Wipro</div>
            <div className="text-black text-xs">₹16,650</div>
            <div className="absolute bottom-4 right-4 text-2xl font-normal text-black">15%</div>
          </div>
        </div>
      </div>
    </div>
  ) : (
    // Collapsed View (default)
    <>
      <div className="text-black text-base">Healthcare</div>
      <div className="text-black text-sm">₹1,11,000</div>
      <div className="absolute bottom-6 right-6 text-3xl font-normal text-black">19%</div>
    </>
  )}
</div>

        {/* Technology Section */}
        <div className="col-span-4 bg-[#bbc6db] rounded-lg p-4 relative h-36">
          <div className="text-black text-base">Technology</div>
          <div className="text-black text-sm">₹1,11,000</div>
          <div className="absolute bottom-6 left-6 text-3xl font-normal text-black">19%</div>
        </div>

        {/* Consumer Goods Section */}
        <div className="col-span-2 bg-[#bbc6db] rounded-lg p-4 relative h-36">
          <div className="text-black text-base">Consumer Goods</div>
          <div className="text-black text-sm">₹55,500</div>
          <div className="absolute bottom-6 left-6 text-3xl font-normal text-black">9.5%</div>
        </div>

        {/* Energy Section */}
        <div className="col-span-3 bg-[#bbc6db] rounded-lg p-4 relative h-36">
          <div className="text-black text-base">Energy</div>
          <div className="text-black text-sm">₹55,500</div>
          <div className="absolute bottom-6 left-6 text-3xl font-normal text-black">9.5%</div>
        </div>

        {/* Other Sectors Section */}
        <div className="col-span-3 bg-[#bbc6db] rounded-lg p-4 relative h-36">
          <div className="text-black text-base">Other Sectors</div>
          <div className="text-black text-sm">₹55,500</div>
          <div className="absolute bottom-6 left-6 text-3xl font-normal text-black">9.5%</div>
        </div>
      </div>
    </div>
  );
};

export default AllocationBlocks;