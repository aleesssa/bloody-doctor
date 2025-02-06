import os
import json
import random
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Label, Footer, Header, Static

from minigames.crossword import CrosswordPuzzle
from minigames.tictactoe import tictactoe
from minigames.wordsearch import WordSearchV2

class BloodyDoctor(App):
    TITLE = "BLOODY DOCTOR"
    SUB_TITLE = "Roleplay as a doctor and save patients!"
    CSS_PATH = "style.tcss"
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode')]
    
    def compose(self) -> ComposeResult:
        # Create child widget for the app
        yield Header()
        yield Footer()
        yield Container(
            Label("Hi, there! Mind telling us your name?"),
            Input(placeholder="Enter your name"),
            id="name"
        )
    
    def action_toggle_dark(self) -> None:
        self.theme = (
            'textual-dark' if self.theme == 'textual-light' else 'textual-light'
        )
        
if __name__ == '__main__':
    app = BloodyDoctor()
    app.run()
    
class Player:
    def __init__(self, name, level, xp, hearts):
        self.name = name
        self.level = level
        self.xp = xp
        self.hearts = hearts
        
    def printStatus(self):
        print(f'Hearts = {self.hearts}')
        print(f'Level = {self.level}')
        print(f'XP = {self.xp}')

    def xpToLevelUp(self):   
        xpToLevelUp = {
        1 : 50,
        2 : 125,
        3 : 225,
        4 : 350,
        5 : 500
         }
        return xpToLevelUp[self.level]

    # convert player data to json to save progress
    def to_dict(self):
        return player.__dict__
    
    # convert saved json file to object
    @staticmethod
    def from_dict(player):
        name = player['name']
        level = player['level']
        xp = player['xp']
        hearts = player['hearts']
        return Player(name, level, xp, hearts)
    
class Patient:
    # Instantiating object
    def __init__(self, name, age, condition, symptom, blood_type, allergy, isRevealedAge = True, isRevealedCondition = False, isRevealedSymptom = False, isRevealedBloodType = False, isRevealedAllergy = False):
        self.name = name
        self.age = age
        self.condition = condition
        self.symptom = symptom
        self.blood_type = blood_type
        self.allergy = allergy    
        
        # Keep track of infos that have been revealed to player
        self.isRevealed = {
        'age' : isRevealedAge,
        'condition' : isRevealedCondition,
        'symptom' : isRevealedSymptom,
        'blood_type' : isRevealedBloodType,
        'allergy' : isRevealedAllergy
        }

    # return state of info(revealed or not) to be saved
    def to_dict(self):
        return self.__dict__
        
    # convert saved json file to object
    @staticmethod
    def from_dict(patient):
        name = patient['name']
        age = patient['age']
        condition = patient['condition']
        symptom = patient['symptom']
        blood_type = patient['blood_type']
        allergy = patient['allergy']
        isRevealed = patient['isRevealed']
        
        patient = Patient(name, age, condition, symptom, blood_type, allergy, isRevealed['age'], isRevealed['condition'], isRevealed['symptom'], isRevealed['blood_type'], isRevealed['allergy'])
        
        return patient
        
    # Print patient's profile
    def printProfile(self):
        print(self.name)
        print(f'Age : {self.age if self.isRevealed['age'] else '?????????'}')
        print(f'Condition : {self.condition if self.isRevealed['condition'] else '?????????'}')
        print(f'Symptom : {self.symptom if self.isRevealed['symptom'] else '?????????'}')
        print(f'Blood type : {self.blood_type if self.isRevealed['blood_type'] else '?????????'}')
        print(f'Allergy : {self.allergy if self.isRevealed['allergy'] else '?????????'}')

class Quiz:
    def __init__(self, questionSet, xp):
        self.questionSet = questionSet
        self.xp = xp

    # Print question and answer choices
    def printQuiz(self, n):
        answerChoices = self.questionSet[n]['answerChoices']
        
        # Print question
        print(self.questionSet[n]['question'])
        
        
        # Print answer choices
        for i, answer in enumerate(answerChoices):
            intToLetter = lambda x: chr(ord("A") + x) # Convert int to letter for MCQ
            print(f'{intToLetter(i)}. {answer}')
        
    # def randomizeChoices(self, n):
    #     # randomize choices position 
    #     randomizedChoices = random.choices(self.questionSet[n]['answerChoices'])
        
    #     pass
        
    def getHint(self, n):
        return self.questionSet[n]['hint']
        
    def checkAnswer(self, n, answer):
        if answer.lower() == self.questionSet[n]['answer'].lower():
            return True
        else:
            return False
    
    def revealInfo(self, patient, index):
        patient.isRevealed[self.questionSet[index]['revealedInfo']] = True        

    # choose question randomly
    def randomize(self):
        return random.randint(0, len(self.questionSet) - 1)

    # Return Quiz dict to be saved in a json file
    def to_dict(self):
        return self.__dict__

    # From dict to instance
    @staticmethod
    def from_dict(quiz):
        questionSet = quiz['questionSet']
        xp = quiz['xp']
        
        return Quiz(questionSet, xp)

