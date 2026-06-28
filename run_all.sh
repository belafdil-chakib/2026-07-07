#!/bin/bash
set -e # Exit immediately if a pipeline returns a non-zero status

# 1. Start Ollama and wait for socket availability
echo "Starting Ollama server..."
ollama serve > /var/log/ollama.log 2>&1 &

echo "Waiting for Ollama API to respond..."
while ! curl -s http://127.0.0.1:11434/api/tags > /dev/null; do
    sleep 0.5
done
echo "Ollama is ready. Pulling model..."
ollama pull deepseek-r1:1.5b

# 2. Setup Virtual Environment Context
VENV_PATH="/workdir/.venv"
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "Error: Virtual environment not found at $VENV_PATH" >&2
    exit 1
fi

# 3. Start Open-WebUI via the active venv context
echo "Starting open-webui..."
if command -v open-webui &> /dev/null; then
    open-webui serve &
else
    echo "Error: open-webui binary not found in virtual environment." >&2
    exit 1
fi

# 4. Start Jupyter Notebook
echo "Starting Jupyter Notebook..."
if command -v jupyter &> /dev/null; then
    exec jupyter notebook --ip=0.0.0.0 --port=8889 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
else
    echo "Error: jupyter binary not found in virtual environment." >&2
    exit 1
fi