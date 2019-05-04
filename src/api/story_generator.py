# == Intention ==

"""
Create an interactive fiction game where the player's name/pronouns
are spliced into the story. 
"""

import api.db as dbService
import api.utils as utils
# I'm just going use the [networkx](networkx.github.io) library to represent
# the graph structure of the game.
import networkx as nx

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

    * **name** : @n
    * **personal pronoun** : @ze
    * **possessive pronoun** : @zir
    * **reflexive pronoun** : @zirself

    > \"**@n** dove into the water with **@zir** dress still on\"
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
        
        Q: do I need to specify that those strings are unicode with the u'string' syntax?
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
    A graph of all the possible variations of a tale. <br>
    Each chapter is a node in the graph, and the edges between them
    are _directed_ edges indicating which chapter leads to the other, <br>

    eg. <br>
    A --> B --> C <br>
    | <br>
    v <br>
    D --> E

    ChapterA can lead to both ChapterB, **and** ChapterD, which in turn can lead to ChapterE

    Args:
    1. **chapter_graph** : a networkx Graph object representing the chapters, and the paths between them
    2. **title** : a string representing the title of the Story
    """
    def __init__(self, chapter_graph, title):
        super(Story, self).__init__()
        self.chapter_graph = chapter_graph
        self.title = title
    
    def generate_all_chapters(self, player):
        """
        Given a Character representing the player, return an array
        of every Chapter in the story with zir information spliced in. 
        [It's mostly meant for debugging]
        """
        
        """
        We're going to use python's excellent List Comprehension here.
        For all of the nodes in the chapter_graph, grab the **second** element
        in the Node's tuple. ie (ID, DATA)[1]
        Then we do DATA['chapter'] to get the Chapter object itself, and finally,
        Character.generate(player) to create the chapter text with the player's info
        spliced in.
        """
        generated_chapters = [n[1]['chapter'].generate(player) 
                                for n in self.chapter_graph.nodes(data=True)]

        print(generated_chapters)
        
        return generated_chapters



# == Story Queeries ==

# === get_story_chapters ===
def get_story_chapters(story_id):
    """
    Given a story id in the form of a string (eg. 'H8wkMown193'),
    go find that story in the database, and then return its list of chapters

    Args: <br>
    1. **story_id** : A string representing the story id to be queeried

    Return: [(KeyA, {'chapter' : ChapterA}), (KeyB, {'chapter': ChapterB}) ...]
    """

    # Here we queery the database using the dbService from db.py
    # We drill down from <br> **Stories --> Our Specific Story --> It's chapters** <br>
    # Then we return an iterable list of chapters by using _.each()_
    db_chapters = dbService.db.child("stories").child(story_id).child("chapters").get().each()

    # db_chapters now = **[PyreObject, PyreObject, ...]**, <br>
    # but networkx needs the form: **[(KEY, DATA), (KEY, DATA), ...]**. <br>
    # Where the KEY is the Chapter's unique ID from firebase, and the DATA, 
    # is a dict with a Chapter object, ie <br>
    # **{'chapter', Chapter('@Zir adventures in wonderland)}** <br>
    # so we use Python's excellent List Comprehension to do it.
    formatted_chapters = [ (c.key(), {'chapter' :Chapter(c.val()['raw'])})
                        for c in db_chapters ]
    
    # TODO At this point we should handle the case where the db returns None because no story/story-chapters exist
    return formatted_chapters


# == Create Demo Story ==

def create_demo_story():
    """
    We use default arguments to generate a story for 
    testing. 'chapter

    Return: String of text representing the generated story
    """

    specific_stories = dbService.db.child("stories").order_by_child("title").equal_to("Great Expectations").get().val()
    
    # print(next(iter(specific_stories)))
    # print(specific_stories.popitem()[1])
    all_stories = dbService.get_all_documents('stories')
    # sample_edges = [(1, 2)]
    sample_chapters = get_story_chapters("hp101") # [(1,ChapterA), (2,ChapterB)]
    
    story_graph = nx.Graph()
    story_graph.add_nodes_from(sample_chapters)
    # TODO: db query for sample edges
    # story_graph.add_edges_from(sample_edges)    

    dragon_slayer = Story(story_graph, 'Dragon Slayer')
    dragon_chapters = dragon_slayer.generate_all_chapters(ADA)

    return "<br>".join(dragon_chapters)
