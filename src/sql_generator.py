import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


class SQLGenerator:
    """Generate and correct safe read-only SQL queries."""

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

    def _clean_sql(self, sql: str) -> str:
        sql = sql.strip()

        if sql.startswith("```sql"):
            sql = sql[len("```sql"):].strip()

        if sql.startswith("```"):
            sql = sql[len("```"):].strip()

        if sql.endswith("```"):
            sql = sql[:-3].strip()

        return sql

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

    def generate_sql(self, question: str, schema: str) -> str:
        prompt = f"""
You are an expert SQLite Text-to-SQL system.

Convert the user's natural language question into ONE valid SQLite query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

STRICT RULES:
1. Generate ONLY a SELECT or WITH query.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, REPLACE, TRUNCATE, ATTACH, or DETACH.
3. Use only tables and columns that exist in the schema.
4. Do not invent tables or columns.
5. Return ONLY the SQL query.
6. Do not use markdown code fences.
7. Do not include explanations.
"""

        try:
            response = self.llm.invoke(prompt)
        except Exception as exc:
            self._handle_llm_error(exc)

        return self._clean_sql(
            self._extract_text(response)
        )

    def correct_sql(
        self,
        question: str,
        schema: str,
        previous_sql: str,
        error: str,
    ) -> str:
        prompt = f"""
You are an expert SQLite SQL debugging agent.

The previous SQL query failed during execution.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

PREVIOUS SQL:
{previous_sql}

DATABASE ERROR:
{error}

Your task is to fix the SQL query.

STRICT RULES:
1. Return ONE valid SQLite query.
2. The query MUST be SELECT or WITH.
3. Never use INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, REPLACE, TRUNCATE, ATTACH, or DETACH.
4. Use only tables and columns that exist in the schema.
5. Correct the query based on the database error.
6. Return ONLY the corrected SQL.
7. Do not use markdown code fences.
8. Do not include explanations.
"""

        try:
            response = self.llm.invoke(prompt)
        except Exception as exc:
            self._handle_llm_error(exc)

        return self._clean_sql(
            self._extract_text(response)
        )