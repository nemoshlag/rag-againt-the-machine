Usage: Run pre-commit linting
Description: Run pre-commit linting
lint:
	pre-commit run --all-files

Usage: run
Description: Run the program
run:
	streamlit run streamlit_app.py

Usage: Build docker image
Description: Build docker image
docker-build:
	docker build -t streamlit-app .

Usage: Run docker container
Description: Run docker container
docker-run:
	docker run -p 8501:8501 streamlit-app
