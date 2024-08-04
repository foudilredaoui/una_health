import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import GlucoseLevel


def import_glucose_data(db: Session, directory: str):
    import os

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            user_id = filename.split(".")[0]
            filepath = os.path.join(directory, filename)
            data = pd.read_csv(filepath, skiprows=1)

            for index, row in data.iterrows():
                glucose_level = GlucoseLevel(
                    user_id=user_id,
                    timestamp=pd.to_datetime(row["Gerätezeitstempel"]),
                    glucose_value=row["Glukosewert-Verlauf mg/dL"],
                    device=row.get("Gerät"),
                    serial_number=row.get("Seriennummer"),
                )
                db.add(glucose_level)
            db.commit()
