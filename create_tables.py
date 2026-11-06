from db import Base, engine
from models import User, Reports

Base.metadata.create_all(engine)

print("Tables created successfully!")