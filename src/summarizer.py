import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


class ResultSummarizer:
    """Convert SQL results into concise natural-language answers."""

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            try:
                api_key = st.secrets.get("GOOGLE_API_KEY")
            except Exception:
                api_key = None

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY was not found in environment variables "
                "or Streamlit Secrets."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.7-flash",
            temperature=0,
            google_api_key=api_key,
        )

    def _extract_text(self, response) -> str:
        content = response.content

        if isinstance(content, list):
            text_parts = []

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

            return "".join(text_parts).strip()

        return str(content).strip()

    def _handle_llm_error(self, exc):
        error_message = str(exc)

        if (
            "RESOURCE_EXHAUSTED" in error_message
            or "429" in error_message
            or "quota" in error_message.lower()
        ):
            raise RuntimeError(
                "Gemini API quota has been exhausted. "
                "Please wait for the quota to reset or use an "
                "available Gemini API plan/model."
            ) from exc

        raise exc

    def summarize(
        self,
        question: str,
        sql: str,
        result: list,
    ) -> str:
        prompt = f"""
You are an analytics assistant.

Answer the user's question using the SQL result.

USER QUESTION:
{question}

SQL QUERY:
{sql}

SQL RESULT:
{result}

RULES:
1. Answer directly and clearly.
2. Use only information present in the SQL result.
3. Do not invent facts.
4. Do not mention internal implementation details.
5. Keep the answer concise.
6. If the result contains a single number, explain what that number represents.
"""

        try:
            response = self.llm.invoke(prompt)
        except Exception as exc:
            self._handle_llm_error(exc)

        return self._extract_text(response)