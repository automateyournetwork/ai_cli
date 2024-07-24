import sys
import requests
import json
import time
import cli

def explain_config(user_prompt):
    url = "http://64.101.169.100:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    # Prepare the prompt for the AI
    data = {
        "model": "llama3",
        "prompt": f"The user is requesting the following Cisco IOS XE configuration from the following prompt: {user_prompt}. Please provide only the Cisco IOS XE commands with no additional text or formatting.Do not answer it as a question please simply and only provide the CLI commands. Please transform any CIDR slash notation IP addresses into their full address.",
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        
        # Wait for a maximum of 120 seconds for a response
        wait_time = 0
        while wait_time < 120 and response.status_code != 200:
            time.sleep(5)
            wait_time += 5
            response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data.get('response', '')
            return ai_response
        else:
            error_msg = f"Error: Received status code {response.status_code}, Response: {response.text}"
            return error_msg
    except Exception as e:
        return f"Exception during API call: {e}"

def extract_commands(response):
    # Check for code block markers and extract the commands within
    if "```" in response:
        commands = response.split("```")[1].strip()
    else:
        commands = response
    return commands

def configure_device(commands):
    command_list = commands.split('\n')
    current_block = []
    for command in command_list:
        command = command.strip()
        if command.startswith("interface") or not command:
            if current_block:
                # Send the current block of commands
                print(f"Configuring device with commands: {current_block}")
                cli.configurep(current_block)
                current_block = []
        if command:
            current_block.append(command)
    if current_block:
        # Send any remaining commands
        print(f"Configuring device with commands: {current_block}")
        cli.configurep(current_block)

if __name__ == "__main__":
    try:
        # Read the user's request from command line arguments
        user_prompt = ' '.join(sys.argv[1:])
        
        # Get the AI-generated configuration commands
        ai_response = explain_config(user_prompt)
        print(f"AI-generated response: {ai_response}")
        
        # Extract the CLI commands from the AI response
        config_commands = extract_commands(ai_response)
        print(f"Extracted commands: {config_commands}")
        
        # Configure the device using the Cisco CLI library
        configure_device(config_commands)
        
    except Exception as e:
        print(f"Error: {e}")
