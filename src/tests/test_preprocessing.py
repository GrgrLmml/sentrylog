import pytest

from utils.prepocessing import log_chunk_preprocessor


@pytest.fixture
def log_lines():
    return """2024-04-20 19:40:41 192.168.65.1 - - [20/Apr/2024:17:40:41 +0000] "GET /manifest.webmanifest HTTP/1.1" 304 0 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:41 192.168.65.1 - - [20/Apr/2024:17:40:41 +0000] "GET /component---src-pages-404-js-efafc08a85c1fccd8cab.js HTTP/1.1" 200 431 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /abc_st_demo/ HTTP/1.1" 404 28868 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /app-3ba290a65dbe80bad269.js HTTP/1.1" 200 37795 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /framework-710896d0ddd6f5699906.js HTTP/1.1" 200 46991 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /webpack-runtime-ef9d21452179cb118815.js HTTP/1.1" 200 2073 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /static/dm-sans-latin-700-normal-6261bc7f59cc2e5f8f293a89e362662f.woff2 HTTP/1.1" 200 18212 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /favicon-32x32.png?v=b25f1b5166faa49ff95f2c682b50d34e HTTP/1.1" 200 1716 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /page-data/app-data.json HTTP/1.1" 200 50 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /page-data/abc_st_demo/page-data.json HTTP/1.1" 404 28868 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "GET /page-data/404.html/page-data.json HTTP/1.1" 200 123 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"
2024-04-20 19:40:42 192.168.65.1 - - [20/Apr/2024:17:40:42 +0000] "HEAD /abc_st_demo HTTP/1.1" 404 0 "http://localhost/abc_st_demo/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" "-"    """.split("\n")


def test_preprocess_log_lines(log_lines):
    chunks = log_chunk_preprocessor(log_lines)
    assert chunks.start_time == '2024-04-20T17:40:41+00:00'
    assert chunks.end_time == '2024-04-20T17:40:42+00:00'
    assert len(chunks.lines) == 12
