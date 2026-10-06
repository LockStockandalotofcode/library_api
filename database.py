from sqlmodel import create_engine, Session

filename = "database.db"
database_url = f"sqlite:///{filename}"
connect_args = {"check_same_thread": False}
# allows fastapi to use same SQLite database in different threads, since one single request could use more then one thread
# lets same connection used against Fastapi's async request handling

engine = create_engine(database_url, connect_args=connect_args)

# get session is a generator, called on request
def get_session():
    with Session(engine) as session:
        yield session