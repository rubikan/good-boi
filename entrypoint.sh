#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "Retrieve models..."
ollama pull $OLLAMA_TXT_MODEL
echo "Done!"

# Wait for Ollama process to finish.
wait $pid