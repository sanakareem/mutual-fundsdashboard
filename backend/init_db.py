import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, MutualFund, Investment, FundPerformance, FundAllocation, FundHolding, FundCapAllocation
from app.core.security import get_password_hash
from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)

# Create all tables
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def init_db():
    """Initialize database with sample data"""
    try:
        # Check if data already exists
        existing_user = db.query(User).filter(User.email == "demo@example.com").first()
        if existing_user:
            print("Sample data already exists.")
            return
        
        # Create demo user
        demo_user = User(
            email="demo@example.com",
            full_name="Demo User",
            password_hash=get_password_hash("password123"),
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        
        # Create mutual funds
        mutual_funds = [
            {
                "name": "ICICI Prudential Bluechip Fund",
                "isn": "INF109K016L0",
                "fund_type": "Equity",
                "fund_category": "Large Cap",
                "fund_house": "ICICI Prudential"
            },
            {
                "name": "HDFC Top 100 Fund",
                "isn": "INF179K01YV8",
                "fund_type": "Equity",
                "fund_category": "Large Cap",
                "fund_house": "HDFC"
            },
            {
                "name": "SBI Bluechip Fund",
                "isn": "INF200K01QX4",
                "fund_type": "Equity",
                "fund_category": "Large Cap",
                "fund_house": "SBI"
            },
            {
                "name": "Axis Bluechip Fund",
                "isn": "INF846K01DP8",
                "fund_type": "Equity",
                "fund_category": "Large Cap",
                "fund_house": "Axis"
            },
            {
                "name": "Mirae Asset Large Cap Fund",
                "isn": "INF769K01AX2",
                "fund_type": "Equity",
                "fund_category": "Large Cap",
                "fund_house": "Mirae Asset"
            }
        ]
        
        # Add mutual funds to database
        db_funds = []
        for fund_data in mutual_funds:
            fund = MutualFund(**fund_data)
            db.add(fund)
            db_funds.append(fund)
        
        db.commit()
        
        # Refresh funds to get IDs
        for fund in db_funds:
            db.refresh(fund)
        
        # Create investments
        investments = [
            {
                "user_id": demo_user.id,
                "fund_id": db_funds[0].id,
                "investment_date": datetime(2023, 1, 10).date(),
                "amount_invested": 1000000,  # ₹10,00,000
                "nav_at_investment": 100,
                "units": 10000  # amount / NAV
            },
            {
                "user_id": demo_user.id,
                "fund_id": db_funds[1].id,
                "investment_date": datetime(2022, 12, 5).date(),
                "amount_invested": 800000,   # ₹8,00,000
                "nav_at_investment": 100,
                "units": 8000
            },
            {
                "user_id": demo_user.id,
                "fund_id": db_funds[2].id,
                "investment_date": datetime(2023, 2, 15).date(),
                "amount_invested": 1200000,  # ₹12,00,000
                "nav_at_investment": 100,
                "units": 12000
            },
            {
                "user_id": demo_user.id,
                "fund_id": db_funds[3].id,
                "investment_date": datetime(2022, 11, 20).date(),
                "amount_invested": 950000,   # ₹9,50,000
                "nav_at_investment": 100,
                "units": 9500
            },
            {
                "user_id": demo_user.id,
                "fund_id": db_funds[4].id,
                "investment_date": datetime(2023, 3, 1).date(),
                "amount_invested": 1100000,  # ₹11,00,000
                "nav_at_investment": 100,
                "units": 11000
            }
        ]
        
        # Add investments to database
        for investment_data in investments:
            investment = Investment(**investment_data)
            db.add(investment)
        
        db.commit()
        
        # Add fund performance data (for NAV history)
        # Generate NAV data for each fund for the past year
        start_date = datetime.now().date() - timedelta(days=365)
        end_date = datetime.now().date()
        current_date = start_date
        
        while current_date <= end_date:
            for i, fund in enumerate(db_funds):
                # Calculate NAV with some randomization to simulate market fluctuations
                days_passed = (current_date - start_date).days
                growth_factor = 1 + (days_passed / 365) * (0.1 + (i * 0.01))  # Different growth rates
                nav = 100 * growth_factor
                
                # Add performance record
                performance = FundPerformance(
                    fund_id=fund.id,
                    date=current_date,
                    nav=nav
                )
                db.add(performance)
            
            current_date += timedelta(days=1)
        
        db.commit()
        
        # Add sector allocations
        sector_allocations = [
            # ICICI Prudential Bluechip Fund
            {"fund_id": db_funds[0].id, "sector": "IT", "percentage": 38},
            {"fund_id": db_funds[0].id, "sector": "Financials", "percentage": 37},
            {"fund_id": db_funds[0].id, "sector": "Energy/Conglomerate", "percentage": 25},
            
            # HDFC Top 100 Fund
            {"fund_id": db_funds[1].id, "sector": "Financials", "percentage": 80},
            {"fund_id": db_funds[1].id, "sector": "Energy/Conglomerate", "percentage": 20},
            
            # SBI Bluechip Fund
            {"fund_id": db_funds[2].id, "sector": "Energy/Conglomerate", "percentage": 27},
            {"fund_id": db_funds[2].id, "sector": "IT", "percentage": 40},
            {"fund_id": db_funds[2].id, "sector": "Financials", "percentage": 21},
            {"fund_id": db_funds[2].id, "sector": "Industrials", "percentage": 12},
            
            # Axis Bluechip Fund
            {"fund_id": db_funds[3].id, "sector": "IT", "percentage": 50},
            {"fund_id": db_funds[3].id, "sector": "Financials", "percentage": 32},
            {"fund_id": db_funds[3].id, "sector": "Energy/Conglomerate", "percentage": 18},
            
            # Mirae Asset Large Cap Fund
            {"fund_id": db_funds[4].id, "sector": "IT", "percentage": 42},
            {"fund_id": db_funds[4].id, "sector": "Financials", "percentage": 34},
            {"fund_id": db_funds[4].id, "sector": "Energy/Conglomerate", "percentage": 24}
        ]
        
        # Add sector allocations to database
        for allocation_data in sector_allocations:
            allocation = FundAllocation(**allocation_data)
            db.add(allocation)
        
        db.commit()
        
        # Add stock holdings
        stock_holdings = [
            # ICICI Prudential Bluechip Fund
            {"fund_id": db_funds[0].id, "stock_name": "Reliance Industries", "percentage": 25},
            {"fund_id": db_funds[0].id, "stock_name": "HDFC Bank", "percentage": 22},
            {"fund_id": db_funds[0].id, "stock_name": "TCS", "percentage": 20},
            {"fund_id": db_funds[0].id, "stock_name": "Infosys", "percentage": 18},
            {"fund_id": db_funds[0].id, "stock_name": "ICICI Bank", "percentage": 15},
            
            # HDFC Top 100 Fund
            {"fund_id": db_funds[1].id, "stock_name": "HDFC Bank", "percentage": 28},
            {"fund_id": db_funds[1].id, "stock_name": "ICICI Bank", "percentage": 24},
            {"fund_id": db_funds[1].id, "stock_name": "Reliance Industries", "percentage": 20},
            {"fund_id": db_funds[1].id, "stock_name": "Kotak Mahindra Bank", "percentage": 18},
            {"fund_id": db_funds[1].id, "stock_name": "Bajaj Finance", "percentage": 10},
            
            # SBI Bluechip Fund
            {"fund_id": db_funds[2].id, "stock_name": "Reliance Industries", "percentage": 27},
            {"fund_id": db_funds[2].id, "stock_name": "TCS", "percentage": 23},
            {"fund_id": db_funds[2].id, "stock_name": "HDFC Bank", "percentage": 21},
            {"fund_id": db_funds[2].id, "stock_name": "Infosys", "percentage": 17},
            {"fund_id": db_funds[2].id, "stock_name": "Larsen & Toubro", "percentage": 12},
            
            # Axis Bluechip Fund
            {"fund_id": db_funds[3].id, "stock_name": "TCS", "percentage": 26},
            {"fund_id": db_funds[3].id, "stock_name": "Infosys", "percentage": 24},
            {"fund_id": db_funds[3].id, "stock_name": "HDFC Bank", "percentage": 22},
            {"fund_id": db_funds[3].id, "stock_name": "Reliance Industries", "percentage": 18},
            {"fund_id": db_funds[3].id, "stock_name": "State Bank of India", "percentage": 10},
            
            # Mirae Asset Large Cap Fund
            {"fund_id": db_funds[4].id, "stock_name": "Reliance Industries", "percentage": 24},
            {"fund_id": db_funds[4].id, "stock_name": "HDFC Bank", "percentage": 23},
            {"fund_id": db_funds[4].id, "stock_name": "TCS", "percentage": 22},
            {"fund_id": db_funds[4].id, "stock_name": "Infosys", "percentage": 20},
            {"fund_id": db_funds[4].id, "stock_name": "ICICI Bank", "percentage": 11}
        ]
        
        # Add stock holdings to database
        for holding_data in stock_holdings:
            holding = FundHolding(**holding_data)
            db.add(holding)
        
        db.commit()
        
        # Add market cap allocations
        cap_allocations = [
            # ICICI Prudential Bluechip Fund
            {"fund_id": db_funds[0].id, "cap_type": "Large Cap", "percentage": 98},
            {"fund_id": db_funds[0].id, "cap_type": "Mid Cap", "percentage": 2},
            {"fund_id": db_funds[0].id, "cap_type": "Small Cap", "percentage": 0},
            
            # HDFC Top 100 Fund
            {"fund_id": db_funds[1].id, "cap_type": "Large Cap", "percentage": 85},
            {"fund_id": db_funds[1].id, "cap_type": "Mid Cap", "percentage": 13},
            {"fund_id": db_funds[1].id, "cap_type": "Small Cap", "percentage": 2},
            
            # SBI Bluechip Fund
            {"fund_id": db_funds[2].id, "cap_type": "Large Cap", "percentage": 97},
            {"fund_id": db_funds[2].id, "cap_type": "Mid Cap", "percentage": 3},
            {"fund_id": db_funds[2].id, "cap_type": "Small Cap", "percentage": 0},
            
            # Axis Bluechip Fund
            {"fund_id": db_funds[3].id, "cap_type": "Large Cap", "percentage": 98},
            {"fund_id": db_funds[3].id, "cap_type": "Mid Cap", "percentage": 2},
            {"fund_id": db_funds[3].id, "cap_type": "Small Cap", "percentage": 0},
            
            # Mirae Asset Large Cap Fund
            {"fund_id": db_funds[4].id, "cap_type": "Large Cap", "percentage": 96},
            {"fund_id": db_funds[4].id, "cap_type": "Mid Cap", "percentage": 4},
            {"fund_id": db_funds[4].id, "cap_type": "Small Cap", "percentage": 0}
        ]
        
        # Add market cap allocations to database
        for cap_data in cap_allocations:
            cap_allocation = FundCapAllocation(**cap_data)
            db.add(cap_allocation)
        
        db.commit()
        
        print("Database initialized with sample data.")
        print("You can log in with:")
        print("Email: demo@example.com")
        print("Password: password123")
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()