from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # This function is called when a request is intercepted
    print(f"Intercepted request: {flow.request.method} {flow.request.url}")
    print(f"Request headers: {flow.request.headers}")
    print(f"Request body: {flow.request.get_text()}")
    
    # Modify the request (e.g., add a header)
    flow.request.headers["X-Interceptor"] = "MyInterceptor"

def response(flow: http.HTTPFlow) -> None:
    # This function is called when a response is intercepted
    print(f"Intercepted response: {flow.response.status_code} {flow.request.url}")
    print(f"Response headers: {flow.response.headers}")
    print(f"Response body: {flow.response.get_text()}")
    
    # Modify the response (e.g., change the response body)
    flow.response.text = flow.response.text.replace("example", "intercepted")
