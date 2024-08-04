from datetime import datetime
from unittest.mock import patch

import pytest
from app.db.core import get_db
from app.db.models import Base, GlucoseLevel
from app.main import app
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for testing
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Create a new database session for each test
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def get_test_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


def create_test_data(db):
    # Create test data for your tests
    db.add(
        GlucoseLevel(
            user_id=1,
            timestamp=datetime(2024, 8, 4, 10, 0, 0),
            glucose_value=90,
            device="DeviceA",
            serial_number="SN123",
        )
    )
    db.add(
        GlucoseLevel(
            user_id=1,
            timestamp=datetime(2024, 8, 4, 11, 0, 0),
            glucose_value=110,
            device="DeviceB",
            serial_number="SN124",
        )
    )
    db.add(
        GlucoseLevel(
            user_id=1,
            timestamp=datetime(2024, 8, 4, 10, 0, 0),
            glucose_value=110,
            device="DeviceB",
            serial_number="SN125",
        )
    )
    db.add(
        GlucoseLevel(
            user_id=2,
            timestamp=datetime(2024, 8, 4, 11, 0, 0),
            glucose_value=110,
            device="DeviceB",
            serial_number="SN125",
        )
    )
    db.commit()


# test for GET /api/v1/levels/
def test_get_glucose_levels(client, db):
    # Insert test data
    create_test_data(db)

    response = client.get(
        "/api/v1/levels/", params={"user_id": 1, "sort_order": "desc"}
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["glucose_value"] == 110
    assert response.json()[1]["glucose_value"] == 90

    # filter by date
    response = client.get(
        "/api/v1/levels/",
        params={
            "user_id": 1,
            "start_timestamp": datetime(2024, 8, 4, 11, 0, 0),
        },
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["timestamp"] >= str(
        datetime(2024, 8, 4, 11, 0, 0)
    )

    # pagination
    response = client.get(
        "/api/v1/levels/", params={"user_id": 1, "limit": 2, "offset": 1}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["glucose_value"] == 110
    assert response.json()[1]["glucose_value"] == 110


# Hypothesis test
@given(
    user_id=st.integers(min_value=1, max_value=1000),
    timestamp=st.datetimes(
        min_value=datetime(2000, 1, 1), max_value=datetime(2100, 12, 31)
    ),
    glucose_value=st.floats(min_value=0, max_value=300),
    device=st.text(min_size=1, max_size=50),
    serial_number=st.text(min_size=1, max_size=50),
)
@settings(
    max_examples=10,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_get_glucose_levels_with_hypothesis(
    user_id, timestamp, glucose_value, device, serial_number
):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        client = TestClient(app)
        level = GlucoseLevel(
            user_id=user_id,
            timestamp=timestamp,
            glucose_value=glucose_value,
            device=device,
            serial_number=serial_number,
        )
        db.add(level)
        db.commit()

        response = client.get("/api/v1/levels/", params={"user_id": user_id})
        assert response.status_code == 200
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# Test for GET /api/v1/levels/{id}
def test_get_glucose_level_by_id(client, db):
    # Insert test data
    level = GlucoseLevel(
        user_id=1,
        timestamp=datetime(2024, 8, 4, 10, 0, 0),
        glucose_value=90,
        device="DeviceA",
        serial_number="SN123",
    )
    db.add(level)
    db.commit()

    response = client.get(f"/api/v1/levels/{level.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["glucose_value"] == 90
    assert data["device"] == "DeviceA"
    assert data["serial_number"] == "SN123"

    # get glucose level by id not found
    response = client.get("/api/v1/levels/999")
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


# Hypothesis test for GET /api/v1/levels/{id}
@given(
    user_id=st.integers(min_value=1, max_value=1000),
    timestamp=st.datetimes(
        min_value=datetime(2000, 1, 1), max_value=datetime(2100, 12, 31)
    ),
    glucose_value=st.floats(min_value=0, max_value=300),
    device=st.text(min_size=1, max_size=50),
    serial_number=st.text(min_size=1, max_size=50),
)
@settings(
    max_examples=10,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_get_glucose_level_by_id_with_hypothesis(
    user_id, timestamp, glucose_value, device, serial_number
):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        client = TestClient(app)
        level = GlucoseLevel(
            user_id=user_id,
            timestamp=timestamp,
            glucose_value=glucose_value,
            device=device,
            serial_number=serial_number,
        )
        db.add(level)
        db.commit()

        response = client.get(f"/api/v1/levels/{level.id}")
        assert response.status_code == 200
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
