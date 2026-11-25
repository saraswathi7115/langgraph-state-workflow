
import logging
import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


# -------------------------------------------------
# 1. LOGGING CONFIGURATION
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


# -------------------------------------------------
# 2. DEFINE TYPED SHARED WORKFLOW STATE
# -------------------------------------------------

class WorkflowState(TypedDict):
    topic: str
    evidence: str
    draft: str
    feedback: str
    score: int
    review_count: int
    status: str


# -------------------------------------------------
# 3. INITIALIZE OLLAMA MODEL
# -------------------------------------------------

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


def ask_llm(prompt: str) -> str:
    """Send a prompt to Ollama and return its response."""
    response = llm.invoke(prompt)
    return response.content


# -------------------------------------------------
# 4. RESEARCHER NODE
# -------------------------------------------------

def researcher(state: WorkflowState):
    logger.info("Researcher node started")

    evidence = ask_llm(
        f"""
        Act as a research assistant.

        Research the following topic:
        {state['topic']}

        Provide:
        1. Introduction
        2. Important facts
        3. Key findings
        4. Examples
        5. Reliable research points

        Use simple and clear language.
        """
    )

    logger.info("Researcher node completed")

    # Return only updated fields
    return {
        "evidence": evidence,
        "status": "Research completed"
    }


# -------------------------------------------------
# 5. WRITER NODE
# -------------------------------------------------

def writer(state: WorkflowState):
    logger.info("Writer node started")

    draft = ask_llm(
        f"""
        Act as a professional writer.

        Topic: {state['topic']}

        Research evidence:
        {state['evidence']}

        Previous reviewer feedback:
        {state['feedback']}

        Prepare a well-structured document containing:
        1. Title
        2. Introduction
        3. Main discussion with headings
        4. Examples
        5. Conclusion

        Use clear and simple language.
        """
    )

    logger.info("Writer node completed")

    # Return only updated fields
    return {
        "draft": draft,
        "status": "Writing completed"
    }


# -------------------------------------------------
# 6. REVIEWER NODE
# -------------------------------------------------

def reviewer(state: WorkflowState):
    logger.info("Reviewer node started")

    review = ask_llm(
        f"""
        Act as a professional document reviewer.

        Topic: {state['topic']}

        Document:
        {state['draft']}

        Evaluate the document for:
        1. Accuracy
        2. Clarity
        3. Organization
        4. Completeness

        Give constructive feedback.

        Your response MUST contain:
        Score: X/10
        Feedback: Your detailed feedback
        """
    )

    # Extract score from review
    match = re.search(r"Score\s*:\s*(\d+)\s*/\s*10", review, re.I)

    if match:
        score = max(0, min(10, int(match.group(1))))
    else:
        score = 0
        logger.warning("Reviewer score could not be extracted")

    logger.info("Reviewer node completed. Score: %d/10", score)

    # Return only updated fields
    return {
        "feedback": review,
        "score": score,
        "review_count": state["review_count"] + 1,
        "status": "Review completed"
    }


# -------------------------------------------------
# 7. BUILD LANGGRAPH WORKFLOW
# -------------------------------------------------

builder = StateGraph(WorkflowState)

builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

# Fixed workflow transitions
builder.add_edge(START, "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "reviewer")
builder.add_edge("reviewer", END)

graph = builder.compile()


# -------------------------------------------------
# 8. GENERATE WORKFLOW DIAGRAM
# -------------------------------------------------

def generate_workflow_diagram():
    diagram = graph.get_graph().draw_mermaid()

    with open("workflow.mmd", "w", encoding="utf-8") as file:
        file.write(diagram)

    logger.info("Workflow diagram saved as workflow.mmd")


# -------------------------------------------------
# 9. EXECUTE WORKFLOW
# -------------------------------------------------

def run_workflow(topic: str):
    initial_state: WorkflowState = {
        "topic": topic,
        "evidence": "",
        "draft": "",
        "feedback": "",
        "score": 0,
        "review_count": 0,
        "status": "Started"
    }

    logger.info("Workflow execution started")

    final_state = graph.invoke(initial_state)

    return final_state


# -------------------------------------------------
# 10. DISPLAY FINAL STATE AND SAVE DOCUMENT
# -------------------------------------------------

def display_result(final_state: WorkflowState):

    print("\n" + "=" * 60)
    print("FINAL WORKFLOW STATE")
    print("=" * 60)

    for key, value in final_state.items():
        print(f"\n{key.upper()}:\n{value}")

    print("\n" + "=" * 60)
    print("FINAL GENERATED ANSWER")
    print("=" * 60)

    print(final_state["draft"])

    with open("final_document.md", "w", encoding="utf-8") as file:
        file.write(f"# {final_state['topic']}\n\n")
        file.write(final_state["draft"])
        file.write("\n\n## Reviewer Feedback\n\n")
        file.write(final_state["feedback"])
        file.write(f"\n\n**Score:** {final_state['score']}/10\n")
        file.write(f"\n**Review Count:** {final_state['review_count']}\n")

    logger.info("Final document saved as final_document.md")
    logger.info("Workflow execution completed successfully")


# -------------------------------------------------
# 11. MAIN PROGRAM
# -------------------------------------------------

if __name__ == "__main__":

    generate_workflow_diagram()

    topic = input("\nEnter a research topic: ").strip()

    if not topic:
        print("Please enter a valid research topic.")
    else:
        try:
            final_state = run_workflow(topic)
            display_result(final_state)

        except Exception:
            logger.exception("Workflow execution failed")
