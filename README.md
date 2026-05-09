# Conversational BI

A beginner-friendly Streamlit application that turns natural-language questions into SQL queries and runs them against a sample college database. The app uses a local Ollama model to generate SQL and includes retry logic to recover from invalid queries automatically.

## Features

- Ask database questions in plain English
- Convert prompts into SQL using a local Ollama model
- Execute SQL queries on a SQLite college database
- Display generated SQL for transparency
- Show query results in a clean Streamlit table
- Retry failed SQL generation automatically

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Requests
- Ollama

## Project Structure

```text
.
|-- app.py
|-- ui.py
|-- setup_db.py
|-- college.db
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Installation

1. Clone the repository.
2. Open the project folder in your terminal.
3. Create and activate a virtual environment.
4. Install the dependencies.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ollama Setup

1. Install Ollama from [ollama.com](https://ollama.com/).
2. Start the Ollama service on your machine.
3. Pull the model used by this project:

```powershell
ollama pull llama3.2
```

The app sends requests to the default local Ollama endpoint:

```text
http://localhost:11434/api/generate
```

## How To Run

1. If you want to rebuild the sample database, run:

```powershell
python setup_db.py
```

2. Start the Streamlit app:

```powershell
streamlit run ui.py
```

3. Open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Example Questions

- Show all students with grade A
- List courses in the Computer Science department
- Count how many students are enrolled in each major
- Show students who took Database Systems

## Screenshots

Add screenshots here before publishing to GitHub:

- Home screen
- Example query input
- Generated SQL and results table

## Future Improvements

- Add query history
- Support chart visualizations for result sets
- Add database selection for multiple datasets
- Improve prompt validation and SQL safety checks
- Add downloadable CSV export

## Notes

- This project is designed to run with a local Ollama model, so no cloud API key is required.
- The included `college.db` file is a small sample database for demonstration.
