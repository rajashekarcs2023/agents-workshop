# Innovation Lab Fetch AI Workshop : Build and Launch your agents on Agentverse
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
  

---

# 🧠 Agent Architecture Overview

Our system is composed of **three main components**, each with a clearly defined role. Together, they create a seamless pipeline from **natural language input** to **expert-level output**.

---

## 📂 `service_file.py` (e.g. `stock_price.py`, `arithmetic_solver.py`)

> **"The EXPERT who knows how to do one specific job really well."**

- Does not understand natural language.
- Excellent at a **specialized task**: stock prices, math, conversions, etc.
- Works best with structured, unambiguous input.

**🔧 Analogy**: Think of this as a **calculator** or **financial analyst** — incredibly skilled at their job, but not conversational.

---

## 💬 `chat_proto.py`

> **"The TRANSLATOR who speaks both human language and technical language."**

- Accepts **natural language input** from the user.
- Uses AI or parsing logic to extract **intents and parameters**.
- Talks to the appropriate EXPERT and formats the response for users.

**🧠 Analogy**: Like a **personal assistant** who understands you and knows how to get help from experts behind the scenes.

---

## 🧩 `agent.py`

> **"The MANAGER who makes sure everything runs smoothly."**

- Handles orchestration and routing of requests.
- Manages timeouts, error handling, and resource control.
- Ensures a smooth handoff between the TRANSLATOR and EXPERTS.

**📋 Analogy**: Acts like an **office manager**, ensuring the right expert is consulted and everything stays organized.

---

# 🔄 Step-by-Step Example: Stock Price Request

Let’s walk through a real request:

### 🗣 User Input:
> *"What's the price of MSFT stock?"*

---

### 1. **The TRANSLATOR (`chat_proto.py`) receives the message**
- Understands this is a request for stock information.

### 2. **TRANSLATOR uses an AI model to extract key parameters**
- Identifies `"MSFT"` as the ticker symbol.

### 3. **TRANSLATOR sends this to the EXPERT (`stock_price.py`)**
- Passes `"MSFT"` as a structured input.

### 4. **The EXPERT queries an external API (e.g., Alpha Vantage)**
- Retrieves live stock data: price, daily change, etc.

### 5. **The TRANSLATOR receives the raw data**
- Converts it into a clear, human-readable message.

---

### ✅ Final Output to User:
> **"Microsoft stock is currently trading at $415.25, up 1.2% today."**

---

## 🔁 Summary of Roles

| Component        | Role Description                          | Analogy                     |
|------------------|--------------------------------------------|-----------------------------|
| `service_file.py` | Specialist function (stock, math, etc.)   | Calculator / Analyst        |
| `chat_proto.py`   | Natural language interpreter + formatter  | Personal Assistant          |
| `agent.py`        | System orchestrator and manager           | Office Manager              |

---


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
