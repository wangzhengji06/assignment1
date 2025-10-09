## Bank Account Simulator

Used to simulate the behavior of a bank account


### How to install

just clone this project.


### How to run the unit test

Install the `pytest` in your python env, and run `pytest` in terminal.


### Sample Usage

`pytest`

`python main.py`


### My thought process

- I probably need state pattern for difference tui
- I should define a state, and the app use state to do action
- app should only talk to bankaccount and action, and leave the tui render to states
- how does the tui talks to app state? render_spec to make tui easier to draw different states
- how does the state transform? tui send the action to app, app tells state
- but state needs to know bank account from app to prevent from withdrawing too much, ask ChatGPT
- Okay I will use protocol although I dont know why
- Get confused even more and heavily rely on ChatGPT
