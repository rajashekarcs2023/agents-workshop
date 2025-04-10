<img width="1220" alt="Screenshot 2025-04-09 at 6 48 24 PM" src="https://github.com/user-attachments/assets/3235d86b-7560-42ce-8769-6f6d8bcea0be" /># agents-workshop
# uAgents: Natural Language-Powered Agents

This repository contains implementations of two powerful AI agents built with the uAgents framework and enhanced with natural language understanding. Each agent demonstrates how to create specialized capabilities that extend the abilities of Large Language Models (LLMs).

## 🧮 Arithmetic Calculator Agent

A precision calculator agent that excels at complex numerical calculations where LLMs often struggle.

### Features

- **High-Precision Arithmetic**: Performs exact calculations with arbitrary precision
- **Natural Language Interface**: Understands questions like "Calculate 123456789 * 987654321"
- **Large Number Support**: Handles numbers far beyond what LLMs can calculate accurately
- **Advanced Operations**: Supports exponents, fractions, and complex expressions
- **Alternative Formats**: Provides binary and hex representations for integer results

### Technical Details

This agent combines:
- SymPy for symbolic mathematics and arbitrary precision
- LLM integration for natural language understanding
- Agent Chat Protocol for reliable messaging

### Example Queries

```
"Calculate 123456789 * 987654321"
"What's 2^50 + 3^30?"
"Compute 987654321^2 - 123456789^2"
```

## 📈 Stock Price Agent

A financial data agent that retrieves real-time stock information via the Alpha Vantage API.

### Features

- **Live Stock Data**: Gets current price, volume, and change information
- **Natural Language Queries**: Understands questions like "What's the price of Apple stock?"
- **Global Market Support**: Works with stocks from major exchanges worldwide
- **Detailed Information**: Provides open, high, low, close values and more
- **Change Tracking**: Shows price changes and percentage movements

### Technical Details

This agent combines:
- Alpha Vantage API integration for real-time market data
- LLM integration for company name to ticker symbol resolution
- Agent Chat Protocol for reliable messaging

### Example Queries

```
"What's the current price of Apple stock?"
"Show me the stock price for Microsoft"
"Get me IBM stock information"
```

## 🔧 Architecture

Both agents follow a modular three-component architecture:


<img width="1220" alt="Screenshot 2025-04-09 at 6 48 24 PM" src="https://github.com/user-attachments/assets/07a2823f-0848-4b00-b7c7-ab93bd5ee99a" />



1. **Core Service Module**: Implements the specialized functionality
   - `arithmetic_solver.py`: Precision calculation engine
   - `stock_price.py`: Stock data API interface

2. **Chat Protocol Module**: Handles natural language communication
   - Extracts structured data from natural language
   - Routes requests to appropriate service functions
   - Formats responses for users

3. **Agent Configuration**: Sets up protocols and connections
   - Configures rate limiting and error handling
   - Manages agent identity and addresses
   - Establishes connections to the Agentverse

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- uAgents library
- SymPy (for Arithmetic agent)
- Requests (for Stock Price agent)

### Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/uagents-examples.git
cd uagents-examples

# Install dependencies
pip install uagents sympy requests
```

### Running the Agents

```bash
# Run the Arithmetic Calculator Agent
python arithmetic_agent/agent.py

# Run the Stock Price Agent (requires API key)
# First, set your Alpha Vantage API key in stock_price.py
python stock_price_agent/agent.py
```

## 📋 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Fetch.ai](https://fetch.ai/) for the uAgents framework
- [SymPy](https://www.sympy.org/) for symbolic mathematics capabilities
- [Alpha Vantage](https://www.alphavantage.co/) for financial market data API
