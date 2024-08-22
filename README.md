# SSTI Vulnerability Checker

This project demonstrates how to identify Server-Side Template Injection (SSTI) vulnerabilities in web applications. It uses a Flask application as a demo target, intercepts HTTP requests using `mitmproxy`, and tests for potential SSTI vulnerabilities.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [References](#references)

## Overview

This project consists of three main components:
1. **Flask Application (`SSTI-vul.py`)**: A simple web application vulnerable to SSTI.
2. **Interceptor (`interceptor.py`)**: A `mitmproxy` script to capture and modify HTTP requests and responses.
3. **Checker (`checker.py`)**: A script to detect SSTI vulnerabilities by sending payloads and analyzing responses.

## Prerequisites

- Python 3.x
- `pip` (Python package manager)
- `mitmproxy` for intercepting and modifying HTTP traffic

## Setup

1. **Clone the Repository:**
   ```bash    
   git clone https://github.com/your-username/ssti-vulnerability-checker.git
   cd ssti-vulnerability-checker
    ```

2. **Install Required Packages:**
   Install the dependencies listed in `requirements.txt`.
    ```bash
   pip install -r requirements.txt
    ```
3. **Install `mitmproxy`:**
   Follow the official mitmproxy installation guide for your operating system.

## Usage

### Step 1: Run the Flask Application
Start the vulnerable Flask application by running:
```bash
python SSTI-vul.py
```
The application will be accessible at http://127.0.0.1:5000.

### Step 2: Intercept the Request
Launch mitmproxy with the custom interceptor script:
```bash
mitmproxy -s interceptor.py
```
In your browser, navigate to http://127.0.0.1:5000 and submit the form.

Observe the captured request in the mitmproxy interface.

Export the captured request to a file named `request.txt`:

- In the mitmproxy interface, select the captured request.
- Press `e` to export and save it as `request.txt`.

### Step 3: Test for SSTI Vulnerabilities
Run the checker script to see if the captured request is vulnerable to SSTI:
```bash
python checker.py
```
The script will analyze the request, test for various template engines, and report if any vulnerabilities are found. If a vulnerability allows command execution, it will be highlighted.

## References

- [mitmproxy Installation Guide](https://mitmproxy.org/docs/latest/overview-installation)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SSTI Vulnerabilities](https://owasp.org/www-community/attacks/Server-Side_Template_Injection)
