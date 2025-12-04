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

# How to use it!
Head over to my GitHub and clone the project
<img width="1881" height="917" alt="image" src="https://github.com/user-attachments/assets/c0557e37-abf6-42c6-9c50-20ce654815d1" />
Once you have an IDE, install node.js with npm install in the client side and in the server side, follow installment on what python I ran, for example: I use an offline website ticker such as yfinance

To close the server running make sure to kill the task for python server, run: TASKKILL /F /IM python.exe

## Setup is hard, but once you have everything set up, everything should be a breeze running the requirements!

# How to run Client
To run client
cd se4390_project >> cd client >> npm run dev

<img width="1918" height="1079" alt="image" src="https://github.com/user-attachments/assets/77ff5b7b-ffac-40c8-83a4-69189abfcc47" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/ff27a5ac-f01d-4228-9e0d-a2e547e99d6b" />
<img width="1914" height="1076" alt="image" src="https://github.com/user-attachments/assets/3847e0b9-c77c-451a-aa02-28e24f40eb87" />

# Server Specification
## 1. Setup & Execution
To run server
cd se4390_project >> cd server >> python server.py 8080

## 2. Request Handling
For each client connection, accept TCP connection. parse the HTTP request (ensure it’s well-formed) and check if client IP is banned (deny if true). Processes based on method:
GET – Retrieve a file. (send_file)
HEAD – Same as GET, but without sending the body. (send_head)
POST – Upload a file to the server. (/Upload)
PUT – Update/replace an existing file on the server. (/Upload)
Return proper error messages if:
File not found → 404 Not Found. (send_404) or (send_400)
Permission denied → 403 Forbidden. (send_403)
Close the connection after serving the request. (yes)

## 3. Multithreading
Run two or three terminals and run on both terminals: python client.py 127.0.0.1 8080 index.html GET, the server should display request simultaneously
<img width="1257" height="327" alt="image" src="https://github.com/user-attachments/assets/8a5c3e0b-819a-46e1-8df3-69f083bb5aaa" />

## 4. Cookies & Visitor Tracking
When you run the main client, ONLY the news page since I made it to where we only track unique visitors for popular stock tickers
The table should contain the HOST, last_visit, and a dictionary called tickers to store visits of each tickers
To retrieve the visitors.json file, make sure you run the client, it should auto make one
<img width="1041" height="576" alt="image" src="https://github.com/user-attachments/assets/435dfb7b-82a7-4a17-9895-9e6c3ca2818e" />
<img width="1330" height="698" alt="image" src="https://github.com/user-attachments/assets/0fabf99a-c806-4174-b252-f088623a1e24" />

## 5. DoS Protection
By running python client.py 127.0.0.1 8080 index.html GET -d 200, the program allows up to 100 requests within 60 seconds, if it exceeds 100+ request, it terminates the IP until restart
To send request, run this example code. Make sure server is running with same port!
<img width="939" height="333" alt="image" src="https://github.com/user-attachments/assets/86ba09cc-e149-458d-96fb-f4093e0f5421" />
<img width="1350" height="355" alt="image" src="https://github.com/user-attachments/assets/303f7c60-3751-434f-b1c6-3e32dfe01c28" />

# Client Specification
## 1. Setup & Execution
## GET method (Retrieve)
- python client.py 127.0.0.1 8080 index.html GET
<img width="977" height="339" alt="image" src="https://github.com/user-attachments/assets/1d0bdb0d-c850-4bef-9473-5a820fe14e20" />

## HEAD method (Fetch Headers)
- python client.py 127.0.0.1 8080 index.html HEAD
<img width="970" height="372" alt="image" src="https://github.com/user-attachments/assets/af01ca5d-213a-470b-acb5-9a4ce97dc547" />

## POST method (Publish)
- python client.py 127.0.0.1 8080 test.txt POST
<img width="957" height="332" alt="image" src="https://github.com/user-attachments/assets/e3b03875-05a4-49bf-ac54-eccab5b4147a" />

## PUT method (Replace)
- python client.py 127.0.0.1 8080 test.txt PUT
<img width="964" height="333" alt="image" src="https://github.com/user-attachments/assets/c8eb246f-3c9e-40ac-b315-905d178b0064" />

## 2. Behavior
GET should automatically save the file to /Download folder
HEAD should prints only the headers
POST should upload a file that is retrieve from GET earlier you made
PUT should replace and upload file from /Download folder alongisde with POST

All of the execution after running HTTP Requests should print out in the server a connection from the IP + address


# Future Improvement
I will make sure the pages will be a lot cleaner than just a white page with JSON info. It is clear that the projection of this project is clean, but there is always better implementation!





