from src.app import activities


def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert set(data["Chess Club"].keys()) == expected_keys


def test_signup_adds_new_participant(client, sample_activity_name, sample_email):
    # Arrange
    participants_before = list(activities[sample_activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": sample_email},
    )

    # Assert
    assert response.status_code == 200
    assert sample_email in activities[sample_activity_name]["participants"]
    assert len(activities[sample_activity_name]["participants"]) == len(participants_before) + 1


def test_signup_returns_400_for_duplicate_email(client, sample_activity_name):
    # Arrange
    existing_email = activities[sample_activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client, sample_email):
    # Arrange
    unknown_activity = "Unknown Club"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": sample_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_existing_participant(client, sample_activity_name):
    # Arrange
    existing_email = activities[sample_activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 200
    assert existing_email not in activities[sample_activity_name]["participants"]


def test_unregister_returns_404_for_missing_participant(client, sample_activity_name):
    # Arrange
    missing_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_404_for_unknown_activity(client, sample_email):
    # Arrange
    unknown_activity = "Unknown Club"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants",
        params={"email": sample_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
