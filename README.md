
# LangGraph State and Workflow Designer

## Overview
This project implements a simple AI workflow using LangGraph and Ollama.
It follows a fixed sequence of three nodes: Researcher, Writer, and Reviewer.

## Workflow
START -> Researcher -> Writer -> Reviewer -> END

## Technologies Used
- Python 3.12
- LangGraph
- Ollama
- Llama 3.2 (3B)

## Nodes
- Researcher: Collects relevant information about the given topic.
- Writer: Generates a structured document based on research.
- Reviewer: Reviews the document, provides feedback, and assigns a score.

## Installation
Install the required packages:

pip install -r requirements.txt

## Run
Execute:

python main.py

Enter a topic when prompted.

## Output
- final_document.md
- workflow.mmd
