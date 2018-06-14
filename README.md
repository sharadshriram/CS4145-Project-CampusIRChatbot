# MyCI - My Campus Information Chatbot

This is a Telegram-bot which is designed and developed as part of the CS4145: Crowd Computing course at the Delft University of Technology by team *CrowdIT* - [Neha Sree Thuraka](https://github.com/nehasreet), [Sharad Shriram](https://github.com/sharadshriram), [Salim Salmi](https://github.com/SalimSalmi), [Yizi Chen](https://github.com/chenyizi086). The use case for which the chatbot is developed is course recommendation using the concept of crowd computing. This is prototype is based on the following flowchart,

<img src = "images/myci-implementation.png">

## Using the chatbot
The chatbot is accessible at [](). However, ping us on the course slack channel for you to interact with the chatbot. Once you are inside the chatbot, you can use the following commands to interact with it

    - `/start` starts the interaction with the chatbot
    - `/display` displays the course preferences of the user
    - `/recommend` gives recommendations of courses based on user preferences
    - `/addpreference` updates the course preferences for the user.
    - `/points` displays the points accumulated 
    - `/remove` remove the preference of the user
    - `/menu` lists all the chatbot commands
    
## Project Structure
The project directories and files are structured in the following tree:

    - `images` images for the repo
    - `python-bot` 
        - `answer.py` processing and aggregating answers recieved from tasks
        - `bot.py`    handles bot instances for handling messages and updates
        - `courselist.csv` compiled list of course title and course codes
        - `main.py` starts the bot, maps the commands to respective functions
        - `mongodb.py` to handle MongoDB to create and modify data relating to the task and user model
        - `neha.py` intial implementation of task allocation done by [@neha](https://github.com/nehasreet)
        - `question.py` module to get questions/ queries from user
        - `recommendations.py` provides course recommendations based on `csv` file
        - `requirements.txt` third-party modules that are required
        - `settings.py` set the access code and timeout period of request for the bot
        - `taskallocation.py` create and allocate tasks to similar users 
        - `usermodel.py` managing the user model based on the chat messages
    - `README.md`

## Setting Up
Before getting started you'll need the following software installed on your operating system:
- Python 3 
- MongoDB (If you're using Windows, [this link](https://www.youtube.com/watch?v=ll2tY6KH8Tk) is useful)

The following python-packages are the next that needs to be installed. Don't forget to be using Powershell/ Terminal with Administrator or super-user privileges. To make your lives easy you can paste the following command to install the packages using pip. Do not have pip? [Check this out](https://pip.pypa.io/en/stable/installing/):

`pip install -r requirements.txt `

### Local Testing
If all the installation went well, you can launch Powershell/ Terminal and run the following command to start the bot service:

`python main.py`

And in Telegram search for `MyCI_bot` and you're good to go!
Have fun! 

In the event of any trouble create an issue on this repo. We'll address it as soon as possible.
