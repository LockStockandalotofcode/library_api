import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from sqlmodel.pool import StaticPool


load_dotenv()
filename = "database.db"
DATABASE_URL = os.getenv("DATABASE_URL", default="sqlite:///./database.db")
print(f"\n\n\nthe current database is : {DATABASE_URL}\n\n\n")

# postgres does not require this setting done manually
connect_args = {}
engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    if ":memory:" in DATABASE_URL:
        engine_kwargs["poolclass"] = StaticPool
# allows fastapi to use same SQLite database in different threads, since one single request could use more then one thread
# lets same connection used against Fastapi's async request handling

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True, **engine_kwargs)

# get session is a generator, called on request
def get_session():
    with Session(engine) as session:
        yield session