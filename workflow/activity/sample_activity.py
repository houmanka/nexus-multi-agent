import logging

from dataclasses import dataclass

from temporalio import activity

logging.basicConfig(level=logging.INFO)


@dataclass
class SampleInput:
    name: str


class HelloActivity:
    def __init__(self) -> None:
        pass

    @activity.defn
    async def say_hello(self, input: SampleInput) -> str:
        logging.info(f"Hello {input.name}")
        return f"Hello, {input.name}!"