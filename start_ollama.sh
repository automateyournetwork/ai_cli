#!/bin/bash

# Stop Ollama service if it's already running
sudo systemctl stop ollama

# Set proxy settings
export http_proxy=http://proxy.esl.cisco.com:8080/
export https_proxy=http://proxy.esl.cisco.com:8080/
export HTTP_PROXY=http://proxy.esl.cisco.com:8080/
export HTTPS_PROXY=http://proxy.esl.cisco.com:8080/

# Set Ollama directories
export OLLAMA_MODELS=/data/ollama/models/
sudo mkdir -p /data/ollama/tmp
sudo chown -R $USER:$USER /data/ollama/tmp
sudo chmod -R 755 /data/ollama/tmp
export OLLAMA_TMPDIR=/data/ollama/tmp

# Start Ollama server in the background
ollama serve &

# Start phi3 model in the background
# Assuming you have a command to start phi3 model, replace `phi3_serve` with the actual command
ollama run phi3 &

echo "Ollama and phi3 models are started and running in the background."
