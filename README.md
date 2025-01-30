# Prerequisites

* Python 3.13.1

# Development installation

* Create a virtual environment

`python -m venv venv`

* Switch to the virtual environment

`./venv/Scripts/activate`

* Install the dependencies

`pip install -r requirements.txt`

* Update dependencies (only in requirements.txt, install separately)

`pur -r requirements.txt`

# Run the bot

## Development

[TODO]

## Server

* Copy the docker-compose file to your server and adapt it to your needs, important sections include:
  * GOODBOI_DISCORD_TOKEN
  * GOODBOI_ANNOUNCE_GUILDS
    * If the bot should announce itself when going online, format is [GUILD1]:[CHANNEL1],[GUILD2]:[CHANNEL2]
  * REPLICATE_API_TOKEN
    * If you want to use the image generation commands
  * Potentially the volumes for the ollama image
* Copy the entrypoint.sh to the directory used in docker-compose.yml for ollama

Finally start the containers:

`docker compose up -d`

NOTE: The first start may take a while since ollama pulls the required model on first run