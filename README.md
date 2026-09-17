# ◈ SQLAgent AI

### Autonomous Text-to-SQL Analytics Agent

**SQLAgent AI** is an AI-powered analytics agent that allows users to interact with a relational database using natural language.

Instead of manually writing SQL queries, users can simply ask questions such as:

> **"How many customers are there?"**

> **"Show me the top 10 customers by total spending."**

> **"Show me the total revenue by country."**

The agent uses **Gemini and LangGraph** to transform natural-language questions into SQL, execute queries safely against a read-only SQLite database, recover from SQL execution errors, summarize the results, and generate visualizations when useful.

---

## 🚀 Live Demo

### 🌐 Try SQLAgent AI

**https://sqlagent-ai.streamlit.app/**

> Ask a question. Let the agent handle the SQL.

### 💻 Source Code

**https://github.com/AbdelrhmanAkl/SQLAgent-AI**

---

## 🎯 What This Project Demonstrates

SQLAgent AI combines several modern AI engineering concepts into a single end-to-end application:

* Natural Language → SQL
* LLM-powered SQL generation
* Agentic workflow orchestration
* LangGraph state management
* SQL validation
* Read-only database execution
* Error-driven SQL self-correction
* AI-powered result summarization
* Automatic data visualization
* Streamlit deployment
* Secure API key management

The goal is not simply to generate SQL, but to build a **controlled autonomous analytics workflow** around an LLM.

---

# ✨ Key Features

## 💬 Natural Language Database Queries

Users can interact with the database using natural language.

```text
Show me the top 10 customers by total spending
```

The agent automatically determines the required tables, relationships, aggregations, filtering, and ordering.

---

## 🤖 Autonomous Agent Workflow

The application is orchestrated using **LangGraph**.

```text
User Question
      │
      ▼
Schema Inspection
      │
      ▼
SQL Generation
      │
      ▼
SQL Validation
      │
      ▼
Read-Only Execution
      │
      ├─────────────── Success ───────────────┐
      │                                       │
      │                                       ▼
      │                              Result Summarization
      │                                       │
      │                                       ▼
      │                              Visualization Check
      │                                       │
      │                                       ▼
      │                                 Final Response
      │
      └────────────── Error
                      │
                      ▼
                SQL Correction
                      │
                      ▼
                   Retry
```

This makes the system more robust than a simple one-shot Text-to-SQL pipeline.

---

# 🔄 SQL Self-Correction

SQLAgent AI can use database execution errors as feedback.

When a generated query fails:

```text
Generated SQL
      ↓
Database Execution
      ↓
Execution Error
      ↓
Error + Previous SQL
      ↓
Gemini SQL Correction
      ↓
Corrected SQL
      ↓
Database Execution
```

The retry process is controlled to prevent infinite execution loops.

### Current retry policy

```text
Maximum SQL attempts: 2
```

This means the agent can perform:

```text
Attempt 1 → Initial SQL
Attempt 2 → Corrected SQL
```

---

# 🔐 Read-Only SQL Execution

Because the application connects an LLM to a database, safe query execution is a core design requirement.

SQLAgent AI restricts generated queries to read-oriented operations.

### Allowed

```sql
SELECT ...
```

```sql
WITH ...
```

### Blocked

```text
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
REPLACE
TRUNCATE
ATTACH
DETACH
```

This keeps the application focused on **analytics and database exploration** rather than database modification.

---

# 🧠 AI-Powered Result Summarization

The raw database result is passed to a dedicated summarization stage.

For example:

```text
User:
How many customers are there?
```

Generated SQL:

```sql
SELECT COUNT(*) FROM Customer;
```

Database result:

```text
59
```

Final response:

```text
There are 59 customers.
```

The summarizer is instructed to use only information contained in the SQL result and avoid inventing facts.

---

# 📊 Automatic Visualization

SQLAgent AI analyzes the returned dataset and determines whether a visualization would be useful.

