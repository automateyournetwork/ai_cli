import sys
import requests
import json
import time

def explain_config(config):
    url = "http://64.101.169.100:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    # Replace newline characters with spaces
    sanitized_config = config.replace('\n', ' ').replace('\r', '')
    data = {
        "model": "llama3",
        "prompt": f"You are a network security expert. Please analyze the following Cisco IOS XE running-configuration with a technical focus on security analysis, best practices, and security configuration. Please report back a list of security risks or vulnerabilitys as well as what is being done well in the configuration from a security perspective: {sanitized_config}",
        "stream": False
    }

    try:
        print(f"Sending request to {url} with data: {json.dumps(data)}")  # Debug: Print request data
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Wait for a maximum of 120 seconds for a response
        wait_time = 0
        while wait_time < 0 and response.status_code != 200:
            print("Waiting for response...")
            time.sleep(5)
            wait_time += 5
            response = requests.post(url, headers=headers, data=json.dumps(data))
        
        print(f"Response status code: {response.status_code}")  # Debug: Print response status code
        print(f"Response text: {response.text}")  # Debug: Print response text
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response received: {response_data}")  # Debug: Print the response data
            ai_response = response_data.get('response', '')
            return ai_response
        else:
            error_msg = f"Error: Received status code {response.status_code}, Response: {response.text}"
            print(error_msg)  # Debug: Print status code and response text if not 200
            return error_msg
    except Exception as e:
        exception_msg = f"Exception during API call: {e}"
        print(exception_msg)  # Debug: Print any exceptions during the API call
        return exception_msg

if __name__ == "__main__":
    try:
        file_path = "/flash/guest-share/show_run_output.txt"  # Correct path in Guestshell
        with open(file_path, 'r') as file:
            raw_config = file.read()
              
        explanation = explain_config(raw_config)
        print(f"Explanation: {explanation}")
        
    except Exception as e:
        error_msg = f"Error: {e}"
        print(error_msg)  # Print any exceptions during the script execution
