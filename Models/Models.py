from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Description(Base):
    __tablename__ = 'retention_schedule_descriptions'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    type_value = Column(String)

    def __repr__(self):
        return "<User(id='%s', type='%s', type_value='%s')>" % (self.id, self.type, self.type_value)

class Pivot(Base):
    __tablename__ = 'retention_schedule_assets_descriptions'
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer)
    description_id = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', asset_id='%s', description_id='%s')>" % (self.id, self.asset_id, self.description_id)

class Asset(Base):
    __tablename__ = 'retention_schedule_assets'
    id = Column(Integer, primary_key=True)
    retention_period = Column(String)
    authorised_by = Column(String)
    authorisation_date = Column(String)
    master = Column(String)
    classification_code = Column(String)
    notes = Column(String)
    keywords = Column(String)
