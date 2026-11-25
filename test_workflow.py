
import unittest
import main


class WorkflowTests(unittest.TestCase):

    def test_graph_compiles(self):
        self.assertIsNotNone(main.graph)

    def test_researcher_node(self):
        main.ask_llm = lambda prompt: "Test research evidence"

        result = main.researcher({"topic": "AI"})

        self.assertEqual(result["evidence"], "Test research evidence")
        self.assertEqual(result["status"], "Research completed")

    def test_writer_node(self):
        main.ask_llm = lambda prompt: "Test draft document"

        result = main.writer({
            "topic": "AI",
            "evidence": "Test evidence",
            "feedback": ""
        })

        self.assertEqual(result["draft"], "Test draft document")

    def test_reviewer_node(self):
        main.ask_llm = lambda prompt: "Score: 8/10\nFeedback: Good work"

        result = main.reviewer({
            "topic": "AI",
            "draft": "Test draft",
            "feedback": "",
            "review_count": 0
        })

        self.assertEqual(result["score"], 8)
        self.assertEqual(result["review_count"], 1)


if __name__ == "__main__":
    unittest.main()
