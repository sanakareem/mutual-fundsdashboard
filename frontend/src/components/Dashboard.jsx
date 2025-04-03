"use client"

import React, { useState, useEffect } from 'react';
import PerformanceChart from './PerformanceChart';
import AllocationBlocks from './AllocationBlocks';
import OverlapAnalysis from './OverlapAnalysis';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('portfolio'); // Set default to 'portfolio' to match the new image
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeFrame, setTimeFrame] = useState('1M');

  // Sample data for investment summary cards
  const summaryData = {
    currentValue: 550000, // Updated to match image
    initialValue: 500000,
    currentReturnPercentage: 0.6,
    totalReturnPercentage: 10, // Updated to match image
    gainAmount: 50000, // Added to match image
    bestPerformingFund: "ICICI Prudential Midcap Fund",
    bestPerformingReturn: 19,
    worstPerformingFund: "Axis Flexi Cap Fund",
    worstPerformingReturn: -5
  };

  // Calculate Internal Rate of Return (IRR) based on purchase dates
  const calculateIRR = (investments) => {
    if (!investments || investments.length === 0) return 0;
    
    // This is a simplified IRR calculation
    // In a real application, you would use a more sophisticated approach
    // such as the Newton-Raphson method to solve for IRR
    
    const totalInitialInvestment = investments.reduce((sum, inv) => sum + inv.amount, 0);
    const currentValue = summaryData.currentValue;
    
    // Get the average holding period in years
    const now = new Date();
    const avgHoldingPeriodDays = investments.reduce((sum, inv) => {
      const purchaseDate = new Date(inv.purchaseDate);
      const holdingDays = (now - purchaseDate) / (1000 * 60 * 60 * 24);
      return sum + holdingDays;
    }, 0) / investments.length;
    
    const avgHoldingPeriodYears = avgHoldingPeriodDays / 365;
    
    // Calculate CAGR as approximation of IRR
    const cagr = Math.pow(currentValue / totalInitialInvestment, 1 / avgHoldingPeriodYears) - 1;
    
    return cagr * 100;
  };

  useEffect(() => {
    // Simulate loading portfolio data
    const loadData = async () => {
      // In a real app, this would be an API call
      setTimeout(() => {
        // Sample portfolio data
        const sampleData = {
          performance: [], // This would be populated from API
          composition: {
            sector_allocations: [
              { name: 'Financial Services', allocation: 28 },
              { name: 'Technology', allocation: 22 },
              { name: 'Consumer Goods', allocation: 17 },
              { name: 'Healthcare', allocation: 12 },
              { name: 'Industrials', allocation: 8 },
              { name: 'Energy', allocation: 7 },
              { name: 'Others', allocation: 6 }
            ]
          },
          mutualFunds: [
            {
              id: 1,
              name: 'ICICI Prudential Midcap Fund',
              allocation: 25,
              purchaseDate: '2023-01-15',
              amount: 125000,
              currentValue: 148750
            },
            {
              id: 2,
              name: 'SBI Blue Chip Fund',
              allocation: 20,
              purchaseDate: '2022-11-20',
              amount: 100000,
              currentValue: 110000
            },
            {
              id: 3,
              name: 'Axis Bluechip Fund',
              allocation: 15,
              purchaseDate: '2023-03-10',
              amount: 75000,
              currentValue: 80250
            },
            {
              id: 4,
              name: 'Kotak Emerging Equity Scheme',
              allocation: 15,
              purchaseDate: '2022-12-05',
              amount: 75000,
              currentValue: 85500
            },
            {
              id: 5,
              name: 'Axis Flexi Cap Fund',
              allocation: 15,
              purchaseDate: '2023-02-18',
              amount: 75000,
              currentValue: 71250
            },
            {
              id: 6,
              name: 'Parag Parikh Flexi Cap Fund',
              allocation: 10,
              purchaseDate: '2023-01-28',
              amount: 50000,
              currentValue: 54000
            }
          ]
        };
        
        setPortfolioData(sampleData);
        setLoading(false);
      }, 1000);
    };
    
    loadData();
  }, []);
  
  const handleTimeFrameChange = (tf) => {
    setTimeFrame(tf);
  };

  // Calculate IRR for the portfolio
  const portfolioIRR = calculateIRR(portfolioData?.mutualFunds);

  return (
    <div className="bg-[#111827] text-white min-h-screen p-8">
      {/* Investment Summary Cards */}
      <div className="grid grid-cols-4 gap-5 mb-10">
        {/* Current Investment Value */}
        <div className="bg-[#1e293b] rounded-lg p-4 relative">
          <div className="absolute top-4 right-4 text-xs flex items-center">
            <span className="text-green-400 mr-1">+{summaryData.currentReturnPercentage}%</span>
            <span className="text-xs text-gray-400">1D Return</span>
          </div>
          <div className="border-l-4 border-blue-500 pl-2 mb-2">
            <div className="text-xs text-gray-400">Current</div>
            <div className="text-xs text-gray-400">Investment Value</div>
          </div>
          <div className="text-xl font-bold mt-2">₹{summaryData.currentValue.toLocaleString()}</div>
        </div>
        
        {/* Initial Investment Value */}
        <div className="bg-[#1e293b] rounded-lg p-4 relative">
          <div className="absolute top-4 right-4 text-xs flex items-center">
            <span className="text-green-400 mr-1">+{summaryData.totalReturnPercentage}%</span>
            <span className="text-xs text-gray-400">Inception</span>
          </div>
          <div className="border-l-4 border-blue-500 pl-2 mb-2">
            <div className="text-xs text-gray-400">Initial</div>
            <div className="text-xs text-gray-400">Investment Value</div>
          </div>
          <div className="text-xl font-bold mt-2">₹{summaryData.initialValue.toLocaleString()}</div>
        </div>
        
        {/* Best Performing Scheme */}
        <div className="bg-[#1e293b] rounded-lg p-4 relative">
          <div className="absolute top-4 right-4 text-xs flex items-center">
            <span className="text-green-400 mr-1">+{summaryData.bestPerformingReturn}%</span>
            <span className="text-xs text-gray-400">Inception</span>
          </div>
          <div className="border-l-4 border-blue-500 pl-2 mb-2">
            <div className="text-xs text-gray-400">Best</div>
            <div className="text-xs text-gray-400">Performing Scheme</div>
          </div>
          <div className="text-xl font-bold mt-2">{summaryData.bestPerformingFund}</div>
        </div>
        
        {/* Worst Performing Scheme */}
        <div className="bg-[#1e293b] rounded-lg p-4 relative">
          <div className="absolute top-4 right-4 text-xs flex items-center">
            <span className="text-red-400 mr-1">{summaryData.worstPerformingReturn}%</span>
            <span className="text-xs text-gray-400">Inception</span>
          </div>
          <div className="border-l-4 border-blue-500 pl-2 mb-2">
            <div className="text-xs text-gray-400">Worst</div>
            <div className="text-xs text-gray-400">Performing Scheme</div>
          </div>
          <div className="text-xl font-bold mt-2">{summaryData.worstPerformingFund}</div>
        </div>
      </div>
      
      {/* Tab navigation - Updated to exactly match the new image */}
      <div className="border-b border-gray-700 flex mb-8">
        <button 
          onClick={() => setActiveTab('performance')}
          className={`px-8 py-4 text-base font-normal ${activeTab === 'performance' ? 'text-white' : 'text-gray-400'}`}
        >
          Performance Metrics
          {activeTab === 'performance' && <div className="absolute bottom-0 left-0 w-full h-1 bg-blue-500"></div>}
        </button>
        <button 
          onClick={() => setActiveTab('portfolio')}
          className={`px-8 py-4 text-base font-normal relative ${activeTab === 'portfolio' ? 'text-white' : 'text-gray-400'}`}
        >
          Portfolio Composition
          {activeTab === 'portfolio' && <div className="absolute bottom-0 w-full h-1 bg-blue-500"></div>}
        </button>
      </div>
      
      {/* Display appropriate content based on active tab */}
      {activeTab === 'performance' ? (
        <div>
          <h2 className="text-xl font-bold mb-6">Performance Summary</h2>
          
          {/* Performance summary block - Updated to match image */}
          <div className="bg-[#1e293b] rounded-lg p-6 mb-8 inline-block">
            <div className="text-2xl font-bold">₹{summaryData.currentValue.toLocaleString()}</div>
            <div className="flex items-center mt-1">
              <div className="text-green-500 text-sm">₹{summaryData.gainAmount.toLocaleString()}</div>
              <div className="text-gray-400 text-sm mx-2">|</div>
              <div className="text-green-500 text-sm">{summaryData.totalReturnPercentage}%</div>
            </div>
          </div>
          
          {/* Performance chart */}
          <PerformanceChart 
            data={loading ? [] : portfolioData?.performance}
            timeFrame={timeFrame}
          />
          
          {/* Time frame selectors - Updated to match image */}
          <div className="flex space-x-2 mt-4">
            {['1M', '3M', '6M', '1Y', '3Y', 'MAX'].map((tf) => (
              <button
                key={tf}
                onClick={() => handleTimeFrameChange(tf)}
                className={`px-4 py-2 text-sm rounded-md ${
                  timeFrame === tf 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>
          
          {/* IRR Information */}
          <div className="mt-12 bg-[#1e293b] rounded-lg p-6">
            <h3 className="text-lg font-bold mb-3">Internal Rate of Return (IRR)</h3>
            <p className="text-gray-300 mb-3">
              The IRR is calculated based on the purchase dates of funds in your portfolio.
            </p>
            <div className="text-xl font-bold text-green-500">
              {portfolioIRR.toFixed(2)}% <span className="text-sm text-gray-400">per annum</span>
            </div>
          </div>
        </div>
      ) : (
        <div>
          <AllocationBlocks />
          
          <OverlapAnalysis />
        </div>
      )}
    </div>
  );
};

export default Dashboard;