from unittest import TestCase

from libs.graph import ChangesGraph


class TestChangesGraph(TestCase):
    def test_changes_graph(self) -> None:
        change_graph = ChangesGraph()

        self.assertEqual(change_graph.generate(10, 0), "▓▓▓▓▓")
        self.assertEqual(change_graph.generate(3, 0), "▓▓▓░░")
        self.assertEqual(change_graph.generate(0, 10), "▒▒▒▒▒")
        self.assertEqual(change_graph.generate(0, 3), "▒▒▒░░")
        self.assertEqual(change_graph.generate(3, 2), "▓▓▓▒▒")
        self.assertEqual(change_graph.generate(2, 3), "▒▒▒▓▓")
        self.assertEqual(change_graph.generate(10, 5), "▓▓▓▓░")
        self.assertEqual(change_graph.generate(5, 10), "▒▒▒▒░")
