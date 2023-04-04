from settings import DARK_SHADE, EMPTY, LIGHT_SHADE, MEDIUM_SHADE


class ChangesGraph:
    def __init__(self, max_value: int = 5, format_width: int = 1) -> None:
        self.max_value = max_value
        self.format_width = format_width
        self.addition_character = DARK_SHADE
        self.deletion_character = MEDIUM_SHADE
        self.format_character = LIGHT_SHADE

    def return_string_graph(self, value: int, character: str) -> str:
        if value >= self.max_value:
            return character * self.max_value
        string_graph = character * value
        return string_graph.ljust(self.max_value, self.format_character)

    def generate(self, number_of_additions: int, number_of_deletions: int) -> str:
        number_of_changes = number_of_additions + number_of_deletions

        is_one_zero = 0 in [number_of_additions, number_of_deletions]
        is_additions_larger = number_of_additions > number_of_deletions

        if number_of_changes <= self.max_value:
            additions = number_of_additions * self.addition_character
            deletions = number_of_deletions * self.deletion_character
            string_graph = EMPTY.join(
                sorted([additions, deletions], key=len, reverse=True)
            )
            if len(string_graph) < self.max_value:
                return string_graph.ljust(self.max_value, self.format_character)
            return string_graph

        if is_one_zero:
            if is_additions_larger:
                return self.return_string_graph(
                    number_of_additions, self.addition_character
                )
            return self.return_string_graph(
                number_of_deletions, self.deletion_character
            )

        colored_character_width = self.max_value - self.format_width
        if is_additions_larger:
            return self.return_string_graph(
                colored_character_width, self.addition_character
            )
        return self.return_string_graph(
            colored_character_width, self.deletion_character
        )
