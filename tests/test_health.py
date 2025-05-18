#!/usr/bin/env python 
# filepath: c:\Squad2-FastAPI\tests\test_health.py 
import sys 
import os 
 
# Add the parent directory to sys.path to allow importing app 
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__)))) 
 
from fastapi.testclient import TestClient 
from backend.app.main import app 
 
client = TestClient(app) 
 
def test_health_check(): 
    resp = client.get("/") 
    assert resp.status_code == 200 
    assert resp.json() == {"status": "ok"} 
