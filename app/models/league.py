"""League (competition) schema."""

from pydantic import BaseModel


class League(BaseModel):
    code: str
    name: str
    country: str
    country_code: str
    emblem: str | None = None