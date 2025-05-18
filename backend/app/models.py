"""
models.py  –  Pydantic-v2 / Annotated version
--------------------------------------------
Defines request- and response-models with OWASP-aligned
input validation and IDE-friendly type hints.
"""

from __future__ import annotations

import re
from typing import Annotated, Optional

from pydantic import BaseModel, Field, field_validator

# ────────────────────────────────────────────────
#  Regex helpers
# ────────────────────────────────────────────────
DOMAIN_RX: re.Pattern[str] = re.compile(
    r"^(?=.{4,253}$)([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}\.)+[A-Za-z]{2,63}$"
)
ALPHA_RX = r"^[A-Za-z]{2,60}$"

# ────────────────────────────────────────────────
#  Re-usable constrained types (Annotated)
# ────────────────────────────────────────────────
FirstName = Annotated[
    str,
    Field(
        description="Given name (letters only)",
        min_length=2,
        max_length=60,
        pattern=ALPHA_RX,
        examples=["Ada"],
    ),
]

LastName = Annotated[
    str,
    Field(
        description="Family name (letters only)",
        min_length=2,
        max_length=60,
        pattern=ALPHA_RX,
        examples=["Lovelace"],
    ),
]

LuckyNumber = Annotated[
    int,
    Field(
        description="Favourite number",
        ge=1,
        le=9_999,
        examples=[42],
    ),
]

Comment = Annotated[
    Optional[str],
    Field(
        description="Free-text note (optional)",
        max_length=140,
        examples=["auto-concat:AdaLovelace"],
    ),
]

# ────────────────────────────────────────────────
#  Item CRUD schemas
# ────────────────────────────────────────────────
class ItemIn(BaseModel):
    """
    Input model for POST/PUT.
    """

    first_name: FirstName
    last_name: LastName
    lucky_number: LuckyNumber
    comment: Comment = None  # default -> omitted if null

    # additional runtime validation example (not strictly needed
    # because regex already enforces A-Z only but shows pattern)
    @field_validator("first_name", "last_name")
    @classmethod
    def names_are_alpha(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError("Name fields must contain only A-Z letters")
        return v


class ItemOut(ItemIn):
    """
    Response model (adds DB id).
    """

    id: Annotated[int, Field(description="Auto-increment DB id", examples=[1])]


# ────────────────────────────────────────────────
#  VirusTotal /research_domain schema
# ────────────────────────────────────────────────
class DomainReport(BaseModel):
    domain: Annotated[str, Field(description="Queried FQDN", examples=["example.com"])]
    vt_response: dict
