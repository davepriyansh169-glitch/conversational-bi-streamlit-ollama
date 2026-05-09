import sqlite3
import requests

DB_PATH = "college.db"

def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
    
SCHEMA = """
Tables in the database:
students(id, name, age, major, enrollment_year)
courses(id, title, credits, department)
grades(student_id, course_id, grade, semester)
Relationships:
- grades.student_id links to students.id
- grades.course_id links to courses.id
"""

def nl_to_sql(question, error_feedback=None):

    if error_feedback:
        prompt = f"""
You are an SQL expert. The following SQL query caused an error.
Fix it so it works correctly.

Schema:
{SCHEMA}

Previous SQL that failed:
{error_feedback['sql']}

Error message:
{error_feedback['error']}

Return ONLY the corrected SQL query. No explanation. No markdown. No backticks.
"""
    else:
        prompt = f"""
You are an SQL expert. Convert the following question to a valid SQL query.

Schema:
{SCHEMA}

Rules:
- Return ONLY the SQL query
- No explanation
- No markdown
- No backticks
- Use only the tables and columns listed in the schema above

Question: {question}
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
   
        json={
            "model": "llama3.2",
            
            "prompt": prompt,
           
            "stream": False
           
        }
    )
   
    result = response.json()
   
    sql = result["response"].strip()
    return sql
def run_query(question):
   
    MAX_RETRIES = 3
   
    last_sql = None
   
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        print(f"\n🔄 Attempt {attempt} of {MAX_RETRIES}")
       
        if attempt == 1:
            sql = nl_to_sql(question)

        else:
            sql = nl_to_sql(question, error_feedback={
                "sql": last_sql,
                "error": last_error
            })
            
        last_sql = sql
        print(f"📝 Generated SQL: {sql}")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            results = [dict(row) for row in rows]
            return {
                "success": True,
                "sql": sql,
                "results": results,
                "attempts": attempt,
            }
        except Exception as e:
            
            last_error = str(e)
            print(f"❌ Error on attempt {attempt}: {last_error}")
            
            if attempt == MAX_RETRIES:
                return {
                    "success": False,
                    "sql": last_sql,
                    "error": last_error,
                    "attempts": attempt
                }
            
