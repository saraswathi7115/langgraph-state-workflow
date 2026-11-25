
import unittest
from unittest.mock import patch

import main


class WorkflowTests(unittest.TestCase):

    # Test 1: Check graph compilation
    def test_graph_compiles(self):
        self.assertIsNotNone(main.graph)

    # Test 2: Check Researcher node
    @patch("main.ask_llm")
    def test_researcher_node(self, mock_llm):

        mock_llm.return_value = "Research evidence about AI"

        state = {
            "topic": "Artificial Intelligence"
        }

        result = main.researcher(state)

        self.assertEqual(
            result["evidence"],
            "Research evidence about AI"
        )

        self.assertEqual(
            result["status"],
            "Research completed"
        )

        self.assertEqual(
            set(result.keys()),
            {"evidence", "status"}
        )

    # Test 3: Check Writer node
    @patch("main.ask_llm")
    def test_writer_node(self, mock_llm):

        mock_llm.return_value = "AI research document"

        state = {
            "topic": "Artificial Intelligence",
            "evidence": "Research evidence",
            "feedback": ""
        }

        result = main.writer(state)

        self.assertEqual(
            result["draft"],
            "AI research document"
        )

        self.assertEqual(
            set(result.keys()),
            {"draft", "status"}
        )

    # Test 4: Check Reviewer node
    @patch("main.ask_llm")
    def test_reviewer_node(self, mock_llm):

        mock_llm.return_value = (
            "Score: 8/10\n"
            "Feedback: Good document"
        )

        state = {
            "topic": "Artificial Intelligence",
            "draft": "Test document",
            "review_count": 0
        }

        result = main.reviewer(state)

        self.assertEqual(result["score"], 8)
        self.assertEqual(result["review_count"], 1)
        self.assertEqual(result["status"], "Review completed")

        self.assertEqual(
            set(result.keys()),
            {"feedback", "score", "review_count", "status"}
        )

    # Test 5: Check complete workflow
    @patch("main.ask_llm")
    def test_complete_workflow(self, mock_llm):

        mock_llm.side_effect = [
            "Research evidence",
            "Generated document",
            "Score: 9/10\nFeedback: Excellent work"
        ]

        initial_state = {
            "topic": "Artificial Intelligence",
            "evidence": "",
            "draft": "",
            "feedback": "",
            "score": 0,
            "review_count": 0,
            "status": "Started"
        }

        final_state = main.graph.invoke(initial_state)

        self.assertEqual(final_state["evidence"], "Research evidence")
        self.assertEqual(final_state["draft"], "Generated document")
        self.assertEqual(final_state["score"], 9)
        self.assertEqual(final_state["review_count"], 1)
        self.assertEqual(final_state["status"], "Review completed")

    # Test 6: Check final workflow state
    @patch("main.ask_llm")
    def test_final_state(self, mock_llm):

        mock_llm.side_effect = [
            "Evidence",
            "Final answer",
            "Score: 8/10\nFeedback: Good work"
        ]

        result = main.run_workflow("Machine Learning")

        required_fields = [
            "topic",
            "evidence",
            "draft",
            "feedback",
            "score",
            "review_count",
            "status"
        ]

        for field in required_fields:
            self.assertIn(field, result)

        self.assertEqual(result["status"], "Review completed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
