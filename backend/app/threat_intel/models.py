"""
Pydantic models for threat intelligence API.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class IndicatorType(str, Enum):
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH = "file_hash"
    EMAIL = "email"


class ThreatType(str, Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    TROJAN = "trojan"
    RANSOMWARE = "ransomware"
    BACKDOOR = "backdoor"
    SPYWARE = "spyware"
    ADWARE = "adware"
    BOTNET = "botnet"


class ProviderData(BaseModel):
    detected: bool
    confidence: int = Field(ge=0, le=100)
    report_time: datetime
    categories: Optional[List[str]] = None


class Geolocation(BaseModel):
    country: str
    country_code: str
    city: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ASNDetails(BaseModel):
    asn: str
    name: str
    route: Optional[str] = None
    domain: Optional[str] = None


class RiskFactors(BaseModel):
    provider_scores: Dict[str, int]
    historical_reports: int
    community_reports: int
    related_threats: int


class ThreatIndicator(BaseModel):
    indicator: str
    indicator_type: IndicatorType
    risk_score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    analysis_count: int
    providers: Dict[str, ProviderData]
    geolocation: Optional[Geolocation] = None
    asn_details: Optional[ASNDetails] = None
    malware: Dict[str, int] = Field(default_factory=dict)
    threat_types: List[ThreatType] = Field(default_factory=list)
    risk_factors: Optional[RiskFactors] = None


class TrendPoint(BaseModel):
    date: datetime
    count: int
    avg_risk_score: int


class GeoDistribution(BaseModel):
    country_code: str
    count: int
    avg_score: int


class EmergingThreat(BaseModel):
    indicator: str
    indicator_type: IndicatorType
    risk_score: int
    first_seen: datetime
    malware_types: List[str]


class TrendData(BaseModel):
    time_period_days: int
    total_indicators: int
    threat_type_distribution: Dict[str, int]
    geographic_distribution: List[GeoDistribution]
    risk_score_trends: List[TrendPoint]
    emerging_threats: List[EmergingThreat]


class ProviderStats(BaseModel):
    total_reports: int
    detection_rate: float = Field(ge=0.0, le=1.0)


class SearchRequest(BaseModel):
    query: Optional[str] = None
    indicator_type: Optional[IndicatorType] = None
    min_risk_score: Optional[int] = Field(None, ge=0, le=100)
    max_risk_score: Optional[int] = Field(None, ge=0, le=100)
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)


class SearchResponse(BaseModel):
    indicators: List[ThreatIndicator]
    total_count: int
    has_more: bool