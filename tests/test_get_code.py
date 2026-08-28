from service.models import URL


async def test_get_code(client, db_session):
    """A known `short_code` redirects; an unknown one 404s."""
    short_code = "abcdef"
    long_url = "http://example.com/path"
    new_entry = URL(short_code=short_code, long_url=long_url)
    db_session.add(new_entry)
    await db_session.commit()

    response = await client.get(f"/{short_code}")
    assert response.status_code == 302
    assert response.headers["location"] == long_url

    response = await client.get("/notfound")
    assert response.status_code == 404
