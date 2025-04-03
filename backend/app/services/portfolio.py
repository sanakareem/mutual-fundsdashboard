from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date
from typing import List, Optional, Dict
import uuid

from app.db.models import Investment, MutualFund, FundPerformance, FundAllocation, FundHolding, FundCapAllocation

def get_portfolio_summary(db: Session, user_id: str):
    """
    Get a summary of the user's portfolio including:
    - Current value
    - Initial investment
    - Total return
    - Return percentage
    - Best performing fund
    - Worst performing fund
    """
    # Get all investments for the user
    investments = db.query(Investment).filter(Investment.user_id == user_id).all()
    
    if not investments:
        return {
            "current_value": 0,
            "initial_investment": 0,
            "total_return": 0,
            "return_percentage": 0,
            "best_performing_fund": "",
            "best_performing_return": 0,
            "worst_performing_fund": "",
            "worst_performing_return": 0
        }
    
    # Calculate current value and total investment
    current_value = 0
    initial_investment = 0
    fund_performance = {}
    
    for investment in investments:
        # Get the latest NAV for the fund
        latest_nav = db.query(FundPerformance)\
            .filter(FundPerformance.fund_id == investment.fund_id)\
            .order_by(FundPerformance.date.desc())\
            .first()
        
        if latest_nav:
            # Calculate current value of this investment
            investment_value = investment.units * latest_nav.nav
            current_value += investment_value
            
            # Add to initial investment
            initial_investment += investment.amount_invested
            
            # Calculate return for this fund
            fund_return = (investment_value - investment.amount_invested) / investment.amount_invested * 100
            
            # Get fund name
            fund = db.query(MutualFund).filter(MutualFund.id == investment.fund_id).first()
            fund_name = fund.name if fund else "Unknown Fund"
            
            fund_performance[fund_name] = fund_return
    
    # Calculate total return
    total_return = current_value - initial_investment
    return_percentage = (total_return / initial_investment) * 100 if initial_investment > 0 else 0
    
    # Find best and worst performing funds
    best_fund = ""
    best_return = -float('inf')
    worst_fund = ""
    worst_return = float('inf')
    
    for fund_name, fund_return in fund_performance.items():
        if fund_return > best_return:
            best_fund = fund_name
            best_return = fund_return
        
        if fund_return < worst_return:
            worst_fund = fund_name
            worst_return = fund_return
    
    return {
        "current_value": current_value,
        "initial_investment": initial_investment,
        "total_return": total_return,
        "return_percentage": return_percentage,
        "best_performing_fund": best_fund,
        "best_performing_return": best_return,
        "worst_performing_fund": worst_fund,
        "worst_performing_return": worst_return
    }

def get_portfolio_performance(db: Session, user_id: str, timeframe: str = "1M"):
    """
    Get performance data for the user's portfolio over a specified timeframe.
    Timeframes: 1M, 3M, 6M, 1Y, 3Y, MAX
    """
    # Determine date range based on timeframe
    end_date = datetime.now().date()
    
    if timeframe == "1M":
        start_date = end_date - timedelta(days=30)
    elif timeframe == "3M":
        start_date = end_date - timedelta(days=90)
    elif timeframe == "6M":
        start_date = end_date - timedelta(days=180)
    elif timeframe == "1Y":
        start_date = end_date - timedelta(days=365)
    elif timeframe == "3Y":
        start_date = end_date - timedelta(days=365 * 3)
    else:  # MAX
        start_date = date(2000, 1, 1)  # A date far in the past
    
    # Get all investments for the user
    investments = db.query(Investment).filter(Investment.user_id == user_id).all()
    
    if not investments:
        return []
    
    # Get performance data for each date in the range
    performance_data = []
    current_date = start_date
    
    while current_date <= end_date:
        portfolio_value = 0
        
        for investment in investments:
            # If investment date is after current date, skip
            if investment.investment_date > current_date:
                continue
            
            # Get the NAV for the fund on this date
            nav = db.query(FundPerformance)\
                .filter(
                    FundPerformance.fund_id == investment.fund_id,
                    FundPerformance.date <= current_date
                )\
                .order_by(FundPerformance.date.desc())\
                .first()
            
            if nav:
                # Calculate value of this investment on this date
                investment_value = investment.units * nav.nav
                portfolio_value += investment_value
        
        # Add data point
        if portfolio_value > 0:
            performance_data.append({
                "date": current_date,
                "value": portfolio_value
            })
        
        # Move to next date
        current_date += timedelta(days=1)
    
    return performance_data