For analytical queries such as:

```text
Show me the total revenue by country
```

the system can generate a Plotly visualization from the returned data.

For simple scalar queries such as:

```text
How many customers are there?
```

the application returns the answer without creating an unnecessary chart.

---

# 🗄️ Database

The project uses the **SQLite Chinook database**, a relational sample database representing a digital music store.

The database contains tables representing entities such as:

```text
Customer
Invoice
InvoiceLine
Artist
Album
Track
Genre
Employee
Playlist
PlaylistTrack
MediaType
```

This provides a realistic relational environment for demonstrating:

* SQL generation
* JOIN operations
* Aggregations
* GROUP BY
* ORDER BY
* Filtering
* Ranking
* Revenue analytics
* Customer analytics
* Music analytics

---

# 💡 Example Queries

## 01 — Customer Analytics

```text
How many customers are there?
```

Result:

```text
There are 59 customers.
```

Generated SQL:

```sql
SELECT COUNT(*) FROM Customer;
```

---

## 02 — Customer Spending

```text
Show me the top 10 customers by total spending
```

Example generated SQL:

```sql
SELECT
    Customer.CustomerId,
    Customer.FirstName,
    Customer.LastName,
    SUM(Invoice.Total) AS TotalSpent
FROM Customer
JOIN Invoice
    ON Customer.CustomerId = Invoice.CustomerId
GROUP BY
    Customer.CustomerId,
    Customer.FirstName,
    Customer.LastName
ORDER BY TotalSpent DESC
LIMIT 10;
```

---

## 03 — Revenue Analytics

```text
Show me the total revenue by country
```

Example generated SQL:

```sql
SELECT
    BillingCountry,
    SUM(Total) AS TotalRevenue
FROM Invoice
GROUP BY BillingCountry;
```

The resulting dataset can be visualized automatically.

---

## 04 — Music Analytics

```text
Show me the most popular genres
```

The agent determines the necessary tables and SQL operations from the available database schema.

---

# 🏗️ Architecture

```text
┌──────────────────────────────┐
│            User              │
│     Natural Language Query   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        SQLAgent AI           │
│          LangGraph           │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────────┐
│   SQLite    │  │     Gemini      │
│   Schema    │  │ SQL Generation  │
└──────┬──────┘  └────────┬────────┘
       │                  │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │ SQL Validation   │
       │ & Safe Execution │
       └────────┬─────────┘
                │
         ┌──────┴──────┐
         │             │
      Success         Error
         │             │
         ▼             ▼
┌──────────────┐ ┌──────────────┐
│ Summarization│ │ SQL Correction│
└──────┬───────┘ └──────┬───────┘
       │                │
       │                └───────┐
       ▼                        │
┌──────────────┐                │
│ Visualization│                │
└──────┬───────┘                │
       │                        │
       └───────────┬────────────┘
                   ▼
          ┌─────────────────┐
          │ Final Response  │
          │ Answer + SQL +  │
          │ Results + Chart │
          └─────────────────┘
```

---

# 🧩 LangGraph Workflow

The agent is implemented as a stateful graph.

### Nodes

```text
generate_sql
      ↓
execute_sql
      ↓
correct_sql
      ↓
summarize_result
      ↓
prepare_chart
```

### Conditional execution

```text
execute_sql
     │
     ├── success → summarize_result
     │
     ├── error   → correct_sql
     │
     └── max retries → end
```

This structure provides explicit control over the agent's execution flow instead of relying on an uncontrolled LLM loop.

---

# 🛠️ Tech Stack

| Technology        | Role                                       |
| ----------------- | ------------------------------------------ |
| **Python**        | Core development                           |
| **Streamlit**     | Interactive web application                |
| **LangGraph**     | Agent workflow orchestration               |
| **LangChain**     | LLM integration                            |
| **Gemini**        | SQL generation, correction & summarization |
| **SQLite**        | Relational database                        |
| **SQLGlot**       | SQL validation                             |
| **Pandas**        | Data processing                            |
| **Plotly**        | Interactive visualization                  |
| **python-dotenv** | Local environment configuration            |

