from unittest import TestCase

from libs.graph import ChangesGraph


class TestChangesGraph(TestCase):
    def test_changes_graph(self) -> None:
        change_graph = ChangesGraph()

        self.assertEqual(
            change_graph.generate(number_of_additions=10, number_of_deletions=0),
            "▓▓▓▓▓",
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=3, number_of_deletions=0), "▓▓▓░░"
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=0, number_of_deletions=10),
            "▒▒▒▒▒",
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=0, number_of_deletions=3), "▒▒▒░░"
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=3, number_of_deletions=2), "▓▓▓▒▒"
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=2, number_of_deletions=3), "▒▒▒▓▓"
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=10, number_of_deletions=5),
            "▓▓▓▓░",
        )
        self.assertEqual(
            change_graph.generate(number_of_additions=5, number_of_deletions=10),
            "▒▒▒▒░",
        )
