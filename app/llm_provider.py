from abc import ABC,abstractmethod

class LLMProvider(ABC):

    @abstractmethod
    def generate(self, message : list[dict]) -> str:
        pass