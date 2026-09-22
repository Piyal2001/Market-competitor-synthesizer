import streamlit as st
from controllers.analysis_controller import AnalysisController
from views.dashboard_view import DashboardView

st.set_page_config(page_title="Market Synthesizer", page_icon="📈", layout="wide")

def main():
    DashboardView.render_header()
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Competitor Data Spreadsheet (CSV or Excel format)", 
        type=["csv", "xlsx"]
    )
    
    if uploaded_file is not None:
        try:
            controller = AnalysisController()
            
            # Step 1: Ingest and clean using Model via Controller
            df = controller.process_dataset(uploaded_file)
            DashboardView.render_data_preview(df)
            
            # Step 2: Trigger AI Synthesis
            if st.button("Generate Executive Intelligence Report", type="primary"):
                with st.spinner("Analyzing competitor vectors and generating executive synthesis..."):
                    report = controller.generate_executive_insights(df)
                    DashboardView.render_executive_report(report)
                    
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

        DashboardView.render_footer()


if __name__ == "__main__":
    main()