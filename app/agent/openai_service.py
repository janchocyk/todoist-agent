import json
import re
from typing import Any, Dict
from loguru import logger
from langfuse.openai import openai


class OpenAIService:
    def __init__(self):
        self.default_model = "gpt-4o"

    async def completion(
        self, config: Dict[str, Any], only_content: bool = True
    ) -> Dict[str, Any]:
        """
        Calls OpenAI API to get a chat completion.

        Parameters:
        - config (Dict[str, Any]): Dictionary containing parameters such as 'messages', 'model', 'stream', and 'jsonMode'.

        Returns:
        - OpenAI response in JSON format.
        """
        messages = config.get("messages", [])
        model = config.get("model", self.default_model)
        stream = config.get("stream", False)
        json_mode = config.get("jsonMode", False)
        name = config.get("name", "test")
        temperature = config.get("temperature", 0)
        metadata = config.get("metadata", None)

        response_format = {"type": "json_object"} if json_mode else {"type": "text"}

        try:
            response = openai.chat.completions.create(
                name=name,
                model=model,
                temperature=temperature,
                messages=messages,
                stream=stream,
                response_format=response_format,
                metadata=metadata,
            )
            openai.flush_langfuse()
            if only_content:
                return response.choices[0].message.content
            return response
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    @staticmethod
    def parse_json_response(response: str) -> Dict[str, Any]:
        try:
            response = response.strip()
            return json.loads(response)
        except json.JSONDecodeError:
            pattern1 = r"```json\s*(\{.*?\})\s*```"
            pattern2 = r"```json\s*(\[.*?\])\s*```"
            match1 = re.search(pattern1, response, re.DOTALL)
            match2 = re.search(pattern2, response, re.DOTALL)
            if match1:
                try:
                    return json.loads(match1.group(1))
                except json.JSONDecodeError as e:
                    logger.error(f"Błąd podczas parsowania JSON: {e}")
            elif match2:
                try:
                    return json.loads(match2.group(1))
                except json.JSONDecodeError as e:
                    logger.error(f"Błąd podczas parsowania JSON: {e}")
            return {"error": "Invalid JSON format"}
