"use client"

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Layout = ({ children }) => {
  const pathname = usePathname();
  const username = "Yashna"; 
  
  return (
    <div className="min-h-screen bg-[#121212] text-white">
      <div className="max-w-7xl mx-auto">
        {/* Main container */}
        <div className="bg-[#121212]">
          {/* Top navigation bar */}
          <div className="px-8 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-12">
              {/* Logo */}
              <Link href="/">
                <span className="text-blue-500 text-3xl font-bold">d</span>
              </Link>

              {/* Navigation items */}
              <nav className="flex items-center space-x-8">
                <Link href="/">
                  <span className="py-5 px-2 text-sm font-medium text-gray-400 hover:text-gray-200">
                    Home
                  </span>
                </Link>
                <Link href="/portfolio">
                  <span className="py-5 px-2 text-sm font-medium text-white border-b-2 border-blue-500">
                    Portfolio
                  </span>
                </Link>
                <Link href="/mutual-funds">
                  <span className="py-5 px-2 text-sm font-medium text-gray-400 hover:text-gray-200">
                    Mutual Funds
                  </span>
                </Link>
                <Link href="/tools">
                  <span className="py-5 px-2 text-sm font-medium text-gray-400 hover:text-gray-200">
                    Tools
                  </span>
                </Link>
                <Link href="/transactions">
                  <span className="py-5 px-2 text-sm font-medium text-gray-400 hover:text-gray-200">
                    Transactions
                  </span>
                </Link>
              </nav>
            </div>

            {/* Right side icons */}
            <div className="flex items-center space-x-6">
              <button className="text-gray-300 hover:text-white">
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
              <button className="text-gray-300 hover:text-white relative">
                <div className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 rounded-full flex items-center justify-center">
                  <span className="text-[10px]">1</span>
                </div>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </button>
              <button className="text-gray-300 hover:text-white">
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </button>
              <button className="text-gray-300 hover:text-white">
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </button>
            </div>
          </div>

          {/* Content area with sidebar */}
          <div className="flex">
            {/* Sidebar */}
            <div className="w-48 p-5">
              <div className="bg-[#303030] rounded p-3 mb-5">
                <span className="text-sm font-medium">PHA</span>
              </div>
              
              <div className="space-y-5">
                <div>
                  <span className="text-sm text-gray-300">Fund Analysis</span>
                </div>
                
                <div>
                  <span className="text-sm text-gray-300">Holdings</span>
                </div>
                
                <div>
                  <span className="text-sm text-gray-300">Transactions</span>
                </div>
              </div>
            </div>

            {/* Main content */}
            <div className="flex-1 p-6">
              {/* Welcome section */}
              <div className="mb-6">
                <h1 className="text-2xl font-bold">Good morning, {username}!</h1>
                <p className="text-gray-400 text-sm">Evaluate Your Investment Performance</p>
              </div>
              
              {/* Main content from the page */}
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Layout;