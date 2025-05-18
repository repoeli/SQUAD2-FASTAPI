import os, httpx
from fastapi import APIRouter, HTTPException
from app.models import DomainReport, DOMAIN_RX

VT_KEY = os.getenv("VT_API_KEY")
router = APIRouter(tags=["Research"])

@router.get(
    "/research_domain/{domain}",
    response_model=DomainReport,
    summary="VirusTotal domain report",
    description="Validates the FQDN then proxies VT v2 /domain/report"
)
async def research_domain(domain: str):
    if not DOMAIN_RX.fullmatch(domain):
        raise HTTPException(status_code=400, detail="invalid domain syntax")

    url = "https://www.virustotal.com/vtapi/v2/domain/report"
    params = {"apikey": VT_KEY, "domain": domain}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params, follow_redirects=True)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="VT upstream error")
    return {"domain": domain, "vt_response": r.json()}
