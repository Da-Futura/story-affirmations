# == Initializing Base Classes ==

# === Character ===
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
    """
    def __init__(self, name, personal_pronoun, posessive_pronoun):
        super(Character, self).__init__()
        self.name = name
        self.personal_pronoun = personal_pronoun
        self.posessive_pronoun = posessive_pronoun

# A demo protoganist modelled after yours truly:
ADA = Character('Ada', 'she', 'her') 
        

# === Story ===
class Story(object):
    """
    All the parts needed to tell a tale
    """
    def __init__(self, text):
        super(Story, self).__init__()
        self.text = text
    
    def create_story(self, player):
        my_player = player
        story: str= self.text
        story = story.replace('Karo', my_player.name)

        return story


def create_demo_story():
    main_character = ADA
    story = Story("Karo drew her sword and declared war.")
    return story.create_story(main_character)
