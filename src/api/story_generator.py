print("Hello World")

class Player(object):
    """The current player"""
    def __init__(self, name, personal, posessive):
        super(Player, self).__init__()
        self.name = name
        self.personal_pronoun = personal        
        self.posessive_pronoun = posessive
        

class Story(object):
    """Initial Story Object"""
    def __init__(self, player):
        super(Story, self).__init__()
        self.player = player
    
    def create_story(self):
        player = self.player
        return player.posessive_pronoun
                

def create_story(name):
    """Creates a story given the user's name"""
    player = Player('Karo', 'she', 'her')
    my_story = Story(player)
    return my_story.create_story()
