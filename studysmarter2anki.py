import studysmarter
from threading import Thread
from typing import List
from sys import exit
import pyfiglet
from pystyle import Write, Colors

try:
    import requests, studysmarter
except ImportError as e:
    print(f"Please run install_dependencies.bat: {e}")
    exit(0)
    
def create_anki_deck(deck_name: str) -> int:
    response = requests.post(
        ANKI_CONNECT_LINK,
        json={"action": "createDeck", "version": 6, "params": {"deck": deck_name}}
    )
    
    return response.status_code

def add_flashcard_to_deck(cards: List[str]) -> int:
    response = requests.post(ANKI_CONNECT_LINK,
                            json={"action": "addNotes",
                                "version": 6,
                                "params": {"notes": cards}})

    return response.status_code

def main(index: int) -> None:
    
    study_set = study_sets.fetch_studyset(index)
    
    create_anki_deck((deck_name := study_set.name))
    
    flash_cards = study_set.fetch_flashcards()
    
    
    cards = []
    for flash_card in flash_cards:
        
        cards.append(
            {
            "deckName": deck_name,
            "modelName": "Basic",
            "fields":{
                "Front": flash_card['front'],
                "Back": flash_card['back']
            },
            "options": {
                "allowDuplicates": False
            }
    }
        )
        
        
    Thread(target=add_flashcard_to_deck, args=(cards,)).start()
    
if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("study2anki")
    
    Write.Print(ascii_banner, Colors.blue_to_purple, interval=0)
    
    user = input("\nWhat is your studysmarter email/username: ")
    password = input("What is your studysmarter password: ")
    study_acc = studysmarter.login(user, password)
    
    ANKI_CONNECT_LINK = "http://localhost:8765"
    
    study_sets = study_acc.fetch_studysets()
    
    anki_threads = []
    
    for index, study_set in enumerate(list(study_sets.study_sets), start=0):
        anki_threads.append(Thread(target=main, args=(index,)))
    
    for thread in anki_threads:
        thread.start()
        
    for thread in anki_threads:
        thread.join()
