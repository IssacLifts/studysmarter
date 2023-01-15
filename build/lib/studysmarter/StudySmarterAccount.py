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

from .login import _login
from .Response import StudySmarterResponse
from .StudySmarterStudySets import StudySets
import requests

class Account:
    def __init__(self, email: str, password: str) -> None:
        self.token, self.id, self.language, self.session = _login(email, password)
        self.session: requests.Session
        self.headers = {"authorization": f"Token {self.token}"}
        
    def change_password(self, new_password: str) -> StudySmarterResponse:
        resp = self.session.patch(f"https://prod.studysmarter.de/users/{self.id}/",
                           json={
                               f"user": {'password': f'"{new_password}"'}
                                 },
                           headers=self.headers)
        
        return StudySmarterResponse(
            status_code=resp.status_code,
            json=resp.json(),
            site_token=self.token
        )
    
    def fetch_studysets(self) -> StudySets:
        resp = self.session.get(f"https://prod.studysmarter.de/users/{self.id}/course-subjects/full/",
                                headers=self.headers)
        return StudySets(resp.json(),
                         self.session,
                         self.token,
                         self.id)
    
    def create_studyset(self,
                         name: str,
                         color_id: int=62,
                         *,
                         exam_date=None,
                         shared=True,
                         unified_subject=None
                         ) -> StudySmarterResponse:
        
        resp = self.session.post(f"https://prod.studysmarter.de/users/{self.id}/course-subjects/",
                          json={
                              "colorId": color_id,
                              "countries": [],
                              "level": 0,
                              "name": name,
                              "shared": shared,
                              "unified_subject": 206
                              
                          },
                          headers={
                              "authorization": f"Token {self.token}"
                          })
        
        return StudySmarterResponse(
           status_code=resp.status_code,
           json=resp.json(),
           site_token=self.token 
        )
        
    def change_name(self, name: str) -> StudySmarterResponse:
        resp = self.session.post(
            f"https://prod.studysmarter.de/users/{self.id}/",
            json={
                "user": {"first_name": str(name)}
            }
        )
        
        return StudySmarterResponse(
            status_code=resp.status_code,
            json=resp.json(),
            site_token=self.token
        )