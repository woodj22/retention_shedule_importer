import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

types = [
    'asset_type',
    'asset_sub_type',
    'business_function',
    'business_activity',
    'retention_reason',
    'security_title',
    'action_on_expiry',
    'reason_for_action',
    'appraisal_criteria'
     ]


asset_attributes = [
    'retention_period'
    'retention_reason' 
    'security_title'
    'authorised_by'
    'authorisation_date'
    'master' 
    'classification_code'
    'notes'
    'keywords'
    ]

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
    retention_reason = Column(String)
    security_title = Column(String)
    authorised_by = Column(String)
    authorisation_date = Column(String)
    master = Column(String)
    classification_code = Column(String)
    notes = Column(String)
    keywords = Column(String)


engine = create_engine('mysql+mysqldb://homestead:secret@192.168.10.10/homestead')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def import_csv(filepath):

        reader = csv.DictReader(open(filepath, encoding='utf-8-sig'))
        for row in reader:

            asset = Asset(retention_period = row['retention_period'],
                retention_reason = row['retention_reason'],
                security_title = row['security_title'],
                authorised_by = row['authorised_by'],
                authorisation_date = row['authorisation_date'],
                master = row['master'],
                classification_code = row['classification_code'],
                notes = row['notes'],
                keywords = row['keywords'],)
            session.add(asset)
            session.commit()
            ids = [get_description_type_id(type, row[type]) for type in types if row[type] is not None]

            pivots = [Pivot(asset_id = asset.id, description_id = id) for id in ids if id is not None]

            session.add_all(pivots)
            session.commit()







def get_description_type_id(type, type_value):
    id= session.query(Description.id).filter_by(type=type, type_value=type_value).first()
    if id is not None:
        return id[0]


filepath = "/Users/BBCWood/Desktop/schedule_data_export.csv"
import_csv(filepath)




# print(d)
