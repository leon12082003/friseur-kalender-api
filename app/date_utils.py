from fastapi import APIRouter, Request
from datetime import datetime
import dateparser

router = APIRouter()

@router.post("/resolve-datum")
async def resolve_datum(request: Request):
    data = await request.json()
    text = data.get("text")

    if not text:
        return {"resolved_date": None}

    parsed_date = dateparser.parse(
        text,
        languages=["de"],
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.now()
        }
    )

    if parsed_date:
        return {"resolved_date": parsed_date.strftime("%Y-%m-%d")}
    else:
        return {"resolved_date": None}
