"""
test_api.py  -  Tests for the Text Summarization API
Uses the `requests` library to call each endpoint.
Run the server first:  uvicorn main:app --reload
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

DIVIDER = "=" * 60


def print_response(label: str, response: requests.Response):
    print(f"\n{DIVIDER}")
    print(f"  {label}")
    print(DIVIDER)
    print(f"  Status : {response.status_code}")
    try:
        body = response.json()
        print(f"  Body   : {json.dumps(body, indent=4, ensure_ascii=False)}")
    except Exception:
        print(f"  Body   : {response.text}")
    print()


# ── Test 1: Root endpoint ─────────────────────────────────────────────────────
def test_root():
    resp = requests.get(f"{BASE_URL}/")
    print_response("GET /  →  API Introduction", resp)
    assert resp.status_code == 200
    assert "api" in resp.json()


# ── Test 2: Health check ──────────────────────────────────────────────────────
def test_health():
    resp = requests.get(f"{BASE_URL}/health")
    print_response("GET /health  →  Health Check", resp)
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ── Test 3: Summarize – valid input (news article) ────────────────────────────
def test_predict_valid_1():
    payload = {
        "text": (
            "Artificial intelligence has rapidly transformed numerous industries over the past decade. "
            "From healthcare to finance, AI-powered tools are streamlining processes, reducing costs, "
            "and enabling capabilities that were previously impossible. Machine learning models can now "
            "diagnose diseases from medical images with accuracy rivaling human specialists. "
            "In the financial sector, algorithmic trading systems process millions of transactions per "
            "second, while fraud detection models protect consumers in real time. "
            "Natural language processing has made virtual assistants and chatbots ubiquitous, "
            "handling customer service queries around the clock without human intervention. "
            "As these technologies continue to advance, ethical considerations around bias, privacy, "
            "and job displacement have become increasingly important topics for policymakers, "
            "researchers, and the general public alike."
        ),
        "max_length": 80,
        "min_length": 20,
    }
    resp = requests.post(f"{BASE_URL}/predict", json=payload)
    print_response("POST /predict  →  Valid input #1 (AI article)", resp)
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data
    assert len(data["summary"]) > 0


# ── Test 4: Summarize – valid input (science article) ────────────────────────
def test_predict_valid_2():
    payload = {
        "text": (
            "Scientists have discovered a new exoplanet located approximately 40 light-years from Earth "
            "that may have conditions suitable for liquid water on its surface. "
            "The planet, designated K2-18b, orbits within the habitable zone of its host star, "
            "a red dwarf known as K2-18. Using data from the James Webb Space Telescope, "
            "researchers detected the chemical signatures of carbon dioxide and methane in the planet's "
            "atmosphere — molecules that on Earth are associated with biological activity. "
            "While scientists caution that these findings are not conclusive evidence of life, "
            "they represent one of the most promising leads in the ongoing search for habitable worlds "
            "beyond our solar system. Further observations are planned over the coming years to "
            "better characterize the planet's atmospheric composition and surface conditions."
        ),
        "max_length": 100,
        "min_length": 30,
    }
    resp = requests.post(f"{BASE_URL}/predict", json=payload)
    print_response("POST /predict  →  Valid input #2 (science article)", resp)
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data


# ── Test 5: Missing / empty text ──────────────────────────────────────────────
def test_predict_empty_text():
    payload = {"text": "   "}
    resp = requests.post(f"{BASE_URL}/predict", json=payload)
    print_response("POST /predict  →  Empty text (expected 422)", resp)
    assert resp.status_code == 422


# ── Test 6: Text too short ────────────────────────────────────────────────────
def test_predict_short_text():
    payload = {"text": "Hello world."}
    resp = requests.post(f"{BASE_URL}/predict", json=payload)
    print_response("POST /predict  →  Too-short text (expected 422)", resp)
    assert resp.status_code == 422


# ── Test 7: min_length >= max_length ─────────────────────────────────────────
def test_predict_invalid_lengths():
    payload = {
        "text": "This is a long enough text " * 10,
        "max_length": 30,
        "min_length": 50,
    }
    resp = requests.post(f"{BASE_URL}/predict", json=payload)
    print_response("POST /predict  →  min_length >= max_length (expected 422)", resp)
    assert resp.status_code == 422


# ── Run all tests ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        test_root,
        test_health,
        test_predict_valid_1,
        test_predict_valid_2,
        test_predict_empty_text,
        test_predict_short_text,
        test_predict_invalid_lengths,
    ]

    passed = 0
    failed = 0

    print(f"\n{'#' * 60}")
    print("  Text Summarization API  –  Test Suite")
    print(f"{'#' * 60}")

    for test_fn in tests:
        try:
            test_fn()
            print(f"  ✅  {test_fn.__name__} PASSED")
            passed += 1
        except AssertionError as e:
            print(f"  ❌  {test_fn.__name__} FAILED  →  {e}")
            failed += 1
        except Exception as e:
            print(f"  ⚠️  {test_fn.__name__} ERROR   →  {e}")
            failed += 1

    print(f"\n{DIVIDER}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(DIVIDER)