class Game:
    games = ['Word search', 'Crossword', 'TicTacToe']
    
    # Display game options
    @classmethod
    def printGameOptions(cls):
        for i, game in enumerate(cls.games):
            print(f'{i+1}. {game}')

    # Execute game based on user's input
    @classmethod
    def executeGame(cls, index):
        if 0 <= index <= len(cls.games):
            print(f'Playing {cls.games[index-1]}')
        else:
            print('Invalid choice.')
            
            
        if index == 1:
            WordSearchV2.execute()
        if index == 2:
            CrosswordPuzzle.execute()
        if index == 3:
            tictactoe.play_game()
            
    @staticmethod
    def saveGame(player, patients, quizzes):
        # Save player and patient data to their respective json files
        with open('player.json', 'w') as playerFile:
            json.dump(player.to_dict(), playerFile, indent = 4)
            
        # Save patient info to patients.json
        patients = [patient.to_dict() for patient in patients]        
        with open('patients.json', 'w') as patientFile:
            json.dump(patients, patientFile, indent = 4)
            
        # Save quizzes to quizzes.json
        quizzes = [quiz.to_dict() for quiz in quizzes] 
        with open('quizzes.json', 'w') as quizFile:
            json.dump(quizzes, quizFile, indent = 4)    
        
                
        

    # Load json files as python dictionaries and create player instance
    @staticmethod
    def loadPlayer():
        with open('player.json', 'r') as playerFile:
            playerData = json.load(playerFile) 
            player = Player.from_dict(playerData) # Player instance created from loaded dictionary
        return player    

    @staticmethod
    def loadPatient(n):
        with open('patients.json', 'r') as patientFile:
            patientData = json.load(patientFile)
            patient = Patient.from_dict(patientData[n])
            
        return patient
    
    @staticmethod
    def loadQuiz(n):
        with open('quizzes.json', 'r') as quizFile:
            quizData = json.load(quizFile)
            quiz = Quiz.from_dict(quizData[n])
            
        return quiz
    
                



# Function for each level
def startLevel(patient, quiz):

    patient.printProfile() # Print patient's profile

    # Loop through quiz set 1
    while len(quiz.questionSet) > 0: #makes sure player answers all the question correctly before proceeding to next patient
        index = 0
        
        # Display question to player
        quiz.printQuiz(index)
        
        hint = input("Would you like to play minigame and get a hint?[yes/no] : ")
        
        if hint.lower() == "y" or hint.lower() == "yes":
            Game.printGameOptions()
            index = int(input(f'Choose the minigame you would like to play![1 - {len(Game.games)}] :'))
            Game.executeGame(index)
            quiz.printQuiz(index)
            
        answer = input("Answer : ")
        if quiz.checkAnswer(index, answer):
            print("Correct!")
            quiz.revealInfo(patient, index) # Reveal patient's info according to the question answered
            quiz.questionSet.pop(index) # Remove question from the list
            player.xp += quiz.xp
        else:
            print("Incorrect.. don't you know your own patient?")
            player.hearts -= 1
            print(f'You currently have {player.hearts} hearts')

        
        if player.xp >= player.xpToLevelUp():
            player.level += 1
            print("You've leveled up!")
    
        saveGame = input('would you like to save the game?')
        if saveGame == 'yes':
            Game.saveGame(player, patients, quizzes)
        
        if player.hearts <= 0:
            lose()
            
        patient.printProfile()
        
# Execute when player loses (10 Hearts gone)
def lose():
    print("Your patient is dead. You should've paid more attention.")
    exit()

# Function to print intro
def printIntro(name):
    print(f'''
Hurry, Dr. {name}! 
The hospital is bustling with patients. 
You currently have 5 patients under your care.
Treat your patients by answering questions related to them.
You can play minigames to acquire hint that will help you answer the question.
Answering correctly will gain you XP that will help you level up!
However, if you answer the question wrong, 1 heart will be deducted from your 10 hearts.
Reaching zero hearts will kill your patient.
Here comes your first patient~
''')