---

# 📁 Project Structure

```text
SQLAgent-AI/
│
├── app.py
│
├── database/
│   └── chinook.db
│
├── src/
│   ├── __init__.py
│   ├── graph.py
│   ├── database.py
│   ├── sql_generator.py
│   ├── summarizer.py
│   └── chart_tool.py
│
├── tests/
│
├── test_database.py
├── test_gemini.py
├── test_sql_generator.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/AbdelrhmanAkl/SQLAgent-AI.git
cd SQLAgent-AI
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Gemini

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

For Streamlit Cloud, configure the API key through **Streamlit Secrets** instead of committing it to the repository.

---

## 5. Launch the application

```powershell
streamlit run app.py
```

---

# ☁️ Deployment

SQLAgent AI is deployed using **Streamlit Community Cloud**.

### Production application

https://sqlagent-ai.streamlit.app/

The deployed application uses Streamlit Secrets for secure API-key configuration.

The Gemini API key is **not stored in the GitHub repository**.

---

# 🧪 Validation

The core application workflow has been tested locally and through the deployed Streamlit application.

A successful production query:

```text
Question:
How many customers are there?

Answer:
There are 59 customers.

SQL Attempts:
1

Visualization:
Not needed

Rows Returned:
1
```

Generated SQL:

```sql
SELECT COUNT(*) FROM Customer;
```

This validates the complete path:

```text
Natural Language
      ↓
Gemini
      ↓
SQL Generation
      ↓
Safe SQLite Execution
      ↓
Result Summarization
      ↓
Streamlit Response
```

---

# 🔒 Security Considerations

This project demonstrates a controlled architecture for connecting an LLM to a relational database.

Current protections include:

* Read-only SQL policy
* Restricted SQL operations
* Controlled retry count
* API key exclusion from Git
* Streamlit Secrets for cloud deployment
* Schema-aware SQL generation

> **Note:** This is a portfolio-grade analytics agent and should be further hardened before being connected to sensitive production databases.

---

# 🚀 Future Improvements

Planned directions include:

* Multi-database support
* PostgreSQL integration
* MySQL integration
* Conversation memory
* Multi-turn analytics
* Query history
* User authentication
* Role-based database permissions
* Advanced SQL validation
* Query cost estimation
* Streaming agent execution
* Improved chart selection
* Observability and tracing
* Production database connectors

---

# 💼 Why SQLAgent AI?

SQLAgent AI demonstrates how an LLM can be integrated into a structured software system rather than being used as a standalone chatbot.

The project combines:

```text
LLMs
  +
Agentic Workflows
  +
Databases
  +
SQL
  +
Validation
  +
Self-Correction
  +
Data Visualization
  +
Cloud Deployment
```

The result is an end-to-end **AI analytics application** capable of translating human questions into database operations and returning understandable analytical answers.

---

# 👨‍💻 Author

## Eng.Abdelrahman Ahmed Akl

**AI Engineer | AI Instructor | Agentic AI & LLMs**

Areas of focus:

```text
Artificial Intelligence
Machine Learning
Deep Learning
Natural Language Processing
Computer Vision
Large Language Models
AI Agents
Generative AI
```

### 🔗 Links

**GitHub:**
https://github.com/AbdelrhmanAkl

**SQLAgent AI Repository:**
https://github.com/AbdelrhmanAkl/SQLAgent-AI

**Live Demo:**
https://sqlagent-ai.streamlit.app/

---

## ⭐ Explore the Project

If you are interested in **Text-to-SQL, LLM applications, AI agents, or intelligent data analytics**, feel free to explore the source code and try the live application.

### ◈ SQLAgent AI

**Ask your database. Let the agent handle the SQL.**
