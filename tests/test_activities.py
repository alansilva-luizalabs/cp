def test_get_activities_returns_expected_payload(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")
    activities_payload = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert email in activities_payload[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")
    activities_payload = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert email not in activities_payload[activity_name]["participants"]


def test_unregister_unknown_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.signed@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == expected_location