# Function to print course and students info
def printInfo():
    print("""
# ***********************************************************************************************************************************************************************
# Program: bloodydoctor.py
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC4L
# Trimester: 2430
# Names: ALEESSA BATRISYIA BINTI AZWAN | NUR ALYA IMAN BINTI MOHD PAZLI YUSOF | NUR DAMIA' BATRISYIA BINTI MOHAMMAD DENEE ROSDI | QAISARAH BINTI SHAMSUL AZRAN
# IDs: 
# Emails: 
# ************************************************************************************************************************************************************************  
    """)
    


# Quiz section
questionSet1 = [
    {
        'question' : "How old is your patient?",
        'answerChoices' : [12, 30, 50, 100],
        'answer' : 'A',
        'revealedInfo' : 'age',
        'hint' : 'Kids this age usually start going through puberty.'
    },
    {
        'question' : "What condition does your patient have?",
        'answerChoices' : ['Diabetes', 'Heart attack', 'Anaemic', 'Heat stroke'],
        'answer' : 'C',
        'revealedInfo' : 'condition',
        'hint' : 'She lacks red'
    },
    {
        'question' : "What is your patient's blood type?",
        'answer' : 'B',
        'answerChoices' : ['B', 'A', 'AB', 'O'],
        'revealedInfo' : 'blood_type',
        'hint' : 'This blood type is rare. Only 6% of population has it.'
    },
    {
        'question' : "Does your patient have any allergy?",
        'answer' : 'A',
        'answerChoices' : ['Peanut butter', 'Seafood', 'Dust', 'None'],
        'revealedInfo' : 'allergy',
        'hint' : 'Sweet.'
    },
    {
        'question' : "What symptom does the patient primarily show?",
        'answer' : 'D',
        'answerChoices' : ['Swollen ankle', 'Irritated skin', 'High fever', 'Fatigue'],
        'revealedInfo' : 'symptom',
        'hint' : 'Tired.'
    }
]
questionSet2 = [
    {
        'question' : "What happened to Baby Boss?",
        'answer' : 'A',
        'answerChoices' : ['Fell off the bed', 'Choked on a food', 'Allergy reaction', 'Cried too much'],
        'revealedInfo' : 'condition',
        'hint' : 'Head concussion'
    },
    {
        'question' : "What symptom is the baby showing?",
        'answer' : 'B',
        'answerChoices' : ['Hyperactivity', 'Vomiting', 'Runny nose', 'High fever'],
        'revealedInfo' : 'symptom',
        'hint' : "Liquid"
    },
    {
        'question' : "From the symptom shown, what is the most immediate medical concern",
        'answer' : 'D',
        'answerChoices' : ['Fractured arm', 'Sprained ankle', 'Dehydration', 'Concussion'],
        'revealedInfo' : 'symptom',
        'hint' : ""
    },
    {
        'question' : "Who can donate blood to Baby Boss?",
        'answer' : 'B',
        'answerChoices' : ['A+ Donor', 'O- Donor', 'B- Donor', 'AB- Donor'],
        'revealedInfo' : 'blood_type',
        'hint' : 'Baby Boss has O+ type.'
    },
    {
        'question' : "Which food should you not feed to Baby Boss?",
        'answer' : 'C',
        'answerChoices' : ['A bowl of fresh fruit', 'A humidifier', 'A scented rose bouquet', 'A book and a cup of tea'],
        'revealedInfo' : 'condition',
        'hint' : 'Jaehyun enjoys nature but avoids certain flowers because they make him feel unwell.'
    }
]
questionSet3 = [
    {
        'question' : "Is Jaehyun eligible for blood donation?",
        'answer' : 'C',
        'answerChoices' : ['Yes, his condition does not affect his eligibility.', 'Yes, as long as he drinks enough water.' ,'No, he has low hemoglobin levels.', 'No, but taking iron supplements right before donation makes him eligible.'],
        'revealedInfo' : 'condition',
        'hint' : 'Jaehyun suffers from iron deficiency.'
    },
    {
        'question' : "Who can donate blood to Jaehyun?",
        'answer' : 'D',
        'answerChoices' : ['B+ donor', 'O+ donor', 'A- Donor', 'O- donor'],
        'revealedInfo' : 'blood_type',
        'hint' : "Jaehyun's blood type is B-"
    },
    {
        'question' : "What symptom does Jaehyun show?",
        'answer' : 'A',
        'answerChoices' : ['Pale skin.', 'High fever', 'Joint pain', 'Rash'],
        'revealedInfo' : 'symptom',
        'hint' : "This condition affects the body's ability to carry oxygen efficiently"
    },
    {
        'question' : "What is the best diet for Jaehyun",
        'answer' : 'B',
        'answerChoices' : ['Dairy products and white rice', 'Lean red meat and vitamin C-rich fruits', 'Fast food and sugary drinks', 'Seafood, whole grains and coffee'],
        'revealedInfo' : 'condition',
        'hint' : 'Jaehyun often feels tired and dizzy.'
    },
    {
        'question' : "As Jaehyun's doctor, what should you avoid placing in his hospital room?",
        'answer' : 'C',
        'answerChoices' : ['A bowl of fresh fruit', 'A humidifier', 'A scented rose bouquet', 'A book and a cup of tea'],
        'revealedInfo' : 'allergy',
        'hint' : 'Jaehyun enjoys nature but avoids certain flowers because they make him feel unwell.'
    }
]
questionSet4 = [
    {
        'question' : "How do you treat Sunghoon's condition?",
        'answer' : 'C',
        'answerChoices' : ['Administration of intravenous fluids and pain management', 'Antibiotic therapy', 'Surgical removal of the appendix', 'Adoption of a high-fiber diet and bed rest'],
        'revealedInfo' : 'condition',
        'hint' : "Sunghoon is facing acute appendicitis"
    },
    {
        'question' : "What causes Sunghoon's symptom?",
        'answer' : '',
        'answerChoices' : ['Physical blockage of the intestines', 'Inflammatory cytokine release', 'Excessive gastric acid secretion', 'Severe blood loss from the inflamed appendix'],
        'revealedInfo' : 'symptom',
        'hint' : "Sunghoon shows lack of appetite as the symptom"
    },
    {
        'question' : "Which is true about Sunghoon's blood type?",
        'answer' : '',
        'answerChoices' : ['They can donate red blood cells to patients of any blood type', 'They are universal recipients for red blood cell transfusions', 'Their plasma can be transfused to patients of all blood types', 'They can only receive red blood cells from O- donors.'],
        'revealedInfo' : 'blood_type',
        'hint' : 'Sunghoon has AB- blood type.'
    },
    {
        'question' : "What is the most appropriate diet for Sunghoon after appendix surgery?",
        'answer' : '',
        'answerChoices' : ['Plenty of fruits and vegetables', 'Clear liquids only, gradually advancing to soft foods', 'High-protein, low-carbohydrate diet', 'High-sugar diet for energy'],
        'revealedInfo' : 'condition',
        'hint' : 'After appendix surgery, patient needs foods that are balanced and easy to digest'
    },
    {
        'question' : "What is Sunghoon allergic to?",
        'answer' : '',
        'answerChoices' : ['Eggs', 'Peanut butter', 'Grapes', 'Nothing'],
        'revealedInfo' : 'allergy',
        'hint' : 'Sunghoon is not allergic to anything'
    }
]
questionSet5 = [
    {
        'question' : "Is Nisreen's conditionc contagious?",
        'answer' : 'C',
        'answerChoices' : ['Yes, it can spread through direct skin contact', 'No, it is not contagious', 'Yes, it is caused by bacteria and can be transmitted through the air', 'All of the above'],
        'revealedInfo' : 'condition',
        'hint' : "Nisreen has eczema"
    },
    {
        'question' : "What type of eczema does Nisreen have?",
        'answer' : 'A',
        'answerChoices' : ['Dyhrotic eczema', 'Atopic dermatitis', 'Contact dermatitis', 'Nummular Eczema'],
        'revealedInfo' : 'symptom',
        'hint' : "Nisreen has small, fluid-filled blisters on her hands"
    },
    {
        'question' : "In a scenario where Nisreen needs blood donation, which one of your previous patients is eligible and compatible to donate blood to Nisreen?",
        'answer' : 'E',
        'answerChoices' : ['Moana binti Drake', 'Baby Boss', 'Jaehyun bin Jamal', 'Sunghoon', 'None of the above'],
        'revealedInfo' : 'blood_type',
        'hint' : 'Nisreen has O- blood type.'
    },
    {
        'question' : "What is the best treatment for Nisreen?",
        'answer' : 'B',
        'answerChoices' : ['Scrubbing the blisters to remove dead skin and applying alcohol-based sanitizer', 'Applying a thick moisturizer, using mild steroid cream, and avoiding triggers', 'Popping the blisters to let the fluid drain and dry out the skin', 'Taking antibiotics immediately, even if there is no sign of infection'],
        'revealedInfo' : 'condition',
        'hint' : 'Treatments should focus on soothing the skin, reducing inflammation, and preventing infections'
    },
    {
        'question' : "Nisreen had an eczema flare up recently. What is the possible trigger for her flare up?",
        'answer' : 'C',
        'answerChoices' : ['Smoke', 'Pollen', 'Dust', 'Stress'],
        'revealedInfo' : 'allergy',
        'hint' : 'Nisreen was cleaning her fan the day before the flare up happened'
    }
]
    


