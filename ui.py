import streamlit as st
import pandas as pd
from app import run_query

st.set_page_config(
    page_title="Conversational BI",
    layout="wide"
  )
st.title("Conversational BI — College Database")

st.markdown("""
Ask questions about the college database in plain English.
The app converts your question to SQL, runs it, and shows the results.
""")

st.divider()
with st.sidebar:
    st.header("Database Schema")
    st.markdown("""
    **students**
    - id, name, age, major, enrollment_year

    **courses**
    - id, title, credits, department

    **grades**
    - student_id, course_id, grade, semester
    """)

question = st.text_input(
    label="Ask a question:",
    placeholder="e.g. Show all students with grade A",

)

submit = st.button("Run Query")

if submit and question:
    with st.spinner("Thinking... converting to SQL and running query..."):

        result = run_query(question)

    if result["success"]:
        st.success(f" Query ran successfully in {result['attempts']} attempt(s)")

        if result["attempts"] > 1:
            st.info(f" Retry logic kicked in — took {result['attempts']} attempts to get correct SQL")

        st.subheader("Generated SQL")
        st.code(result["sql"], language="sql")

        st.subheader("Results")

        if result["results"]:

            df = pd.DataFrame(result["results"])
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(result['results'])} row(s) returned")

        else:
            st.warning(" Query ran successfully but returned no results")
    else:
        st.error(f"Query failed after {result['attempts']} attempt(s)")
        st.subheader("Last SQL Attempted")
        st.code(result["sql"], language="sql")
        st.subheader("Error")
        st.code(result["error"])
        