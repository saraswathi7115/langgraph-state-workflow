
# LangGraph State and Workflow Designer

## 1. Project Overview

This project implements an AI-powered Researcher-Writer-Reviewer workflow using Python, LangGraph and Ollama.

The application uses a shared typed state to manage information between three independent agent nodes.

## 2. Workflow Architecture

START -> Researcher -> Writer -> Reviewer -> END

### Researcher
- Accepts the research topic.
- Collects relevant evidence.
- Updates the shared evidence state.

### Writer
- Reads the topic and research evidence.
- Generates a structured document.
- Updates the draft state.

### Reviewer
- Evaluates the generated document.
- Provides constructive feedback.
- Assigns a score out of 10.
- Updates the review count and status.

## 3. Shared Workflow State

The application uses TypedDict to define:

- topic
- evidence
- draft
- feedback
- score
- review_count
- status

Each node returns only its updated state fields.

## 4. Technologies Used

- Python 3.12
- LangGraph
- LangChain Core
- LangChain Ollama
- Ollama
- Llama 3.2 (3B)

## 5. Installation

Install Python and Ollama.

Download the model:

ollama pull llama3.2:3b

Install Python dependencies:

pip install -r requirements.txt

## 6. Execution

Run the application:

python main.py

Enter a research topic when prompted.

## 7. Workflow Diagram

The application generates workflow.mmd using the compiled LangGraph structure.

## 8. Output

The application displays:

- Research evidence
- Generated document
- Reviewer feedback
- Review score
- Final workflow state

It also saves final_document.md.

## 9. Execution Logging

The application logs the execution status of each agent node and reports workflow completion or errors.

## 10. Testing

Run the automated tests:

python -m unittest test_workflow.py -v

The tests check:
- Graph compilation
- Researcher node
- Writer node
- Reviewer node
- Complete workflow execution
- Final state fields

Mock responses are used in tests to avoid requiring live Ollama calls.

