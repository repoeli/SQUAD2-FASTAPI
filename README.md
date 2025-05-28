http://localhost:8181/
http://localhost:8181/threat-intel/health
http://localhost:8181/threat-intel/trends
http://localhost:8181/threat-intel/risk-score/ip/192.168.1.1

curl -X POST http://localhost:8181/threat-intel/search -H "Content-Type: application/json" -d "{\"query_type\":\"ip\",\"query_value\":\"malicious\",\"limit\":3}" 2>nul

http://localhost:8181/threat-intel/risk-score/ip/192.168.1.1

backend/
├── app/
│ ├── threat_intel/
│ │ ├── models.py
│ │ ├── mock_data.py
│ │ └── router.py
│ ├── main.py
│ ├── models.py
│ ├── crud_router.py
│ └── vt_router.py
├── requirements.txt
└── Dockerfile
infra/
└── docker-compose.yml
tests/
├── conftest.py
├── test_health.py
├── test_items.py
└── test_virustotal.py
docs/
└── ... (documentation files)
