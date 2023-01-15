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
from ordered_set import OrderedSet
from typing import Dict, Set, Tuple, List
from .utils import html_parse_string, parse_multiple_choice_answers
from .Response import StudySmarterResponse
from lxml.html import fromstring

class StudySet:
    def __init__(self,
                 name: str,
                 id: int,
                 session: Session,
                 token: str,
                 user_id: int) -> None:
        self.name = name
        self.set_id = id
        self.__session: Session = session
        self.__token = token
        self.user_id = user_id
        self.__headers = {"authorization": f"Token {self.__token}"}

    def add_flashcard(self, question: str, answer: str) -> StudySmarterResponse:
        resp = self.__session.post(
            f"https://prod.studysmarter.de/users/{self.user_id}/course-subjects/{self.set_id}/flashcards/",
            json={
                "flashcard_image_ids": [],
                "tags": [],
                "question_html": [
                    {
                    "text": html_parse_string(str(question)),
                    "is_correct": True
                    }
                ],
                "answer_html": [
                    {
                    "text": html_parse_string(str(answer)),
                    "is_correct": True
                    }
                ],
                "shared": 2,
                "hint_html": [],
                "solution_html": ""
                },
            headers=self.__headers
        )
        
        return StudySmarterResponse(
            status_code=resp.status_code,
            json=resp.json(),
            site_token=self.__token
        )
        
    def create_subset(self, name: str) -> StudySmarterResponse:
        resp= self.__session.post(
            f"https://prod.studysmarter.de/users/{self.user_id}/course-subjects/",
            json={
                "name": str(name),
                "parent_subject_id": self.set_id
            },
            
            headers=self.__headers
        )
        
        return StudySmarterResponse(
            status_code=resp.status_code,
            json=resp.json(),
            site_token=self.__token
        )
        
    def add_multiple_choice_flashcard(self, question: str,
                                      correct_answer: str,
                                      incorrect_answers: List[str]
                                      ) -> StudySmarterResponse:
        
        answers_json = parse_multiple_choice_answers(question,
                                                     correct_answer,
                                                     incorrect_answers)
        
        resp = self.__session.post(
            f"https://prod.studysmarter.de/users/{self.user_id}/course-subjects/{self.set_id}/flashcards/",
            json=answers_json,
            headers=self.__headers
        )
        
        return StudySmarterResponse(
            status_code=resp.status_code,
            json=resp.json(),
            site_token=self.__token
            
        )
        
    def fetch_flashcards(self) -> List[str]:   
        resp = self.__session.get(f"https://prod.studysmarter.de/users/{self.user_id}/course-subjects/{self.set_id}/flashcards/?search=&s_bad=true&s_medium=true&s_good=true&s_trash=false&s_unseen=true&tag_ids=&quantity=9999999&created_by=&order=anti-chronological&cursor=",
                        headers=self.__headers)
        
        question_answers = []
        
        for question in resp.json()['results']:
            question_ = question['question_html']
            html_question = question_[0]['text']
            
            answer = question['answer_html']
            
            if len(answer) > 1:
                for idx, answer_ in enumerate(answer):
                    if answer[idx]['is_correct'] is True:
                        html_answer = answer_['text']
                        break
                            
                    else:
                        continue
            else:
                html_answer = answer[0]['text']
                              
            html_question = html_question.replace("<br>", "\n")
            html_answer = html_answer.replace("<br>", "\n")
            
            html_question = html_question.replace("\xa0", '')
            html_answer = html_answer.replace("\xa0", '')

            root_question = fromstring(html_question)
            root_answer = fromstring(html_answer)
            
            plain_question_text = root_question.text_content()
            plain_answer_text = root_answer.text_content()
            
            question_answers.append({
                "back": plain_answer_text,
                "front": plain_question_text
            })
            
        return question_answers
      
class StudySets:
    
    def __init__(self,
                 flash_cards: dict,
                 session: Session,
                 token: str,
                 user_id: int) -> None:
        self._session = session
        self.__token = token
        self.user_id = user_id
        self.__results_dict = None
        self.__studyset_objects, self.__raw_flashcards = self.__parse_studysets(flash_cards)
        
        
    def __parse_studysets(self, flashcards) -> Tuple[Set, Dict]:
        self.__results_dict = {flashcard['breadcrumbs'][0]['name']: flashcard['breadcrumbs'][0]['id'] for flashcard in flashcards['results']}
        cards = OrderedSet()
        for _flashcard in list(zip(self.__results_dict.keys(), self.__results_dict.values())):
            cards.add(StudySet(*_flashcard, self._session, self.__token, self.user_id))
        return (cards, self.__results_dict)
    
    @property
    def study_sets(self) -> dict:
        return self.__raw_flashcards
    
    
    def fetch_studyset(self, index: int) -> StudySet:
        return self.__studyset_objects[index]
        