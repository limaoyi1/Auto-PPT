import json

from langchain.memory import RedisChatMessageHistory
from langchain.schema.messages import BaseMessage, _message_to_dict, messages_from_dict


def extract_first_and_last_two_lines(input_string):
    lines = input_string.strip().split('\n')
    first_line = lines[0] if lines else ''
    last_two_lines = lines[0] if len(lines) >= 1 else ''
    return first_line, last_two_lines


def starts_with_please(input_string):
    return input_string.startswith("this is my (旅行者的) new question :")


class MyRedisChatMessageHistory(RedisChatMessageHistory):
    def add_message(self, message: BaseMessage) -> None:
        """Your custom implementation of add_message method."""
        # Add your custom code here
        # For example, you can perform additional processing or logging before adding the message to Redis.
        # To call the original add_message method from the parent class, you can use super().

        # For this example, let's simply print the message content before adding it to Redis.

        # Call the original add_message method to store the message in Redis.
        #  对message 进行处理 删除多余的信息
        if starts_with_please(message.content):
            first_line, last_two_lines = extract_first_and_last_two_lines(message.content)
            content1 = last_two_lines.replace("this is my (旅行者的) new question :", "")
            message.content = content1
        self.redis_client.lpush(self.key, json.dumps(_message_to_dict(message)))
        if self.ttl:
            self.redis_client.expire(self.key, self.ttl)

        # Add any additional logic after the message has been added to Redis (if needed).
        # For instance, you can log a success message or perform other actions.

# Now, you can use MyRedisChatMessageHistory instead of RedisChatMessageHistory
# to take advantage of your custom add_message method.
