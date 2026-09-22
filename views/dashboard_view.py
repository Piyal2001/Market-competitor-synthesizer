import streamlit as st
import pandas as pd
import plotly.express as px
from models.competitor_model import ExecutiveReport


class DashboardView:

    @staticmethod
    def inject_custom_css():
        """Injects institutional, corporate analytics styling with proper top clearance."""
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                letter-spacing: -0.01em;
            }

            /* Clean up top margin and remove default Streamlit header elements */
            #MainMenu { visibility: hidden; }
            header { visibility: hidden; }
            footer { visibility: hidden; }

            .block-container {
                padding-top: 3.5rem !important;
                padding-bottom: 3.5rem !important;
                max-width: 1240px;
            }

            /* Executive Navigation / Header */
            .corporate-header {
                display: flex;
                flex-direction: column;
                border-bottom: 1px solid #1e293b;
                padding-bottom: 1.8rem;
                margin-bottom: 2rem;
            }
            .corp-meta-row {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 0.8rem;
            }
            .corp-pill {
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                padding: 4px 12px;
                border-radius: 4px;
                background: #0f172a;
                border: 1px solid #334155;
                color: #94a3b8;
            }
            .corp-live-pill {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                padding: 4px 12px;
                border-radius: 4px;
                background: rgba(14, 165, 233, 0.1);
                border: 1px solid rgba(14, 165, 233, 0.35);
                color: #38bdf8;
            }
            .corp-live-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #38bdf8;
                box-shadow: 0 0 8px #38bdf8;
            }
            .corp-title {
                font-size: 2.1rem;
                font-weight: 800;
                color: #f8fafc;
                margin: 0;
                letter-spacing: -0.03em;
            }
            .corp-subtitle {
                font-size: 0.95rem;
                color: #94a3b8;
                margin-top: 0.4rem;
                margin-bottom: 0;
                line-height: 1.5;
            }

            /* Section Headers */
            .section-header-box {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 2.2rem;
                margin-bottom: 1.1rem;
            }
            .section-tag {
                font-size: 0.72rem;
                font-weight: 800;
                color: #38bdf8;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                background: rgba(14, 165, 233, 0.1);
                border: 1px solid rgba(14, 165, 233, 0.2);
                padding: 2px 8px;
                border-radius: 4px;
            }
            .section-heading {
                font-size: 1.18rem;
                font-weight: 700;
                color: #f1f5f9;
                margin: 0;
            }

            /* Metric KPI Panels */
            .kpi-container {
                background: #090d16;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 1.25rem 1.4rem;
                border-left: 3px solid #0284c7;
            }
            .kpi-title {
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: #64748b;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }
            .kpi-value {
                font-size: 1.75rem;
                font-weight: 800;
                color: #f8fafc;
                line-height: 1.1;
            }

            /* Report Cards */
            .brief-panel {
                background: #090d16;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 1.5rem;
                height: 100%;
            }
            .brief-title {
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: #38bdf8;
                margin-bottom: 0.75rem;
            }
            .brief-body {
                color: #cbd5e1;
                font-size: 0.92rem;
                line-height: 1.65;
                margin: 0;
            }

            /* Recommendation Row */
            .rec-row {
                background: #090d16;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 1.1rem 1.4rem;
                margin-bottom: 0.75rem;
                display: flex;
                gap: 14px;
                align-items: baseline;
            }
            .rec-num {
                font-size: 0.82rem;
                font-weight: 800;
                color: #38bdf8;
                background: rgba(14, 165, 233, 0.15);
                padding: 2px 8px;
                border-radius: 4px;
            }
            .rec-text {
                font-size: 0.9rem;
                color: #e2e8f0;
                margin: 0;
                line-height: 1.55;
            }

            /* Competitor Matrix Grid Item */
            .matrix-card {
                background: #090d16;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 1.3rem;
                margin-bottom: 0.9rem;
            }
            .matrix-top {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #1e293b;
                padding-bottom: 0.6rem;
                margin-bottom: 0.75rem;
            }
            .matrix-name {
                font-size: 1rem;
                font-weight: 700;
                color: #f8fafc;
            }

            /* Status Pills */
            .pill-pos {
                background: rgba(16, 185, 129, 0.12);
                color: #10b981;
                border: 1px solid rgba(16, 185, 129, 0.25);
                padding: 2px 9px;
                border-radius: 4px;
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .pill-neg {
                background: rgba(239, 68, 68, 0.12);
                color: #ef4444;
                border: 1px solid rgba(239, 68, 68, 0.25);
                padding: 2px 9px;
                border-radius: 4px;
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .pill-neu {
                background: rgba(245, 158, 11, 0.12);
                color: #f59e0b;
                border: 1px solid rgba(245, 158, 11, 0.25);
                padding: 2px 9px;
                border-radius: 4px;
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            /* Professional Button */
            div.stButton > button:first-child {
                background: #0284c7 !important;
                color: #ffffff !important;
                border: 1px solid #0369a1 !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
                padding: 0.65rem 1.8rem !important;
                border-radius: 6px !important;
                box-shadow: none !important;
                transition: background-color 0.15s ease !important;
            }
            div.stButton > button:first-child:hover {
                background: #0369a1 !important;
            }

            /* Institutional Footer */
            .corp-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid #1e293b;
                padding: 2.2rem 0;
                margin-top: 4rem;
                font-size: 0.85rem;
                color: #64748b;
            }
            .corp-footer-left span {
                color: #f1f5f9;
                font-weight: 600;
            }
            .corp-footer-right span {
                color: #94a3b8;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def render_header():
        DashboardView.inject_custom_css()
        st.markdown(
            """
            <div class="corporate-header">
                <div class="corp-meta-row">
                    <span class="corp-pill">Strategic Intelligence Unit</span>
                    <span class="corp-live-pill"><span class="corp-live-dot"></span>Model Engine Active</span>
                </div>
                <h1 class="corp-title">Market & Competitor Intelligence Synthesizer</h1>
                <p class="corp-subtitle">Automated dataset normalization, price benchmark index, and structured executive brief synthesis.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def render_data_preview(df: pd.DataFrame):
        price_cols = [c for c in df.columns if "price" in c or "cost" in c]
        total_records = len(df)

        st.markdown(
            """
            <div class="section-header-box">
                <span class="section-tag">[01 // METRICS]</span>
                <h3 class="section-heading">Executive Benchmark Indicators</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Profiles Analyzed</div>
                    <div class="kpi-value">{total_records}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if price_cols:
            p_col = price_cols[0]
            avg_p = df[p_col].mean()
            min_p = df[p_col].min()
            max_p = df[p_col].max()

            with col2:
                st.markdown(
                    f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Mean Benchmark Price</div>
                        <div class="kpi-value">${avg_p:,.0f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Floor Pricing</div>
                        <div class="kpi-value">${min_p:,.0f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col4:
                st.markdown(
                    f"""
                    <div class="kpi-container">
                        <div class="kpi-title">Ceiling Pricing</div>
                        <div class="kpi-value">${max_p:,.0f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            with col2:
                st.markdown(f'<div class="kpi-container"><div class="kpi-title">Attributes Tracked</div><div class="kpi-value">{len(df.columns)}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="kpi-container"><div class="kpi-title">Data Status</div><div class="kpi-value">Verified</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="kpi-container"><div class="kpi-title">Ingestion Layer</div><div class="kpi-value">Structured</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabular Data Section
        st.markdown(
            """
            <div class="section-header-box">
                <span class="section-tag">[02 // INGESTION]</span>
                <h3 class="section-heading">Normalized Dataset Records</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                price_cols[0] if price_cols else "price": st.column_config.NumberColumn(
                    format="$%d"
                )
            } if price_cols else None
        )

        # Distribution Chart
        if price_cols:
            col = price_cols[0]
            name_candidates = [c for c in df.columns if "name" in c or "competitor" in c or "product" in c]
            x_axis = name_candidates[0] if name_candidates else df.columns[0]

            st.markdown(
                """
                <div class="section-header-box">
                    <span class="section-tag">[03 // DISTRIBUTION]</span>
                    <h3 class="section-heading">Cross-Competitor Pricing Variance</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            fig = px.bar(
                df,
                x=x_axis,
                y=col,
                text_auto=True,
                title=None,
                color=col,
                color_continuous_scale=["#0369a1", "#0284c7", "#38bdf8"]
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#090d16",
                font=dict(family="Plus Jakarta Sans, sans-serif", color="#94a3b8"),
                xaxis=dict(gridcolor="#1e293b", title=x_axis.replace("_", " ").upper(), tickfont=dict(size=11)),
                yaxis=dict(gridcolor="#1e293b", title="PRICE (USD)", tickfont=dict(size=11)),
                coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=10, b=10),
                bargap=0.35
            )
            fig.update_traces(marker_line_width=1, marker_line_color="#1e293b", opacity=0.95)
            st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_executive_report(report: ExecutiveReport):
        st.markdown("<br><hr style='border-color: #1e293b;'><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-box">
                <span class="section-tag">[04 // SYNTHESIS]</span>
                <h3 class="section-heading">Executive Strategic Dossier</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown(
                f"""
                <div class="brief-panel">
                    <div class="brief-title">Market Landscape & Positioning</div>
                    <p class="brief-body">{report.market_overview}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_right:
            st.markdown(
                f"""
                <div class="brief-panel">
                    <div class="brief-title">Pricing Dynamics & Elasticity</div>
                    <p class="brief-body">{report.pricing_strategy_verdict}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Strategic Directives
        st.markdown(
            """
            <div class="section-header-box">
                <span class="section-tag">[05 // ACTION ITEMS]</span>
                <h3 class="section-heading">Strategic Leadership Directives</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        for idx, rec in enumerate(report.strategic_recommendations, 1):
            st.markdown(
                f"""
                <div class="rec-row">
                    <span class="rec-num">0{idx}</span>
                    <p class="rec-text">{rec}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Competitor Matrix Breakdown
        st.markdown(
            """
            <div class="section-header-box">
                <span class="section-tag">[06 // COMPARATIVE]</span>
                <h3 class="section-heading">Competitor Matrix Analysis</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        comp_cols = st.columns(2)
        for i, item in enumerate(report.competitor_insights):
            sent = item.sentiment_rating.lower()
            if "pos" in sent:
                pill_class = "pill-pos"
            elif "neg" in sent:
                pill_class = "pill-neg"
            else:
                pill_class = "pill-neu"

            target_col = comp_cols[i % 2]
            with target_col:
                target_col.markdown(
                    f"""
                    <div class="matrix-card">
                        <div class="matrix-top">
                            <span class="matrix-name">{item.competitor_name}</span>
                            <span class="{pill_class}">{item.sentiment_rating}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.4rem;">
                            <strong style="color: #cbd5e1; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.04em;">Core Advantage:</strong><br>
                            {item.core_strength}
                        </div>
                        <div style="font-size: 0.85rem; color: #94a3b8;">
                            <strong style="color: #cbd5e1; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.04em;">Critical Gap:</strong><br>
                            {item.vulnerability}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    @staticmethod
    def render_footer():
        st.markdown(
            """
            <div class="corp-footer">
                <div class="corp-footer-left">
                    Automated Market Intelligence Platform &bull; Developed by <span>Piyal</span>
                </div>
                <div class="corp-footer-right">
                    &bull; <span>Engine: Gemini 2.5 Flash</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )