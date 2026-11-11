class Chat:
    """A conversation with a model."""

    def __init__(self, llm, system):
        self.llm = llm
        self.system = system
        self.messages = []

    def send(self, text):
        """Send the user's message. Return the model's reply."""
        new_messages = self.messages + [
            {
            "role" : "user",
            "content" : text
            }
        ]

        response = self.llm.messages.create(
            system = self.system,
            messages = new_messages,
            max_tokens = 300,
        )

        self.messages = new_messages + [
            {"role" : "assistant", "content" : response.text}
        ]

        return response.text
