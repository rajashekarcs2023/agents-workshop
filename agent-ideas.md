

---

# 🌐 Useful Agents You Can Build (Following the Stock Price Agent Pattern)

All the agents below follow a consistent architecture:

> **Natural language input → AI processing → structured parameters → API call → formatted response for the user**

Once you've built your foundational agent, you only need to swap out the **data models** and **API integration logic**, while keeping the **same messaging and processing framework**.

---

## ☁️ Weather Agent
- **Input**: Location names in natural language  
- **Output**: Current weather, forecast, alerts  
- **APIs**: 
  - [OpenWeatherMap](https://openweathermap.org/api)  
  - [Weather.gov](https://www.weather.gov/documentation/services-web-api)  
  - [AccuWeather](https://developer.accuweather.com/)  

---

## 🗞 News Summarizer
- **Input**: Topics, companies, or people in natural language  
- **Output**: Summaries of recent news articles  
- **APIs**: 
  - [NewsAPI](https://newsapi.org/)  
  - [GDELT](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)  
  - [New York Times API](https://developer.nytimes.com/)  

---

## ✈️ Flight Tracker
- **Input**: Flight numbers or routes in natural language  
- **Output**: Status, delays, gate info  
- **APIs**: 
  - [FlightAware](https://flightaware.com/commercial/firehose/firehose_documentation.rvt)  
  - [Aviationstack](https://aviationstack.com/)  
  - [Flightstats](https://developer.flightstats.com/)  

---

## 🍽 Restaurant Finder
- **Input**: Cuisine types and locations in natural language  
- **Output**: Recommendations, ratings, opening hours  
- **APIs**: 
  - [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3)  
  - [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)  
  - [TripAdvisor API](https://developer-tripadvisor.com/home)  

---

## 💱 Currency Converter
- **Input**: Currency pairs and amounts in natural language  
- **Output**: Exchange rate and converted amount  
- **APIs**: 
  - [Fixer.io](https://fixer.io/)  
  - [Open Exchange Rates](https://openexchangerates.org/)  
  - [Currency Layer](https://currencylayer.com/)  

---

## 🛍 Product Price Tracker
- **Input**: Product names in natural language  
- **Output**: Pricing, history, and retailer links  
- **APIs**: 
  - [Amazon Product API](https://affiliate-program.amazon.com/)  
  - [eBay API](https://developer.ebay.com/)  
  - Custom web scraping (e.g. with [SerpAPI](https://serpapi.com/))  

---

## 🚇 Public Transit Tracker
- **Input**: Routes or station names in natural language  
- **Output**: Arrival times, delays, disruptions  
- **APIs**: 
  - [Google Transit API](https://developers.google.com/transit)  
  - [Transit Land](https://www.transit.land/)  
  - Local city APIs  

---

## 🥘 Recipe Finder
- **Input**: Ingredients or cuisines in natural language  
- **Output**: Recipes with instructions and nutritional info  
- **APIs**: 
  - [Spoonacular](https://spoonacular.com/food-api)  
  - [Edamam](https://developer.edamam.com/)  
  - [TheMealDB](https://www.themealdb.com/api.php)  

---

## 🎬 Movie/TV Show Info
- **Input**: Show/movie titles in natural language  
- **Output**: Ratings, streaming platforms, cast, etc.  
- **APIs**: 
  - [TMDB (The Movie Database)](https://www.themoviedb.org/documentation/api)  
  - [OMDB](https://www.omdbapi.com/)  
  - [JustWatch API (unofficial)](https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/justwatch/)  

---

## 🧑‍⚕️ Health Data Tracker
- **Input**: Health metrics in natural language (e.g. "my heart rate last week")  
- **Output**: Trends, analysis, and recommendations  
- **APIs**: 
  - [Fitbit API](https://dev.fitbit.com/build/reference/web-api/)  
  - [Apple HealthKit (via iOS)](https://developer.apple.com/documentation/healthkit)  
  - [Google Fit API](https://developers.google.com/fit)  

---

## 🧠 Framework Summary

```text
Natural Language Input
        ↓
     AI Parser
        ↓
 Structured Parameters
        ↓
     API Integration
        ↓
Formatted Output for Users
```

This modular approach allows you to scale your agent ecosystem with minimal changes to the core logic — **build once, reuse everywhere**.


---

# 🧩 Useful Agents Without External APIs

You can build powerful agents using **only built-in Python capabilities or local libraries**, avoiding the need for external APIs. This makes them faster, more reliable, and easier to run offline or in secure environments.

These agents follow the **same architecture** as the Stock Price Agent:

> **Natural language input → AI processing → structured parameters → local function call → formatted response**

---

## 📊 Text Analyzer Agent
- **Function**: Analyzes input text for readability, sentiment, tone, and complexity  
- **Libraries**: `NLTK`, `TextBlob`, `textstat`, `re`  
- **Use Case**: Evaluate content quality, sentiment of feedback, or writing complexity  

---

## 🔄 File Converter Agent
- **Function**: Converts between file formats (e.g., CSV ↔ JSON, XLSX → CSV)  
- **Libraries**: `pandas`, `json`, `openpyxl`, `csv`  
- **Use Case**: Preprocessing datasets, simplifying file formats, automation workflows  

---

## 🧮 Math Problem Solver
- **Function**: Solves algebraic equations, calculus problems, and linear algebra  
- **Libraries**: `sympy`, `numpy`, `scipy`  
- **Use Case**: Homework assistance, technical calculations, symbolic math with step-by-step solutions  

---

## 📈 Data Visualization Agent
- **Function**: Generates charts (bar, pie, line, scatter) from user-provided data  
- **Libraries**: `matplotlib`, `seaborn`, `plotly`, `pandas`  
- **Use Case**: Convert tabular/natural language data into visuals, analytics helpers  

---

## 🔐 Password Generator
- **Function**: Creates strong passwords based on user-defined rules  
- **Libraries**: `random`, `string`, `secrets`  
- **Use Case**: Security tools, password hygiene, tip-based password recommendations  

---

## 🗓 Calendar/Schedule Helper
- **Function**: Calculates time between dates, finds workdays, or helps with planning  
- **Libraries**: `datetime`, `calendar`  
- **Use Case**: Task planning, calculating due dates or vacation periods  

---

## 🌍 Language Translation Agent (Offline)
- **Function**: Translates text between major languages  
- **Libraries**: `transformers`, `fairseq`, pre-trained models like `M2M100`, `NLLB`  
- **Use Case**: Private translation, basic multi-language communication  

---

## 📝 Text Summarization Agent
- **Function**: Summarizes long documents or paragraphs into concise bullet points  
- **Libraries**: `sumy`, `spacy`, `gensim` (extractive)  
- **Use Case**: Article TL;DRs, meeting note generators, content digestion  

---

## 🧵 Regular Expression Helper
- **Function**: Generates regex patterns based on descriptions; tests them on sample inputs  
- **Libraries**: `re`, `regex`  
- **Use Case**: Regex creation and debugging, pattern explanation in plain English  

---

## 📏 Unit Converter
- **Function**: Converts between units (length, temperature, volume, weight, etc.)  
- **Libraries**: `pint`, `sympy`, custom logic  
- **Use Case**: Everyday conversion needs, science and engineering helpers  

---

## ⚙️ Architecture Overview

```text
Natural Language Input
        ↓
     AI Parser
        ↓
 Structured Parameters
        ↓
 Local Python Function
        ↓
Formatted Output to User
```

By keeping everything local, these agents avoid the limitations of external APIs (like rate limits or downtime) and can be embedded into offline systems or privacy-sensitive environments.

---
