import requests
from uagents import Model, Field

API_KEY = "your_api_key"
BASE_URL = "https://www.alphavantage.co/query"

class StockPriceRequest(Model):
    """Model for requesting stock price data"""
    symbol: str = Field(description="Stock symbol (e.g., IBM, AAPL, MSFT)")

class StockPriceResponse(Model):
    """Model for stock price response data"""
    results: str

async def get_stock_price(symbol: str) -> str:
    """
    Fetch stock price information from Alpha Vantage API
    
    Args:
        symbol: Stock symbol to get price for
        
    Returns:
        Formatted string with stock price information
    """
    try:
        # Build request parameters for the Quote Endpoint
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        # Check if we got valid data
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            
            # Format the response
            result = f"📈 STOCK PRICE: {symbol.upper()} 📈\n\n"
            result += f"Price: ${quote.get('05. price', 'N/A')}\n"
            result += f"Change: {quote.get('09. change', 'N/A')} ({quote.get('10. change percent', 'N/A')})\n"
            result += f"Volume: {quote.get('06. volume', 'N/A')}\n"
            result += f"Trading Day: {quote.get('07. latest trading day', 'N/A')}\n"
            result += f"Previous Close: ${quote.get('08. previous close', 'N/A')}\n"
            result += f"Open: ${quote.get('02. open', 'N/A')}\n"
            result += f"High: ${quote.get('03. high', 'N/A')}\n"
            result += f"Low: ${quote.get('04. low', 'N/A')}\n"
            
            return result
        else:
            # Handle error or no data scenario
            error_message = data.get("Note", data.get("Information", "No data found for this symbol"))
            return f"Could not retrieve stock price for {symbol}.\n\n{error_message}"
            
    except Exception as e: 
        return f"Error fetching stock price information: {str(e)}"