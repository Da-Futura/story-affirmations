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
    A named entity within the chapter.
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
        

# == Chapter ==
class Chapter(object):
    """
    A body of annotated text which takes the form of a string representing the excerpt.     
    Variables, like *name* and *possessive pronoun* are recorded in the markup form:

    * **name** : !n
    * **personal pronoun** : !ze
    * **possessive pronoun** : !zir
    * **reflexive pronoun** : !zirself

    > \"**!n** dove into the water with **!zir** dress still on\"
    """
    def __init__(self, raw):
        super(Chapter, self).__init__()
        self.raw = raw
    
    def generate(self, player):
        """
        Given a player (**Character**), we can take zir information and substitute it into the paragraph. 
        """

        """
        We start with an list of tuples, where each tuple has the form:
        (custom-markup , player-attribute)
        """
        replacements = [
                        ('@n', player.name),
                        ('@N', player.name),
                        ('@ze', player.personal_pronoun.lower()),
                        ('@Ze', player.personal_pronoun.capitalize()),
                        ('@zir', player.posessive_pronoun.lower()),
                        ('@Zir', player.posessive_pronoun.capitalize()),
                        ('@zirself', player.reflexive_pronoun.lower()),
                        ('@Zirself', player.reflexive_pronoun.capitalize())
                        ]

        chapter = self.raw
        # Now given the current chapter, perform all the replacements. 
        # I'm sure that there's a more efficient way to do this, (maybe regex)
        # but this'll have to do for now.
        for r in replacements:
            chapter = chapter.replace(r[0], r[1])

        return chapter


# == Story ==

class Story(object):
    """
    A Story is a collection of chapters. 

    While it represents a single tale, each tale can have multiple
    branching endings based on user traits, and decisions. 
    We accomplish this branching by having Stack of _accessed chapters_ 
    ie, chapters that have been shown to the current user. 

    * **chapters** : [Chapter, Chapter, ...]
    """
    def __init__(self, chapters):
        super(Story, self).__init__()
        self.chapters = chapters

    def get_player_version(self, player):
        """
        Given a player, generate a custom version of all chapters
        with the player's information spliced in. 
        Note that it just runs on _all_ of the Story's chapters right now. 
        
        TODO: In the future we'll figure out some branching logic here.

        Return: String of text representing the full Story with Chapters
                Separated by newlines.
        """
        
        accessed_list = [chapter.generate(player) for chapter in self.chapters]
        return '<br>'.join(accessed_list)

        
    


# == Create Demo Story ==

def create_demo_story():
    """
    We use default arguments to generate a story for 
    testing. 

    Return: String of text representing the generated story
    """
    
    main_character = ADA
    
    # We're just creating a set of sample text here, but we'll read from a db later
    chapter1 = Chapter("@N drew @zir sword and declared war.")
    chapter2 = Chapter("@Ze was afraid that @ze would never get to be @zirself in the current political climate.")
    chapter3 = Chapter("@N's fear forced @ze into an uncomfortable position where @ze had no choice but bloodshed.")

    story = Story([chapter1, chapter2, chapter3])

    # Given the main character, generate a story with zir information filled in.
    adas_story = story.get_player_version(main_character)

    return adas_story

def create_character(name, posessive_pronoun, personal_pronoun, reflexive_pronoun):
    """A stubbed out function for creating a character in a db"""
    
    character = Character(name, personal_pronoun, posessive_pronoun, reflexive_pronoun)
