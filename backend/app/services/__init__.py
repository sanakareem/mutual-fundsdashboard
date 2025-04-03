# Import service functions to make them accessible through the module
from .auth import authenticate_user, create_user, get_password_hash, verify_password, create_access_token
from .mutual_fund import get_mutual_funds, get_mutual_fund_by_id, get_mutual_fund_performances
from .investment import create_investment, get_investments_by_user, get_investment_by_id
from .portfolio import get_portfolio_summary, get_portfolio_performance, get_portfolio_composition, get_fund_overlap