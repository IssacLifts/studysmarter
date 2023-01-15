# studysmarter
API Wrapper for studysmarter.

Developed by Issac (c) 2022

Example use case:
```python
import studysmarter

# login
studysmarter_account = studysmarter.login("testemail123@gmail.com", "password123")

# change studysmarter account name
studysmarter_account.change_name("IssacLifts")

# create new studyset
stsudysmarter_account.create_studyset("Quantum Physics")

# fetch all studysets (dictionary format)
studysets = studysmarter_account.fetch_studysets()

# prints all your studysets in dictionary format
print(studysets.study_sets)

# fetch the first studyset
studyset = studysets.fetch_studyset(0)

# fetches all flashcards
flash_cards = studyset.fetch_flashcards()

# adds a flashcard to set
studyset.add_flashcard("What's the equation to find speed", "Disance / time")
```
