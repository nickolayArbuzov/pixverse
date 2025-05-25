class Image2VideoCommand:
    def __init__(self, payload):
        self.payload = payload


class Image2VideoUseCase:

    async def execute(self, command: Image2VideoCommand):
        pass
