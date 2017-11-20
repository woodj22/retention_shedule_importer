import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

from Models.Models import Asset, Description, Pivot

Base = declarative_base()

types = {
    'asset_type': 'Asset_type',
    'asset_sub_type': 'Asset_sub_type',
    'business_function': 'Business_Function',
    'business_activity': 'Business_Activity',
    'retention_reason': 'Retention_Reason',
    'security_title': 'Security_Title',
    'action_on_expiry': 'Action_on_Expiry',
    'reason_for_action': 'Reason_For_Action',
    'appraisal_criteria': 'Appraisal_Criteria',
}

asset_attributes = [
    'asset_type',
    'asset_sub_type',
    'asset_sub_type_description',
    'business_function',
    'business_activity',
    'retention_period',
    'retention_reason',
    'security_title',
    'action_on_expiry',
    'reason_for_action',
    'appraisal_criteria',
    'authorised_by',
    'authorisation_date',
    'master',
    'classification_code',
    'notes',
    'keywords',
    ]

engine = create_engine('mysql+mysqldb://homestead:secret@192.168.10.10/homestead-test')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def import_xlsx():
    with open('retention_schedule_asset_csv.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        assetCount = 0
        pivotCount = 0
        for row in reader:
            # i = (row['authorisation_date']).split('/')[::-1]
            # auth_date = date(int(i[0]), int(i[1]), int(i[2]))

            asset = Asset(
                retention_period = row['retention_period'],
                authorised_by = row['authorised_by'],
                authorisation_date = row['authorisation_date'],
                master = row['master'],

                classification_code = row['classification_code'],
                notes = row['notes'],
                keywords = row['keywords'],
            )
            session.add(asset)
            session.commit()
            assetCount += 1
            unmatchedAssets = {}
            for type, value in types.items():

                description = session.query(Description).filter(Description.type == value).filter(Description.type_value == row[type]).first()

                if description is not None:
                    pivot = Pivot(asset_id=asset.id, description_id=description.id)
                    session.add(pivot)
                    session.commit()
                    pivotCount += 1
                else:
                    unmatchedAssets[row[type]] = type
    print(unmatchedAssets)
    print("Assets imported: ", assetCount, "Pivot joins created: ", pivotCount)

if __name__ == "__main__" :
    import_xlsx()