def get_portfolio_composition(db: Session, user_id: str):
    """
    Get composition details of the user's portfolio including:
    - Sector allocations
    - Stock allocations
    - Market cap allocations
    """
    # Get all investments for the user
    investments = db.query(Investment).filter(Investment.user_id == user_id).all()
    
    if not investments:
        return {
            "sector_allocations": [],
            "stock_allocations": [],
            "cap_allocations": []
        }
    
    # Calculate portfolio value
    portfolio_value = 0
    investment_values = {}
    
    for investment in investments:
        # Get the latest NAV for the fund
        latest_nav = db.query(FundPerformance)\
            .filter(FundPerformance.fund_id == investment.fund_id)\
            .order_by(FundPerformance.date.desc())\
            .first()
        
        if latest_nav:
            # Calculate current value of this investment
            investment_value = investment.units * latest_nav.nav
            investment_values[investment.fund_id] = investment_value
            portfolio_value += investment_value
    
    # Initialize dictionaries to aggregate allocations
    sector_allocations = {}
    stock_allocations = {}
    cap_allocations = {}
    
    # Process each investment
    for investment in investments:
        if investment.fund_id not in investment_values:
            continue
        
        investment_value = investment_values[investment.fund_id]
        investment_weight = investment_value / portfolio_value if portfolio_value > 0 else 0
        
        # Get sector allocations for this fund
        fund_sectors = db.query(FundAllocation).filter(FundAllocation.fund_id == investment.fund_id).all()
        for sector in fund_sectors:
            sector_value = investment_value * (sector.percentage / 100)
            if sector.sector in sector_allocations:
                sector_allocations[sector.sector] += sector_value
            else:
                sector_allocations[sector.sector] = sector_value
        
        # Get stock holdings for this fund
        fund_holdings = db.query(FundHolding).filter(FundHolding.fund_id == investment.fund_id).all()
        for holding in fund_holdings:
            stock_value = investment_value * (holding.percentage / 100)
            if holding.stock_name in stock_allocations:
                stock_allocations[holding.stock_name] += stock_value
            else:
                stock_allocations[holding.stock_name] = stock_value
        
        # Get market cap allocations for this fund
        fund_caps = db.query(FundCapAllocation).filter(FundCapAllocation.fund_id == investment.fund_id).all()
        for cap in fund_caps:
            cap_value = investment_value * (cap.percentage / 100)
            if cap.cap_type in cap_allocations:
                cap_allocations[cap.cap_type] += cap_value
            else:
                cap_allocations[cap.cap_type] = cap_value
    
    # Convert to percentage and format for response
    sector_result = []
    for sector, amount in sector_allocations.items():
        percentage = (amount / portfolio_value) * 100 if portfolio_value > 0 else 0
        sector_result.append({
            "sector": sector,
            "amount": amount,
            "percentage": percentage
        })
    
    stock_result = []
    for stock, amount in stock_allocations.items():
        percentage = (amount / portfolio_value) * 100 if portfolio_value > 0 else 0
        stock_result.append({
            "stock_name": stock,
            "amount": amount,
            "percentage": percentage
        })
    
    cap_result = []
    for cap_type, amount in cap_allocations.items():
        percentage = (amount / portfolio_value) * 100 if portfolio_value > 0 else 0
        cap_result.append({
            "cap_type": cap_type,
            "amount": amount,
            "percentage": percentage
        })
    
    # Sort by percentage in descending order
    sector_result.sort(key=lambda x: x["percentage"], reverse=True)
    stock_result.sort(key=lambda x: x["percentage"], reverse=True)
    cap_result.sort(key=lambda x: x["percentage"], reverse=True)
    
    return {
        "sector_allocations": sector_result,
        "stock_allocations": stock_result,
        "cap_allocations": cap_result
    }

def get_fund_overlap(db: Session, fund_id1: str, fund_id2: Optional[str] = None):
    """
    Get overlap analysis between mutual funds.
    If fund_id2 is provided, calculate overlap between the two funds.
    If fund_id2 is not provided, calculate overlap between fund_id1 and all other funds.
    """
    # Get holdings for fund1
    fund1_holdings = db.query(FundHolding).filter(FundHolding.fund_id == fund_id1).all()
    fund1_stocks = set(holding.stock_name for holding in fund1_holdings)
    
    # Get fund1 name
    fund1 = db.query(MutualFund).filter(MutualFund.id == fund_id1).first()
    fund1_name = fund1.name if fund1 else "Unknown Fund"
    
    result = []
    
    if fund_id2:
        # Calculate overlap with a specific fund
        fund2_holdings = db.query(FundHolding).filter(FundHolding.fund_id == fund_id2).all()
        fund2_stocks = set(holding.stock_name for holding in fund2_holdings)
        
        # Get fund2 name
        fund2 = db.query(MutualFund).filter(MutualFund.id == fund_id2).first()
        fund2_name = fund2.name if fund2 else "Unknown Fund"
        
        # Calculate overlap
        common_stocks = fund1_stocks.intersection(fund2_stocks)
        overlap_percentage = (len(common_stocks) / len(fund1_stocks)) * 100 if fund1_stocks else 0
        
        result.append({
            "fund1_name": fund1_name,
            "fund2_name": fund2_name,
            "overlap_percentage": overlap_percentage,
            "common_stocks": list(common_stocks)
        })
    else:
        # Calculate overlap with all other funds
        all_funds = db.query(MutualFund).filter(MutualFund.id != fund_id1).all()
        
        for fund2 in all_funds:
            fund2_holdings = db.query(FundHolding).filter(FundHolding.fund_id == fund2.id).all()
            fund2_stocks = set(holding.stock_name for holding in fund2_holdings)
            
            # Calculate overlap
            common_stocks = fund1_stocks.intersection(fund2_stocks)
            overlap_percentage = (len(common_stocks) / len(fund1_stocks)) * 100 if fund1_stocks else 0
            
            result.append({
                "fund1_name": fund1_name,
                "fund2_name": fund2.name,
                "overlap_percentage": overlap_percentage,
                "common_stocks": list(common_stocks)
            })
    
    # Sort by overlap percentage in descending order
    result.sort(key=lambda x: x["overlap_percentage"], reverse=True)
    
    return result