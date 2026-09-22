import os
from typing import Any
from dotenv import load_dotenv
import pandas as pd
from google import genai
from google.genai import types
from models.competitor_model import CompetitorDataProcessor, ExecutiveReport

load_dotenv()


class AnalysisController:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not defined in environment variables.")
        self.client = genai.Client(api_key=api_key)

    def process_dataset(self, uploaded_file: Any) -> pd.DataFrame:
        """Invokes Model logic to clean raw file data."""
        return CompetitorDataProcessor.load_and_clean_data(uploaded_file)

    def generate_executive_insights(self, df: pd.DataFrame) -> ExecutiveReport:
        """Synthesizes tabular data into an ExecutiveReport using Gemini."""
        summary_stats = CompetitorDataProcessor.extract_summary_stats(df)

        # Take a representative sample (up to 30 rows) to stay within clean context boundaries
        data_preview = df.head(30).to_markdown(index=False)

        prompt = f"""
        Act as a Principal Business and Market Research Analyst. 
        Analyze the following cleaned competitor product data and synthesize it into an executive report.

        --- QUANTITATIVE METRICS ---
        {summary_stats}

        --- COMPETITOR DATA TABLE ---
        {data_preview}
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You evaluate competitor intelligence data objectively. Provide strategic, data-backed insights. "
                    "Adhere strictly to the requested JSON schema."
                ),
                response_mime_type="application/json",
                response_schema=ExecutiveReport,
                temperature=0.2,
            ),
        )

      
        if not response.text:
            raise RuntimeError("Received an empty response from Gemini API.")

        return ExecutiveReport.model_validate_json(response.text)