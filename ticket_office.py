import sys

import pandas as pd
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.styles import Style
from pyfiglet import Figlet

from models import *

logo = Figlet(font="5lineoblique", width=250)

print(HTML(f'<style color="#e11d48">{logo.renderText("TrainTickets")}</style>'))
print(HTML(f'<style color="#e11d48">github.com/PersifoX/TrainTickets</style>\n'))
print(HTML(f'<bold>1.</bold> <style color="#60a5fa">Выберите </style>'))
print(HTML(f'<bold>2.</bold> <style color="#60a5fa">Выберите маршрут</style>'))
print(HTML(f'<bold>3.</bold> <style color="#60a5fa">Купите место</style>\n'))

style = Style(
    [
        ("pl", "#454545 italic"),
        ("error", "#e11d48 bold"),
        ("warning", "#f59e0b bold"),
        ("success", "#00b76e bold"),
        ("primary", "#e11d48"),
    ]
)

session = PromptSession(
    style=style,
    erase_when_done=True,
    complete_in_thread=True,
)

ticket_office = TicketOffice()

try:
    while True:
        # setup

        seat_number = session.prompt("Номер места: ")

        print()


except KeyboardInterrupt:
    sys.stdout.flush()
    print("Goodbye!")
