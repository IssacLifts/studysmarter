"""MIT License

Copyright (c) 2023 Issac

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

from requests import Session
from .errors import InvalidEmailOrPassword

def _login(email: str, password: str, *, session: Session = None) -> tuple:
    session = session if session is not None else Session()
    resp = session.post("https://prod.studysmarter.de/api-token-auth/",
                        json={
                            "password": password,
                            "platform": 'web',
                            "username": email
                        })
    resp_json: dict = resp.json()
    status: int = resp.status_code
    if resp_json.get('error_code') == "001":
        raise InvalidEmailOrPassword(
            "Invalid Email or password"
        )
        
    elif status == 429:
        return 'ratelimited'
    
    return resp_json['token'], resp_json['id'], resp_json['language'], session
    