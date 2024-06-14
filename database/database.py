from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Float, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()

class Institution(Base):
    __tablename__ = "institutions"

    id_institution = Column("id_institution", Integer, primary_key=True)
    name = Column("name", String)

    def __init__(self, id_institution, name):
        self.id_institution = id_institution
        self.name = name


class Cuestionario(Base):
    __tablename__ = "cuestionarios"

    id_cuestionario = Column("id_cuestionario", Integer, primary_key=True, autoincrement=True)
    #id_institution = Column("id_institution", Integer, ForeignKey("institutions.id"))
    name_institution = Column("name_institution", String)
    content = Column("content", String)
    date = Column("date", DateTime)


class AudioTeoriaBD(Base):
    __tablename__ = "audioteoria"
    id_estudiante = Column("id_aspirante", Integer, primary_key=True)
    audioperceptiva = Column("audioperceptiva", Float)
    teoria = Column("teoria", Float)
    date = Column("date", DateTime)
    active = Column("active", BOOLEAN)

class Person(Base):
    __tablename__ = "persons"
    
    id_person = Column("id_monitor", Integer, primary_key=True)
    name = Column("name", String)
    group = Column("group", String)
    date = Column("date", DateTime)
    role = Column("role", String)
    active = Column("active", BOOLEAN)

class Candidate(Base):
    __tablename__ = "candidates"

    id_person = Column("Id_candidate", Integer, primary_key=True)
    name = Column("name", String)
    group = Column("group", String)
    registration_date = Column("registration_date", DateTime)
    active = Column("active", BOOLEAN)
    state = Column("state", String)
    grades_instrument = Column("grades_instrument", String)
    grades_solfeo = Column("grades_solfeo", String)
    last_change = Column("last_change", DateTime)
    description_last_change = Column("description_last_change", String)
    
def createSession():
    engine = create_engine("sqlite:///DBTEST.db?charset=utf8", echo=True, poolclass=NullPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

