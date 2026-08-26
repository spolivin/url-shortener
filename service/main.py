from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .code import generate_base62_secret
from .db import get_db
from .models import URL


class ShortenRequest(BaseModel):
    long_url: HttpUrl


app = FastAPI()


@app.get("/health")
async def health(session: AsyncSession = Depends(get_db)):
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.post("/shorten")
async def shorten(payload: ShortenRequest, session: AsyncSession = Depends(get_db)):
    for _ in range(10):
        try:
            short_code = generate_base62_secret()
            new_entry = URL(short_code=short_code, long_url=str(payload.long_url))
            session.add(new_entry)
            await session.commit()
            break
        except IntegrityError:
            await session.rollback()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Number of attempts exceeded",
        )

    return {"short_code": new_entry.short_code}


@app.get("/{short_code}")
async def get_code(short_code: str, session: AsyncSession = Depends(get_db)):
    query = select(URL).where(URL.short_code == short_code)
    result = await session.execute(query)
    item = result.scalar_one_or_none()
    if item is not None:
        return RedirectResponse(url=item.long_url, status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
