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

import html
from typing import List

def html_parse_string(string: str) -> str:
    string = html.escape(string)
    if "\n" in string:
        html_parse_string((string := string.replace("\n", "<br>")))
        
    return f"</p>{string}</p>"

def parse_multiple_choice_answers(question: str, correct_answer: str, incorrect_answers: List[str]) -> dict:
    base_dict = {
        "flashcard_image_ids": [],
        "tags": [],
        "question_html": [
            {
            "text": html_parse_string(question),
            "is_correct": True
            }
        ],
        "answer_html": [],
        "shared": 2,
        "hint_html": [],
        "solution_html": ""
        }
    
    base_dict['answer_html'].append({
        "text": html_parse_string(str(correct_answer)),
        "is_correct": True
    })
    
    for incorrect_answer in incorrect_answers:
        base_dict['answer_html'].append({
            "text": html_parse_string(str(incorrect_answer)),
            "is_correct": False
        }
        )
        
    return base_dict
        