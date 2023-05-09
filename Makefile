chatbot:
	python chatbot.py

streamlit:
	streamlit run streamlit.py

kill:
	kill -9 `lsof -t -i:8502`
