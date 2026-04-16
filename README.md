# TalentLens (Proof-of-Concept)
TalentLens is an AI tool that provides users the ability to search through data with natural language. 
TalentLens is a proof-of-concept designed for Pro-Act IT, a consultancy company with a huge database of 
consultants. However, querying over the database is very time-consuming and inefficient in many 
cases. Therefore, I developed TalentLens, which provides workers the ability to quickly retrieve 
relevant data.

## Application
For everything to work, make sure [Python 3.13](https://www.python.org/downloads/), 
[Docker](https://www.docker.com/get-started/), and [Ollama](https://ollama.com/download) 
are all installed on your computer.

## Virtual Environment
For the project, we're using a virtual environment. This is the most common and versatile way 
to start working on coding projects. We'll be using [Poetry](https://python-poetry.org/docs/). 
Poetry is a powerful tool for managing your Python dependencies and packages. You can run the 
following command to install Poetry:

```
pip install poetry
```

After you've installed poetry, you can move to wherever the project lives on your device:

```
cd ~/path/to/semantic_search
```

Then, to actually create the virtual environment, call

```
poetry install
```

To work within the environment, use

```
$(poetry env activate) # for macOS or Linux
poetry env activate # for Windows
```

Alternatively, you can use

```
poetry shell
```

## Running the Application
To run the app, you simply need to ensure Docker is running, and then call

```
docker compose up
```

Now, your app should be running at [localhost](host:8088/)

