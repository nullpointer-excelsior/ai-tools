include .env

paste-summarize:
	export OPENAI_API_KEY="$(OPENAI_API_KEY)"; pbpaste | python src/main.py summarize | jq


summarize:
	export OPENAI_API_KEY="$(OPENAI_API_KEY)";python src/main.py summarize "$(t)" | jq
