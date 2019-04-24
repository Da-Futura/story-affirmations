# == Intention ==

"""
We're going to parse a paragraph of annotated text 
(usually a book excerpt), and then, given information 
on the player, generate a new version of the text with 
the player's infromation spliced in.
"""



# == Character ==
class Character(object):
    """
    A named entity within the story.
    Right now we're only considering name and pronouns,
    but in the future we'll store other biographical data.

    Args:

    1. **name** (string): 
        The proper noun name of the character 

    2. **personal_pronoun** (string): 
        The preferred personal pronoun (she/he/ze/etc)

    3. **possesive_pronoun** (string): 
        The preferred posessive pronoun (her/his/zir/etc)

    4. **reflexive_pronoun** (string):
        The preferred reflexive pronoun (herself/homself/zirself/etc)
    """
    def __init__(self, name, personal_pronoun, posessive_pronoun, reflexive_pronoun):
        super(Character, self).__init__()
        self.name = name
        self.personal_pronoun = personal_pronoun
        self.posessive_pronoun = posessive_pronoun
        self.reflexive_pronoun = reflexive_pronoun
    

# A demo protoganist modelled after yours truly:
ADA = Character('Ada', 'she', 'her', 'herself')
        

# == Story ==
class Story(object):
    """
    A body of annotated text which takes the form of a string
    representing the excerpt. Variables, like *name* and *possessive pronoun* 
    are recorded in the shorthand form:

    * **name** : !n
    * **personal pronoun** : !ze
    * **possessive pronoun** : !zir
    * **reflexive pronoun** : !zirself

    ['**!n**' , 'dived', 'into', 'the', 'water', 'with' , '**!zir**', 'dress', 'still', 'on!' ]

    """
    def __init__(self, raw):
        super(Story, self).__init__()
        self.raw = raw
    
    def generate(self, player):
        """
        Given a player (**Character**), we can take zir information and substitute it into the paragraph. 
        """
        
        curr_player = player
        
        story = self.raw.replace('@n', player.name)
        story = story.replace('@ze', player.personal_pronoun)
        story = story.replace('@zir', player.posessive_pronoun)
        story = story.replace('@zirself', player.reflexive_pronoun)

        return story

# == Create Demo Story ==

def create_demo_story():
    """
    We use default arguments to generate a story for 
    testing. 

    Return: String of text representing the generated story
    """
    
    main_character = ADA
    main_text = "@n drew @zir sword and declared war"
    story = Story(main_text)
    return story.generate(main_character)

def create_character(name, posessive_pronoun, personal_pronoun, reflexive_pronoun):
    character = Character(name, personal_pronoun, posessive_pronoun, reflexive_pronoun)
