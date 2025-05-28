"""
Threat Intelligence API Router
"""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.threat_intel.models import (
    IndicatorType, 
    ThreatIndicator, 
    TrendData, 
    SearchRequest, 
    SearchResponse,
    ProviderStats
)
from app.threat_intel.mock_data import MockDataProvider

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/threat-intel", tags=["Threat Intelligence"])


@router.get(
    "/risk-score/{indicator_type}/{indicator}",
    response_model=ThreatIndicator,
    summary="Get risk score for an indicator",
    description="Analyze an indicator and return its risk score with threat intelligence data"
)
async def get_risk_score(
    indicator: str,
    indicator_type: IndicatorType
):
    """
    Get comprehensive threat intelligence for a specific indicator.
    
    Args:
        indicator: The indicator to analyze (IP, domain, URL, hash, etc.)
        indicator_type: Type of the indicator
        
    Returns:
        Comprehensive threat intelligence data including risk score
    """
    try:
        # In a real implementation, this would query multiple threat intel providers
        # For now, we'll use mock data
        logger.info(f"Analyzing {indicator_type} indicator: {indicator}")
        
        result = MockDataProvider.get_mock_indicator(indicator, indicator_type)
        
        return ThreatIndicator(**result)
        
    except Exception as e:
        logger.error(f"Error analyzing indicator {indicator}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze indicator: {str(e)}"
        )


@router.get(
    "/trends",
    response_model=TrendData,
    summary="Get threat intelligence trends",
    description="Retrieve threat intelligence trends and statistics for a specified time period"
)
async def get_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    indicator_type: Optional[IndicatorType] = Query(None, description="Filter by indicator type")
):
    """
    Get threat intelligence trends and analytics.
    
    Args:
        days: Number of days to include in the trend analysis
        indicator_type: Optional filter by indicator type
        
    Returns:
        Trend data including counts, distributions, and emerging threats
    """
    try:
        logger.info(f"Fetching trends for {days} days, type: {indicator_type}")
        
        result = MockDataProvider.get_mock_trend_data(days, indicator_type)
        
        return TrendData(**result)
        
    except Exception as e:
        logger.error(f"Error fetching trends: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch trend data: {str(e)}"
        )


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search threat indicators",
    description="Search for threat indicators with various filters"
)
async def search_indicators(request: SearchRequest):
    """
    Search for threat indicators based on various criteria.
    
    Args:
        request: Search parameters including query, filters, and pagination
        
    Returns:
        List of matching indicators with metadata
    """
    try:
        logger.info(f"Searching indicators with query: {request.query}")
        
        # Get mock search results
        indicators_data = MockDataProvider.get_mock_search_results(request.limit)
        
        # Apply filters if specified
        filtered_results = []
        for indicator_data in indicators_data:
            # Filter by indicator type
            if request.indicator_type and indicator_data["indicator_type"] != request.indicator_type:
                continue
                
            # Filter by risk score range
            risk_score = indicator_data["risk_score"]
            if request.min_risk_score is not None and risk_score < request.min_risk_score:
                continue
            if request.max_risk_score is not None and risk_score > request.max_risk_score:
                continue
                
            # Filter by query string (simple contains check)
            if request.query and request.query.lower() not in indicator_data["indicator"].lower():
                continue
                
            filtered_results.append(ThreatIndicator(**indicator_data))
        
        # Apply pagination
        start_idx = request.offset
        end_idx = start_idx + request.limit
        paginated_results = filtered_results[start_idx:end_idx]
        
        return SearchResponse(
            indicators=paginated_results,
            total_count=len(filtered_results),
            has_more=end_idx < len(filtered_results)
        )
        
    except Exception as e:
        logger.error(f"Error searching indicators: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search indicators: {str(e)}"
        )


@router.get(
    "/providers/stats",
    response_model=dict,
    summary="Get provider statistics",
    description="Get statistics about threat intelligence providers"
)
async def get_provider_stats():
    """
    Get statistics about threat intelligence providers.
    
    Returns:
        Dictionary with statistics for each provider
    """
    try:
        logger.info("Fetching provider statistics")
        
        # Mock provider statistics
        stats = {
            "virustotal": ProviderStats(total_reports=1245, detection_rate=0.85),
            "abuseipdb": ProviderStats(total_reports=892, detection_rate=0.72),
            "otx": ProviderStats(total_reports=634, detection_rate=0.81),
            "urlscan": ProviderStats(total_reports=412, detection_rate=0.68)
        }
        
        return {provider: stat.dict() for provider, stat in stats.items()}
        
    except Exception as e:
        logger.error(f"Error fetching provider stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch provider statistics: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check for threat intelligence service",
    description="Check if the threat intelligence service is operational"
)
async def health_check():
    """
    Health check endpoint for the threat intelligence service.
    
    Returns:
        Status information about the service
    """
    return {
        "status": "ok",
        "service": "threat-intelligence",
        "providers": ["virustotal", "abuseipdb", "otx", "urlscan"],
        "features": ["risk-scoring", "trends", "search", "analytics"]
    }