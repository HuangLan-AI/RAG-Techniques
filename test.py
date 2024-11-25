header = {
    'host': 'localhost:8080',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'referer': 'http://localhost:3000/',
    'content-type': 'application/json',
    'content-length': '26',
    'origin': 'http://localhost:3000',
    'connection': 'keep-alive',
    'cookie': 'your-cookie-data-here',
    'X-Auth-Request-Email': 'user@example.com',  # Example of a custom header
    'X-Auth-Request-Name': 'User Name'            # Example of a custom header
}

x = 'X-Auth-Request-Email'
print(x in header)


# Headers({'host': 'localhost:8080', 
#          'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0', 
#          'accept': '*/*', 
#          'accept-language': 'en-US,en;q=0.5', 
#          'accept-encoding': 'gzip, deflate, br, zstd', 
#          'referer': 'http://localhost:3000/', 
#          'content-type': 'application/json', 
#          'content-length': '26', 
#          'origin': 'http://localhost:3000', 
#          'connection': 'keep-alive', 
#          'cookie': 'ajs_anonymous_id=3c462d25-36e2-479a-880d-0905188543e0; supabase-auth-token=%5B%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjU0MzIxL2F1dGgvdjEiLCJzdWIiOiJlNjg1ZDQ2YS1jZDQ2LTRhZmMtYjRhOS02ZWU3MTUzNGVhYjgiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzI2NjQ5NjIzLCJpYXQiOjE3MjY2NDYwMjMsImVtYWlsIjoiZmFyYXouc3ViaGFuaUBrdW9rZ3JvdXAuY29tLnNnIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3MjY1NDIyNTF9XSwic2Vzc2lvbl9pZCI6IjA3NDAyYjQwLThhOTgtNDdlNS05MWNmLTZjYjNiYTUzYjVhNSIsImlzX2Fub255bW91cyI6ZmFsc2V9.5HpNnlJokFIUXxRmJd2-9UsLRCQMs4qwiHhTNNRPD3E%22%2C%22djYWksMbCVXs1jO6LL6Hlg%22%2Cnull%2Cnull%2Cnull%5D; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU1ZmUxY2NhLTBmMDMtNGVmZi05NDE0LTg4ZTUyYTJmMDdlNyJ9.XlChya2yBuD_o9rr0nkMEUh7MtlXoPcfU28Ccc2Qifo; oui-session=eyJfc3RhdGVfbWljcm9zb2Z0X01HWFhkOFA0dWxDUlA1SkJJR1BTeVZOSmR5Q3d2ViI6IHsiZGF0YSI6IHsicmVkaXJlY3RfdXJpIjogImh0dHBzOi8va2FpdmEtZ3B0ZGV2Lm5ncm9rLmRldi9vYXV0aC9taWNyb3NvZnQvY2FsbGJhY2siLCAibm9uY2UiOiAiYnhSajBneE9BSVJzYVI1WXhWNVgiLCAidXJsIjogImh0dHBzOi8vbG9naW4ubWljcm9zb2Z0b25saW5lLmNvbS9jMWE1ZjNkMC0wZjJiLTQ5YTgtYjdmOC1iYWY0OTQxNTVlZTcvb2F1dGgyL3YyLjAvYXV0aG9yaXplP3Jlc3BvbnNlX3R5cGU9Y29kZSZjbGllbnRfaWQ9YmNmMmNiMmUtY2Q0ZS00NjAwLTk2MjMtNDc5Y2E5OWZiY2MwJnJlZGlyZWN0X3VyaT1odHRwcyUzQSUyRiUyRmthaXZhLWdwdGRldi5uZ3Jvay5kZXYlMkZvYXV0aCUyRm1pY3Jvc29mdCUyRmNhbGxiYWNrJnNjb3BlPW9wZW5pZCtlbWFpbCtwcm9maWxlJnN0YXRlPU1HWFhkOFA0dWxDUlA1SkJJR1BTeVZOSmR5Q3d2ViZub25jZT1ieFJqMGd4T0FJUnNhUjVZeFY1WCJ9LCAiZXhwIjogMTcyOTQ5NTM4Mi4yMjEyOTk0fX0=.ZxX3fQ.cOZBIOx9JyRx_9mjV_AMtwp_N2M', 
#          'sec-fetch-dest': 'empty', 
#          'sec-fetch-mode': 'cors', 
#          'sec-fetch-site': 'same-site', 
#          'priority': 'u=4'})


import secrets
print(secrets.token_urlsafe(32))
