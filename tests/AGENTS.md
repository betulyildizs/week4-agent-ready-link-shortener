# Test Guidance

- Test the public API through its HTTP interface, using the existing FastAPI test client patterns.
- Cover successful behavior and relevant failure or edge cases for each feature.
- Keep tests independent: each test should set up or select its own data and must not rely on execution order or unrelated persistent database contents.
- Assert observable behavior, such as status codes, response data, headers, and redirects, rather than private implementation details.
