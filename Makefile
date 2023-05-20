include .env

paste-summarize:
	export OPENAI_API_KEY="$(OPENAI_API_KEY)"; pbpaste | python src/summarize.py 

summarize:
	export OPENAI_API_KEY="$(OPENAI_API_KEY)";python src/summarize.py "$(t)" 

run-restaurant-api:
	uvicorn src.apis.restaurants:app --reload --port 8000

run-app:
	export OPENAI_API_KEY="$(OPENAI_API_KEY)";python src/main.py  
	
run-script:
	export OPENAI_API_KEY="$(OPENAI_API_KEY)";python src/$(s).py
