class Text2VideoCommand:
    def __init__(self, payload):
        self.payload = payload


class Text2VideoUseCase:

    async def execute(self, command: Text2VideoCommand):
        pass
