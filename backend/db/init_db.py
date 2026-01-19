from base import Base, engine
import models       # without this import tables would be empty


Base.metadata.create_all(bind=engine)   # Table needs initialization, error otherwise

print(Base.metadata.tables)
