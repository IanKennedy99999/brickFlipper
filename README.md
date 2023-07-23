Brick Flipper:

A Nike to StockX Sneaker Profit Analyzer

This Python application scrapes sneaker data from the Nike and StockX websites, compares prices and sizes, and analyzes the potential profitability of buying sneakers from Nike and reselling them on StockX.

Features
Check Available Sizes on Nike: Checks for the available sizes of a particular Nike product.

Check if a Size is Available on Nike: Checks if a particular size is available for a Nike product.

Scrape StockX Data: Scrapes information about a particular shoe from the StockX website.

Get Price and Apply Discount: Gets the price of a Nike product and applies a discount if provided.

Get Highest Bids on StockX: Gets the highest bids for a product from the StockX website.

Check Profitability: Checks if buying a Nike shoe and selling it on StockX would be profitable.

Get Nike Product URLs: Gets the URLs of Nike shoes.

Convert Nike URL to StockX URL: Converts a Nike product URL to a StockX URL.

Main Function: Utilizes all the functions above to get a list of Nike shoes, check their prices and sizes, and analyze if reselling them on StockX would be profitable.

Usage
The main functionalities of the application are broken down into separate Python functions that can be run independently. Here are the main functions and how to use them:

availableSizes(url): Checks for the available sizes of a particular Nike product. Takes a URL as a parameter.

hasSize(size, url): Checks if a particular size is available for a Nike product. Takes a size and a URL as parameters.

stockx(url): Scrapes information about a particular shoe from the StockX website. Takes a URL as a parameter.

getPrice(url, discount): Gets the price of a Nike product and applies a discount if provided. Takes a URL and a discount rate as parameters.

highestBids(url): Gets the highest bids for a product from the StockX website. Takes a URL as a parameter.

check(lzt, url, number, discount): Checks if buying a Nike shoe and selling it on StockX would be profitable. Takes a list, a URL, a number, and a discount rate as parameters.

getNikes(url, number): Gets the URLs of Nike shoes. Takes a URL and a number as parameters.

getStockx(url): Converts a Nike product URL to a StockX URL. Takes a URL as a parameter.

main(number, url): The main function. Takes a number and a URL as parameters.

Before running the application, please ensure that all necessary Python libraries are installed.

Installation
The application requires Python 3 and the following Python libraries: requests, BeautifulSoup, pandas, json, and selenium. You can install these libraries using pip:

bash
Copy code
pip install requests beautifulsoup4 pandas json selenium
Contribution
Contributions are welcome! Please feel free to submit a Pull Request.
