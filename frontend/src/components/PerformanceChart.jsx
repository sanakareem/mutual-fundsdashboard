"use client"

import React, { useState, useEffect } from 'react';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const PerformanceChart = ({ data = [], timeFrame }) => {
  const [chartData, setChartData] = useState([]);
  
  useEffect(() => {
    // For demo purposes, generate sample data if none provided
    // In production, this would use the actual provided data
    if (!data || data.length === 0) {
      generateSampleData(timeFrame);
    } else {
      setChartData(data);
    }
  }, [data, timeFrame]);
  
  const generateSampleData = (timeFrame) => {
    const currentDate = new Date();
    let startDate;
    let interval;
    
    // Determine date range based on timeframe
    switch(timeFrame) {
      case '1M':
        startDate = new Date(currentDate);
        startDate.setMonth(currentDate.getMonth() - 1);
        interval = 2; // Every 2 days
        break;
      case '3M':
        startDate = new Date(currentDate);
        startDate.setMonth(currentDate.getMonth() - 3);
        interval = 5; // Every 5 days
        break;
      case '6M':
        startDate = new Date(currentDate);
        startDate.setMonth(currentDate.getMonth() - 6);
        interval = 10; // Every 10 days
        break;
      case '1Y':
        startDate = new Date(currentDate);
        startDate.setFullYear(currentDate.getFullYear() - 1);
        interval = 20; // Every 20 days
        break;
      case '3Y':
        startDate = new Date(currentDate);
        startDate.setFullYear(currentDate.getFullYear() - 3);
        interval = 60; // Every 60 days
        break;
      case 'MAX':
        startDate = new Date(currentDate);
        startDate.setFullYear(currentDate.getFullYear() - 5);
        interval = 120; // Every 120 days
        break;
      default:
        startDate = new Date(currentDate);
        startDate.setMonth(currentDate.getMonth() - 1);
        interval = 2;
    }
    
    // Create sample data that mimics the chart pattern in the image
    const sampleData = [];
    let currentValue = 500000;
    let date = new Date(startDate);
    let trend = 1; // 1 for uptrend, -1 for downtrend
    let trendCount = 0;
    
    while (date <= currentDate) {
      // Create some volatility in the chart
      trendCount++;
      if (trendCount > Math.floor(Math.random() * 5) + 3) {
        trend = -trend;
        trendCount = 0;
      }
      
      // Add some randomness to the price movement
      const changePercent = (Math.random() * 1.5 + 0.2) * trend;
      currentValue = currentValue * (1 + changePercent / 100);
      
      // Format the date for display
      const formattedDate = formatChartDate(date, timeFrame);
      
      sampleData.push({
        date: formattedDate,
        value: Math.round(currentValue),
        fullDate: new Date(date) // Store the full date for tooltip display
      });
      
      // Increment the date by the interval
      date.setDate(date.getDate() + interval);
    }
    
    // Ensure we end at 550000 to match the dashboard
    sampleData[sampleData.length - 1].value = 550000;
    
    setChartData(sampleData);
  };
  
  const formatChartDate = (date, timeFrame) => {
    const day = date.getDate();
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[date.getMonth()];
    
    if (timeFrame === '1M' || timeFrame === '3M') {
      return `${day} ${month}`;
    } else {
      return `${day} ${month} ${date.getFullYear().toString().substr(2, 2)}`;
    }
  };
  
  const formatTooltipDate = (date) => {
    if (!date) return '';
    
    const d = new Date(date);
    const day = d.getDate();
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[d.getMonth()];
    const year = d.getFullYear();
    
    return `${day} ${month} ${year}`;
  };
  
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 p-3 rounded shadow-lg border border-gray-700">
          <p className="text-sm text-gray-300">{formatTooltipDate(data.fullDate)}</p>
          <p className="text-sm font-medium">₹{data.value.toLocaleString()}</p>
        </div>
      );
    }
    return null;
  };
  
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
        >
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#2563EB" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis 
            dataKey="date" 
            axisLine={false}
            tickLine={false}
            tickMargin={10}
            tick={{ fill: '#71717a', fontSize: 12 }}
            interval={"preserveStartEnd"}
          />
          <YAxis 
            hide={true}
            domain={['dataMin - 10000', 'dataMax + 10000']}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line 
            type="monotone"
            dataKey="value"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6, fill: '#3b82f6', strokeWidth: 3, stroke: '#111827' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceChart;