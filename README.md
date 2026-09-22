# Market & Competitor Intelligence Synthesizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture: MVC](https://img.shields.io/badge/Architecture-MVC-green.svg)](#system-architecture)
[![Model: Gemini 2.5 Flash](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-orange.svg)](#llm-synthesis-engine)

An institutional-grade decision-support platform designed for corporate strategy, product leadership, and executive offices. The synthesizer automates raw competitor data ingestion, tabular sanitization, cross-vector price benchmarking, and deterministic LLM synthesis to deliver actionable market briefs.

Developed by **Piyal**.

---

## Key Features

- **Automated Data Normalization:** Ingests unorganized CSV and Excel dumps, cleans missing data, strips currency characters, and standardizes feature schemas.
- **Operational KPI Benchmarking:** Computes dynamic metric spreads, including Floor, Mean, and Ceiling pricing distributions.
- **Cross-Competitor Pricing Variance:** Generates high-density interactive Plotly visualizations for competitive pricing elasticity.
- **Deterministic Generative Synthesis:** Integrates Google's **Gemini 2.5 Flash** using structured **Pydantic Schemas** (`response_schema`), guaranteeing 100% type-safe JSON extraction without hallucinations or markdown formatting errors.
- **Executive Institutional UI:** Clean dark-mode fintech interface engineered with pure CSS overrides and zero informal emojis.

---

## System Architecture

The project adheres strictly to the **Model-View-Controller (MVC)** architectural pattern to ensure clean separation of concerns and maintainability:

```text
market-competitor-synthesizer/
│
├── models/
│   ├── __init__.py
│   └── competitor_model.py     # Pydantic schemas, data ingestion & pandas sanitization
│
├── views/
│   ├── __init__.py
│   └── dashboard_view.py       # Custom institutional CSS, KPI rendering & Plotly UI
│
├── controllers/
│   ├── __init__.py
│   └── analysis_controller.py  # Gemini SDK client orchestration & prompt synthesis
│
├── .env                        # Local API secrets (git-ignored)
├── app.py                      # Application bootstrap & entry point
└── requirements.txt            # Locked runtime dependencies
