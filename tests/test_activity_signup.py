import pytest


def test_signup_successfully_registers_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }

    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email_query_param(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


@pytest.mark.xfail(reason="Capacity enforcement is expected but not implemented yet")
def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Debate Team"
    full_roster = [f"student{i}@mergington.edu" for i in range(12)]

    # Fill the activity to capacity before acting.
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert activities[activity_name]["max_participants"] == 12

    from src.app import activities as activities_store

    activities_store[activity_name]["participants"] = full_roster

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


@pytest.mark.xfail(reason="Email format validation is expected but not implemented yet")
def test_signup_rejects_invalid_email_format(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "not-an-email"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": invalid_email})

    # Assert
    assert response.status_code == 422
