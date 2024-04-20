import pytest

from config.config import logger
from parser.models import ResponseItems
from parser.parser import parse_llm_response, parse_custom_json


@pytest.fixture
def llm_output():
    return """
    Here is some text followed by a JSON object:
     {"category": "Warning", "type": "Attempted Directory Traversal", "origin": "192.168.65.1", "relevant_log": "192.168.65.1 - - [16/Apr/2024:15:11:46 +0000] \"GET /page-data/abc_st_demo/page-data.json HTTP/1.1\" 404 28868 \"http://localhost/abc_st_demo/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"", "recommendation": "Implement strict input validation and access control to prevent unauthorized access to sensitive directories or files. Consider using a web application firewall (WAF) to detect and block such attempts."}
     then we have another JSON object:
     ```JSON
     {"category": "Info", "type": "Standard Application Requests", "origin": "192.168.65.1", "relevant_log": "The majority of the log entries appear to be standard requests for resources related to the application, such as HTML pages, JavaScript files, images, and other assets. These do not appear to be indicative of a targeted attack.", "recommendation": "Continue monitoring the logs for any unusual patterns, but these requests seem to be normal application usage."}
     ```
     maybe here comes a broken json object:
     {"category": "Error", "type": "Broken JSON Object", "origin": "
     after that yet another correct one
     {"category": "Warning", "type": "Attempted Directory Traversal", "origin": "192.168.65.1", "relevant_log": "192.168.65.1 - - [16/Apr/2024:15:11:46 +0000] \"GET /page-data/abc_st_demo/page-data.json HTTP/1.1\" 404 28868 \"http://localhost/abc_st_demo/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"", "recommendation": "Implement strict input validation and access control to prevent unauthorized access to sensitive directories or files. Consider using a web application firewall (WAF) to detect and block such attempts."}
     and finally a proper JSON but with a missing/corrupt field:
     {"categories": "Warning, Info", "type": "Attempted Directory Traversal", "origin": "192.168.65.1", "relevant_log": "192.168.65.1 - - [16/Apr/2024:15:11:46 +0000] \"GET /page-data/abc_st_demo/page-data.json HTTP/1.1\" 404 28868 \"http://localhost/abc_st_demo/\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"", "recommendation": "Implement strict input validation and access control to prevent unauthorized access to sensitive directories or files. Consider using a web application firewall (WAF) to detect and block such attempts."}
    """


def test_parse_llm_output(llm_output):
    pared_output = parse_llm_response(llm_output)
    assert len(pared_output.items) == 3
    assert pared_output.parsing_errors == 2
