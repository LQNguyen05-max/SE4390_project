# Stock News Analytics Website

## 1. Detailed Description of the Project

This project is a Stock News Analytics Website powered by a custom HTTP/1.0 web server written from scratch in Python. The server handles basic HTTP methods (GET, HEAD, POST, PUT) and serves both static files (HTML, CSS) and dynamic financial news content. Users can enter stock ticker symbols (e.g., AAPL, TSLA, NVDA) to view related news articles. The server tracks visitor activity using cookies, recording visit counts, last visit times, and searched tickers. An analytics page (`/stats`) summarizes site usage, including unique visitors, total requests, and popular stock searches. This project demonstrates how a lightweight, extensible web server can deliver meaningful data services by combining networking fundamentals with real-world use cases.

## 2. Relation to the Networking Course

This project applies key networking concepts from the course:

- **HTTP Protocol Implementation:** Building the server at the application layer using HTTP/1.0.
- **Socket Programming:** Enabling client–server communication.
- **Concurrency:** Using multithreading to handle multiple simultaneous requests.
- **Session Management:** Tracking users with cookies.
- **Security:** Logging requests and detecting DoS attacks.
- **Browser Compatibility:** Ensuring the server works with standard web browsers.

By bridging theory and practice, the project connects protocol knowledge to web technology applications.

## 3. Risks and Mitigation

- **Protocol Implementation Risk:** Misinterpreting HTTP/1.0 could cause incorrect responses.
  - _Mitigation:_ Test with multiple browsers and HTTP clients (curl, Postman).
- **Concurrency Issues:** Multithreading may introduce race conditions or thread-safety problems.
  - _Mitigation:_ Use thread synchronization and test under simulated load.
- **Data Availability Risk:** Reliance on live APIs may fail due to rate limits or outages.
  - _Mitigation:_ Maintain a fallback local dataset of sample news articles.
- **Security Risks:** Vulnerability to denial-of-service (DoS) attacks.
  - _Mitigation:_ Monitor request rates and block abusive IPs.
- **Performance Risk:** Dynamic content may slow under high traffic.
  - _Mitigation:_ Optimize logging and cache frequently requested data.

## 4. Final Objectives

By project completion, the server and website will:

- Correctly handle GET, HEAD, POST, and PUT HTTP methods.
- Be compatible with major browsers (Chrome, Firefox, Safari).
- Support concurrent connections via multithreading.
- Use cookies to track visitor activity (visit count, last visit time).
- Dynamically serve stock news articles by ticker symbol.
- Provide an analytics page summarizing visitors, requests, and trending stocks.
- Detect and mitigate simple DoS attacks by blocking abusive IPs.
- Include a custom HTTP client for testing uploads, downloads, and stress scenarios.
- Include pages that represents stock analysis to show feeds to issue stock-related activities.

(Apparently in terminal, the @- is treating as a operator)

# Client Side

GET method

- python client.py 127.0.0.1 8080 index.html GET

HEADER method

# Server Side

# Testing GET method

# Testing POST method

echo "hello world" > test.txt
Get-Content test.txt -Raw | curl -x POST --data-binary "@-" http://127.0.0.1:8080/Upload/test.txt

# Testing PUT method

- echo "old" > test.txt
- Get-Content test.txt -Raw | curl.exe -X PUT --data-binary "@-" http://127.0.0.1:8080/Upload/test.txt
