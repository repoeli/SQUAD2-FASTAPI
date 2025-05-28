"""
Mock data provider for testing threat intelligence endpoints.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional
from app.threat_intel.models import IndicatorType, ThreatType

class MockDataProvider:
    """Provides mock data for testing threat intelligence endpoints."""
    
    @staticmethod
    def get_mock_indicator(indicator: str, indicator_type: IndicatorType) -> Dict[str, Any]:
        """Generate a mock indicator with risk score and other details."""
        return {
            "indicator": indicator,
            "indicator_type": indicator_type,
            "risk_score": random.randint(0, 100),
            "confidence": random.randint(50, 95),
            "last_updated": datetime.now() - timedelta(hours=random.randint(1, 48)),
            "risk_factors": {
                "provider_scores": {
                    "virustotal": random.randint(0, 100),
                    "abuseipdb": random.randint(0, 100),
                    "otx": random.randint(0, 100)
                },
                "historical_reports": random.randint(1, 10),
                "community_reports": random.randint(0, 50),
                "related_threats": random.randint(0, 5)
            },
            "threat_types": random.sample(
                [t.value for t in ThreatType], 
                k=random.randint(1, 3)
            )
        }
    
    @staticmethod
    def get_mock_trend_data(days: int, indicator_type: Optional[IndicatorType] = None) -> Dict[str, Any]:
        """Generate mock trend data for threat intelligence."""
        today = datetime.now()
        
        # Generate trend points
        trend_points = []
        for i in range(days):
            day = today - timedelta(days=i)
            trend_points.append({
                "date": day,
                "count": random.randint(5, 50),
                "avg_risk_score": random.randint(30, 80)
            })
        
        # Generate type distribution
        type_distribution = {}
        if not indicator_type:
            for t in IndicatorType:
                type_distribution[t.value] = random.randint(10, 100)
        
        # Generate geographic distribution
        geo_distribution = []
        country_codes = ["US", "CN", "RU", "DE", "GB", "FR", "JP", "BR", "IN", "CA"]
        for country in random.sample(country_codes, k=min(len(country_codes), random.randint(3, 8))):
            geo_distribution.append({
                "country_code": country,
                "count": random.randint(5, 50),
                "avg_score": random.randint(30, 80)
            })
        
        # Generate emerging threats
        emerging_threats = []
        threat_indicators = [
            "192.168.1.1", "example.com", "malicious.exe", 
            "bad.domain.com", "10.10.10.10", "evil.php"
        ]
        threat_types = ["ip", "domain", "file_hash", "domain", "ip", "url"]
        
        for i in range(min(len(threat_indicators), random.randint(3, 5))):
            emerging_threats.append({
                "indicator": threat_indicators[i],
                "indicator_type": threat_types[i],
                "risk_score": random.randint(60, 95),
                "first_seen": today - timedelta(days=random.randint(1, 7)),
                "malware_types": random.sample(
                    ["trojan", "ransomware", "backdoor", "spyware", "adware"],
                    k=random.randint(1, 3)
                )
            })
        
        return {
            "time_period_days": days,
            "total_indicators": sum(point["count"] for point in trend_points),
            "threat_type_distribution": type_distribution,
            "geographic_distribution": geo_distribution,
            "risk_score_trends": trend_points,
            "emerging_threats": emerging_threats
        }
    
    @staticmethod
    def get_mock_search_results(limit: int = 10) -> List[Dict[str, Any]]:
        """Generate mock search results for threat indicators."""
        indicators = []
        
        indicator_samples = [
            ("8.8.8.8", "ip"),
            ("1.1.1.1", "ip"),
            ("example.com", "domain"),
            ("malware.com", "domain"),
            ("https://evil.com/malware.exe", "url"),
            ("44d88612fea8a8f36de82e1278abb02f", "file_hash"),
            ("192.168.1.1", "ip"),
            ("phishing.site", "domain"),
            ("https://bad.com/page", "url"),
            ("e6a7cd654a2f4ab58cd466eeaae16b8b", "file_hash")
        ]
        
        # Use a smaller number of samples if limit is small
        samples_to_use = min(len(indicator_samples), limit)
        
        for i in range(samples_to_use):
            indicator, indicator_type = indicator_samples[i]
            
            # Provider data
            providers = {}
            provider_names = ["virustotal", "abuseipdb", "otx", "urlscan"]
            
            for provider in random.sample(provider_names, k=random.randint(1, len(provider_names))):
                providers[provider] = {
                    "detected": random.choice([True, False]),
                    "confidence": random.randint(0, 100),
                    "report_time": datetime.now() - timedelta(hours=random.randint(1, 72))
                }
            
            # Geolocation data if it's an IP
            geolocation = None
            if indicator_type == "ip":
                geolocation = {
                    "country": "United States",
                    "country_code": "US",
                    "city": "Ashburn",
                    "region": "Virginia",
                    "latitude": 39.0438,
                    "longitude": -77.4874
                }
            
            # ASN details if it's an IP
            asn_details = None
            if indicator_type == "ip":
                asn_details = {
                    "asn": "AS15169",
                    "name": "Google LLC",
                    "route": "8.8.8.0/24",
                    "domain": "google.com"
                }
            
            # Create indicator
            indicators.append({
                "indicator": indicator,
                "indicator_type": indicator_type,
                "risk_score": random.randint(0, 100),
                "first_seen": datetime.now() - timedelta(days=random.randint(1, 30)),
                "last_seen": datetime.now() - timedelta(hours=random.randint(0, 48)),
                "analysis_count": random.randint(1, 20),
                "providers": providers,
                "geolocation": geolocation,
                "asn_details": asn_details,
                "malware": {
                    "trojan": random.randint(0, 10),
                    "spyware": random.randint(0, 5),
                    "ransomware": random.randint(0, 3)
                } if random.choice([True, False]) else {}
            })
        
        return indicators
