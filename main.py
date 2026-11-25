
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


# 1. Define workflow state
class WorkflowState(TypedDict):
    topic: str
    evidence: str
    draft: str
    feedback: str
    score: int
    review_count: int
    status: str


# 2. Connect to Ollama
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# Helper function to call the LLM
def ask_llm(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content


# 3. Researcher node
def researcher(state: WorkflowState):
    print("\n[LOG] Researcher node started")

    evidence = ask_llm(
        f"Research the following topic and provide useful facts, "
        f"key points and evidence in simple language:\n{state['topic']}"
    )

    print("[LOG] Researcher node completed")
    return {"evidence": evidence, "status": "Research completed"}


# 4. Writer node
def writer(state: WorkflowState):
    print("\n[LOG] Writer node started")

    draft = ask_llm(
        f"Write a well-structured document about {state['topic']} "
        f"using the following research.\n\n"
        f"Research:\n{state['evidence']}\n\n"
        f"Reviewer feedback from previous attempt:\n{state['feedback']}\n"
        f"Write clearly with an introduction, headings and conclusion."
    )

    print("[LOG] Writer node completed")
    return {"draft": draft, "status": "Writing completed"}


# 5. Reviewer node
def reviewer(state: WorkflowState):
    print("\n[LOG] Reviewer node started")

    review = ask_llm(
        f"Review the following document on {state['topic']}.\n\n"
        f"Document:\n{state['draft']}\n\n"
        "Give constructive feedback and a score out of 10.\n"
        "Use this format:\n"
        "Score: <number>/10\n"
        "Feedback: <your feedback>"
    )

    # Extract score from review
    score = 5
    for line in review.splitlines():
        if "score:" in line.lower():
            try:
                score = int(line.split(":")[1].split("/")[0].strip())
                score = max(0, min(10, score))
                break
            except ValueError:
                pass

    print(f"[LOG] Reviewer node completed - Score: {score}/10")

    return {
        "feedback": review,
        "score": score,
        "review_count": state["review_count"] + 1,
        "status": "Review completed"
    }


# 6. Build the graph with fixed transitions
builder = StateGraph(WorkflowState)

builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

builder.add_edge(START, "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "reviewer")
builder.add_edge("reviewer", END)

graph = builder.compile()


# 7. Generate workflow diagram (Mermaid format)
diagram = """graph TD
    A([START]) --> B[Researcher]
    B --> C[Writer]
    C --> D[Reviewer]
    D --> E([END])
"""

with open("workflow.mmd", "w", encoding="utf-8") as f:
    f.write(diagram)

print("[LOG] Workflow diagram saved as workflow.mmd")


# 8. Execute the workflow
if __name__ == "__main__":
    topic = input("Enter a research topic: ")

    initial_state: WorkflowState = {
        "topic": topic,
        "evidence": "",
        "draft": "",
        "feedback": "",
        "score": 0,
        "review_count": 0,
        "status": "Started"
    }

    print("\n[LOG] Workflow execution started")

    final_state = graph.invoke(initial_state)

    # 9. Display final state
    print("\n" + "=" * 50)
    print("FINAL WORKFLOW STATE")
    print("=" * 50)

    for key, value in final_state.items():
        print(f"\n{key.upper()}:\n{value}")

    # 10. Save generated document
    with open("final_document.md", "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n")
        f.write(final_state["draft"])
        f.write("\n\n## Reviewer Feedback\n\n")
        f.write(final_state["feedback"])
        f.write(f"\n\n**Score:** {final_state['score']}/10\n")

    print("\n[LOG] Document saved as final_document.md")
    print("[LOG] Workflow execution completed successfully")
