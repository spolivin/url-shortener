from sqlalchemy import select

from service.models import URL


async def test_shorten(client, db_session):
    """A valid `long_url` gets a short code, persisted correctly in the DB."""
    payload = {"long_url": "http://example.com/path"}
    response = await client.post("/shorten", json=payload)
    assert response.status_code == 200

    short_code = response.json()["short_code"]
    assert len(short_code) == 6

    query = select(URL).where(URL.short_code == short_code)
    result = await db_session.execute(query)
    item = result.scalar_one_or_none()
    assert item.long_url == payload.get("long_url")


async def test_shorten_retries_exceeded(mocker, client):
    """10 straight `short_code` collisions make `/shorten` give up with 500."""
    mock_generate_code = mocker.patch("service.main.generate_base62_secret")
    mock_generate_code.return_value = "aaaaaa"
    payload = {"long_url": "http://example.com/path"}
    response = await client.post("/shorten", json=payload)
    assert response.status_code == 200
    response = await client.post("/shorten", json=payload)
    assert response.status_code == 500
    assert mock_generate_code.call_count == 11


async def test_shorten_collision_overcome(mocker, client, db_session):
    """A single `short_code` collision is retried and recovered from."""
    short_code = "aaaaaa"
    long_url = "http://example.com/path"
    new_entry = URL(short_code=short_code, long_url=long_url)
    db_session.add(new_entry)
    await db_session.commit()

    mock_generate_code = mocker.patch(
        "service.main.generate_base62_secret", side_effect=["aaaaaa", "bbbbbb"]
    )
    payload = {"long_url": long_url}
    response = await client.post("/shorten", json=payload)
    assert response.status_code == 200
    assert response.json()["short_code"] == "bbbbbb"
    assert mock_generate_code.call_count == 2
