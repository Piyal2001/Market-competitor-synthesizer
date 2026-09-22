from typing import Any, Dict, List
import pandas as pd
from pydantic import BaseModel, Field


class CompetitorInsight(BaseModel):
    competitor_name: str = Field(description="Name of the competitor")
    core_strength: str = Field(description="Primary market advantage or feature")
    vulnerability: str = Field(description="Reported weakness, gap, or negative feedback")
    sentiment_rating: str = Field(description="Positive, Neutral, or Negative")


class ExecutiveReport(BaseModel):
    market_overview: str = Field(description="A concise 2-3 sentence executive summary of the landscape")
    pricing_strategy_verdict: str = Field(description="Assessment of pricing trends and tiers")
    strategic_recommendations: List[str] = Field(description="3 actionable recommendations for product leadership")
    competitor_insights: List[CompetitorInsight] = Field(description="Structured breakdowns per competitor")


class CompetitorDataProcessor:
    """Handles raw data ingestion and standard Pandas sanitization."""

    @staticmethod
    def load_and_clean_data(uploaded_file: Any) -> pd.DataFrame:
        """Reads CSV or Excel and applies foundational cleanup."""
        file_name = getattr(uploaded_file, "name", "")
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Standardize column names (strip spaces, lowercase, replace spaces with underscores)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

        # Drop fully empty rows
        df.dropna(how="all", inplace=True)

        # Fill missing values for core textual attributes
        object_columns = df.select_dtypes(include=["object"]).columns
        for col in object_columns:
            df[col] = df[col].fillna("Not Specified").astype(str).str.strip()

        # Clean pricing if present (removes currency symbols like $, ₹ and converts to float)
        price_cols = [c for c in df.columns if "price" in c or "cost" in c]
        for col in price_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[^\d.]", "", regex=True)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).astype(float)

        return df

    @staticmethod
    def extract_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """Extracts basic quantitative metrics for prompt injection."""
        summary: Dict[str, Any] = {
            "total_records": int(len(df))
        }

        price_cols = [c for c in df.columns if "price" in c or "cost" in c]
        if price_cols:
            col = price_cols[0]
            summary["avg_price"] = round(float(df[col].mean()), 2)
            summary["min_price"] = round(float(df[col].min()), 2)
            summary["max_price"] = round(float(df[col].max()), 2)
            summary["price_column"] = str(col)

        return summary