# Print students info
printInfo()


# GAME STARTS


# Check for saved file
if os.path.exists('player.json'):
    loadFile = input('Would you like to load your saved game? [Yes/No] : ')
    if loadFile.lower() == 'yes' or loadFile.lower() == 'y':
        # Create instances using saved data
        player = Game.loadPlayer()
        quizzes = []
        patients = []
        
        # Load patients and quizzes info and append instances to patients and quizzes list
        for i in range (player.level - 1, 5):
            patients.append(Game.loadPatient(i))
            quizzes.append(Game.loadQuiz(i))
 
        
        print(f'Welcome back, Dr. {player.name}! Ready to get back to work? Of course you are ! Let us continue!!!')
        
        # Start level starting from current patient
        for i in range(len(patients)):
            startLevel(patients[i], quizzes[i])
    else:       
        # Create Patient instances using new data   
        patient1 = Patient('Moana binti Drake', 12, 'Anemia', 'Slight dizziness', 'A', 'peanut butter', isRevealedAge=False)
        patient2 = Patient('Baby Boss', 1, 'Head concussion', 'Vomiting', 'O+', 'Eggs')
        patient3 = Patient('Jaehyun bin Jamal', 27, 'Iron deficiency', 'Pale skin', 'B-', 'Roses')
        patient4 = Patient('Sunghoon', 45, 'Acute appendictitis', 'Lack of appetite', 'AB-', 'None')
        patient5 = Patient('Nisreen Athirah', 22, 'Eczema', 'Painful blisters on hands', 'O-', 'Dust')
        
        patients = [patient1, patient2, patient3, patient4, patient5]
        
        # Create Quiz instances using new data
        quiz1 = Quiz(questionSet1, xp=10)
        quiz2 = Quiz(questionSet2, xp=15)
        quiz3 = Quiz(questionSet3, xp=20)
        quiz4 = Quiz(questionSet4, xp=25)
        quiz5 = Quiz(questionSet5, xp=30)

        quizzes = [quiz1, quiz2,quiz3, quiz4, quiz5]
        
        # Get player's name and create player instance
        name = input("Hi there! Mind telling us your name? : ").capitalize()
        player = Player(name, xp=0, level=1, hearts=10)
        printIntro(player.name) # INTRO
