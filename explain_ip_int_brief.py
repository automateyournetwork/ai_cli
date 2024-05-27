import sys
import requests
import json
import time

def explain_config(config):
    #url = "http://localhost:11434/api/generate"
    url = "http://64.101.169.100:11434/api/generate"
    
    headers = {
        "Content-Type": "application/json"
    }
    # Replace newline characters with spaces
    sanitized_config = config.replace('\n', ' ').replace('\r', '')
    data = {
    #    "model": "phi3",
        "model": "llama3",
        "prompt": f"Analyze Cisco IOS XE show ip interface brief command output: {sanitized_config}",
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Wait for a maximum of 120 seconds for a response
        wait_time = 0
        while wait_time < 0 and response.status_code != 200:
            print("Waiting for response...")
            time.sleep(5)
            wait_time += 5
            response = requests.post(url, headers=headers, data=json.dumps(data))
              
        if response.status_code == 200:
            response_data = response.json()
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
        file_path = "/flash/guest-share/ip_int_brief_output.txt"  # Correct path in Guestshell
        with open(file_path, 'r') as file:
            raw_config = file.read()
              
        explanation = explain_config(raw_config)
        print(f"Explanation: {explanation}")
        
    except Exception as e:
        error_msg = f"Error: {e}"
        print(error_msg)  # Print any exceptions during the script execution
