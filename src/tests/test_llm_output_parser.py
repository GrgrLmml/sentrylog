import pytest

from parser.parser import parse_llm_response, parse_custom_json


@pytest.fixture
def llm_output1():
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

@pytest.fixture
def llm_output2():
    return """
    [
  {
    "category": "Info",
    "type": "Potential Reconnaissance",
    "origin": "192.168.65.1",
    "relevant_log": "192.168.65.1 - - [16/Apr/2024:14:26:13 +0000] \"GET /_stcore/host-config HTTP/1.1\" 304 0 \"http://dashboard.localhost/Demographics\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"",
    "recommendation": "This request appears to be a harmless request for host configuration. However, monitor for repeated attempts as it could be part of a reconnaissance phase. Regularly update and patch your systems and applications to minimize potential vulnerabilities."
  },
  {
    "category": "Info",
    "type": "Potential Reconnaissance",
    "origin": "192.168.65.1",
    "relevant_log": "192.168.65.1 - - [16/Apr/2024:14:26:13 +0000] \"GET /_stcore/health HTTP/1.1\" 304 0 \"http://dashboard.localhost/Demographics\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"",
    "recommendation": "This request appears to be a harmless request for health status. However, monitor for repeated attempts as it could be part of a reconnaissance phase. Regularly update and patch your systems and applications to minimize potential vulnerabilities."
  },
  {
    "category": "Warning",
    "type": "Potential Sensitive Data Access",
    "origin": "192.168.65.1",
    "relevant_log": "192.168.65.1 - - [16/Apr/2024:14:31:02 +0000] \"GET /_stcore/stream HTTP/1.1\" 101 6687 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"",
    "recommendation": "This request attempts to access a stream. Ensure that adequate access controls are in place to restrict sensitive data exposure. Regularly review access logs and limit permissions to necessary personnel only."
  },
  {
    "category": "Critical",
    "type": "Potential Unauthorized Access",
    "origin": "192.168.65.1",
    "relevant_log": "192.168.65.1 - - [16/Apr/2024:15:11:24 +0000] \"GET /abc_st_demo/ HTTP/1.1\" 404 28868 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\" \"-\"",
    "recommendation": "This request attempts to access an unauthorized location ('/abc_st_demo/'). Ensure that adequate access controls, firewall rules, and intrusion detection/prevention systems are in place. Regularly review and update security policies and conduct security audits to identify and mitigate potential vulnerabilities."
  }
]
    """


def test_parse_llm_output(llm_output1):
    pared_output = parse_llm_response(llm_output1)
    assert len(pared_output.items) == 3
    assert pared_output.parsing_errors == 2


def test_parse_llm_output2(llm_output2):
    pared_output = parse_llm_response(llm_output2)
    assert len(pared_output.items) == 4
    assert pared_output.parsing_errors == 0