else:
    # Create Patient instances using new data   
    patient1 = Patient('Moana binti Drake', 12, 'Anemia', 'Slight dizziness', 'A', 'peanut butter', isRevealedAge=False)
    patient2 = Patient('Baby Boss', 1, 'Head concussion', 'Vomiting', 'O+', 'Eggs')
    patient3 = Patient('Jaehyun bin Jamal', 27, 'Iron deficiency', 'Pale skin', 'B-', 'Roses')
    patient4 = Patient('Sunghoon', 45, 'Acute appendictitis', 'Lack of appetite', 'AB-', 'None')
    patient5 = Patient('Nisreen Athirah', 22, 'Eczema', 'Painful blisters on hands', 'O-', 'Dust')
    
    patients = [patient1, patient2, patient3, patient4, patient5]
    
    # Create Quiz instances using new data
    quiz1 = Quiz(questionSet1, xp=10)
    quiz2 = Quiz(questionSet2, xp=15)
    quiz3 = Quiz(questionSet3, xp=20)
    quiz4 = Quiz(questionSet4, xp=25)
    quiz5 = Quiz(questionSet5, xp=30)

    quizzes = [quiz1, quiz2,quiz3, quiz4, quiz5]
    
    # Get player's name and create player instance
    name = input("Hi there! Mind telling us your name? : ").capitalize()
    player = Player(name, xp=0, level=1, hearts=10)
    printIntro(player.name) # INTRO


for i in range(len(patients)):
    startLevel(patients[i], quizzes[i])
            

