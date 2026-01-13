import openai
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam, ChatCompletionAssistantMessageParam, ChatCompletionToolMessageParam, ChatCompletionUserMessageParam;

class LLmClient:
    def __init__(self, model: str):
        self.model = model
        self.history: list[ChatCompletionMessageParam] = []

    def add_user_message(self, message: str):
        self.history.append(ChatCompletionUserMessageParam(content=message, role="user"))

    def add_assistant_message(self, message: ChatCompletionAssistantMessageParam):
        self.history.append(message)
        
    def add_tool_message(self, message: ChatCompletionToolMessageParam):
        self.history.append(message)
        
    def complete_chat(self, tools = []) -> ChatCompletion:
        return openai.chat.completions.create(
            model=self.model,
            messages=self.history,
            tools=tools,
            tool_choice="auto",
            parallel_tool_calls=False
        )
