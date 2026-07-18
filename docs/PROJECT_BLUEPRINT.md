# Enterprise AI Data Assistant - Project Blueprint



## Project Goal



Build a production-grade Enterprise AI Data Assistant that allows enterprise users to query company data using natural language.



Example questions:



- Which department has the highest average salary?

- Show employees hired after 2024.

- Which projects are over budget?

- Compare Engineering and Finance salaries.

- List employees reporting to Alice Johnson.



The assistant should:



1. Convert natural language into SQL.

2. Validate the generated SQL.

3. Execute SQL safely.

4. Present results as tables and charts.

5. Maintain conversation history.

6. Maintain query history.

7. Log audit events.

8. Support enterprise authentication and authorization.



The project is intended to demonstrate enterprise software engineering, AI engineering, backend development, database design, frontend development and deployment.



---



# Technology Stack



## Backend



- Python 3.11

- FastAPI

- SQLAlchemy 2.0

- PostgreSQL

- Alembic

- Pydantic

- JWT Authentication



## AI



- Google Gemini 2.5 Flash

- LangChain

- LangGraph

- FAISS

- Schema RAG



## Frontend



- React

- TypeScript

- TailwindCSS

- React Query

- Recharts



## DevOps



- Docker

- Docker Compose

- Kubernetes



## Testing



- Pytest

- httpx



---



# Architecture



React UI



↓



FastAPI Backend



↓



Authentication (JWT)



↓



LangGraph Agent



↓



SQL Validation Layer



↓



Read-only SQL Engine



↓



PostgreSQL



---



# Current Folder Structure

Enterprise-ai-data-assistant/

app/
    api/
    core/
    database/
    models/
    services/
    agents/
    rag/
    utils/
    main.py

database/
docker/
docs/
embeddings/
frontend/
kubernetes/
scripts/
tests/

.env
.env.example
README.md
CHANGELOG.md
requirements.txt

---



# Completed Milestones



## Project Initialization



Completed



- Git repository

- Virtual environment

- Requirements file

- GitHub repository



---



## Backend Foundation



Completed



- FastAPI

- Project structure

- Configuration loading

- Environment variables

- PostgreSQL connection

- SQLAlchemy engine

- Database session dependency

- Health endpoint



---



## ORM Foundation



Completed



Created:



- Base

- BaseModel



Features:



- UUID primary keys

- created_at

- updated_at



---



## Authentication Models



Completed



Models:



- Role

- User



Relationships completed.



---



## Employee Management Models



Completed



Models:



- Department

- Employee



Relationships:



- Department -> Employees

- Employee -> Department

- Employee -> Manager

- Employee -> Direct Reports



Fields include:



- salary

- employment_type

- office_location

- employee_number



---



## Alembic



Completed



- Alembic initialized

- env.py configured

- Metadata registration completed



Migration not generated yet.



---



# Current State



The project currently contains:



- FastAPI backend

- PostgreSQL connection

- SQLAlchemy ORM models

- Alembic configuration



No database tables exist yet.



No authentication exists.



No APIs exist except health.



No AI functionality exists.



No frontend exists.



---



# Permanent Architecture Decisions



## SQL Safety



Generated SQL must execute using a dedicated read-only PostgreSQL user.



Rules:



- SELECT only

- Single statement only

- No INSERT

- No UPDATE

- No DELETE

- No DROP

- No ALTER

- No CREATE

- No TRUNCATE



Enforce:



- statement timeout

- configurable row limit



Validation occurs before execution.



---



## Authentication



JWT



RBAC



No PostgreSQL Row Level Security.



Authorization occurs in FastAPI.



---



## LLM



Google Gemini 2.5 Flash.



The LLM must always be abstracted behind a service layer.



---



## Conversation Memory



LangGraph manages runtime state.



Persistent storage is PostgreSQL.



Redis is NOT part of Version 1.



---



## Database



Alembic is the only mechanism allowed for schema creation.



Never use:



Base.metadata.create_all()



---



# Remaining Milestones



## Phase 1



Initial Alembic Migration



- Generate migration

- Review migration

- Apply migration

- Verify tables



---



## Phase 2



Seed Database



Generate realistic company data.



Company:



NovaTech Solutions



Departments:



- Engineering

- Finance

- HR

- Marketing

- Sales

- Operations

- Customer Support



Generate:



- Roles

- Users

- Employees

- Departments



---



## Phase 3



Business Models



Create:



- Projects

- Budgets

- Project Assignments



Generate migration.



Seed realistic data.



---



## Phase 4



Authentication



Implement:



- JWT

- Password hashing

- Login

- Refresh token

- Current user dependency



---



## Phase 5



RBAC



Role-based permissions.



Admin



Manager



HR



Finance



Employee



---



## Phase 6



CRUD APIs



Departments



Employees



Projects



Budgets



---



## Phase 7



AI Layer



Implement:



- Schema extraction

- FAISS schema embeddings

- LangChain

- LangGraph

- SQL generation

- SQL validation

- Safe execution



---



## Phase 8



Conversation System



Implement:



- Conversation sessions

- Conversation messages

- Query history

- Audit logging



---



## Phase 9



Frontend



React



TypeScript



Tailwind



Chat interface



Dashboard



Charts



History



---



## Phase 10



Deployment



Docker



Docker Compose



Kubernetes



---



# Coding Standards



Always use:



- SQLAlchemy 2.0

- Type hints

- Mapped typing

- Dependency Injection

- PEP8

- Modular code



Never:



- Hardcode secrets

- Rewrite working code

- Modify unrelated files

- Add libraries unless requested



---



# Development Workflow



For every feature:



1. Analyze current implementation.

2. Produce implementation plan.

3. Wait for confirmation.

4. Implement.

5. Self-review.

6. Generate manual test cases.

7. Wait for review before next feature.



Never skip the planning phase.



---



# Success Criteria



The finished project should demonstrate:



- Enterprise backend architecture

- Production-grade database design

- Secure AI-generated SQL

- LangGraph orchestration

- RAG

- Authentication

- RBAC

- React frontend

- Charts

- Conversation memory

- Query history

- Audit logging

- Docker deployment

- Kubernetes deployment



The project should be of resume quality and suitable for discussion during software engineering, AI engineering and full-stack interviews.