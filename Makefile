chatbot:
	python app.py

kill:
	kill -9 `lsof -t -i:9000`
