
# == Intention ==

"""
Given a set of annotated text excerpts represented as Chapters grouped
in a tree structure of possible story branches, make a game where 
the player can co-create the story based on a series of choices 
which will walk zir down the tree of chapters.
"""


from anytree import Node, RenderTree, Resolver, Walker

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
    A Story is a collection of chapters. 

    While it represents a single tale, each tale can have multiple
    branching endings based on user traits, and decisions. We're using
    a tree structure with each choice leading you down a branch.
    
    I'm just going to just use the [anytree](https://anytree.readthedocs.io/) library
    because implementing the whole Node/Render tree class rigmarole got messy real fast. 

    * **chapter_tree** : tree_root_node
    """
    def __init__(self, chapter_tree):
        super(Story, self).__init__()
        self.chapter_tree = chapter_tree


    def walk_chapter_tree(self, target):
        """
        Given a target node, walk through the character tree and return the current tale.
        The path takes the form of the name of the active node in the tree,
        ie, where the player has reached in the tale.
        
        * **path** : [active_node_name]
        """
        # The tale embodies the entierity of the story (at this point in time)
        # It'll be returned as an array of Chapters (in the right order)
        tale = []

        # Resolvers are an [anytree](https://anytree.readthedocs.io/) class which is used for search
        # Passing it 'name' is the way we tell it which attribute
        # to search on. I imagine that we could pass it 'chapter' too
        r = Resolver('name')

        # Next we get the current node, ie, the chapter that the player
        # is currently at.
        # TODO: What if a node is missing?
        curr_chapter = r.get(self.chapter_tree, target) 

        # Now that we know where they ended up in the story, we can get
        # their history by backtracking through the tree.
        ancestors = curr_chapter.ancestors

        for chapter in ancestors:            
            tale.append(chapter) # Adding to the tale array
        
        # Importantly, the list of a node's _ancestors_ don't include 
        # the node, therefore, for the complete tale, we need to 
        # add the current chapter
        tale.append(curr_chapter)

        return tale

    


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
    chapter3 = Chapter("@Ze spent years of @zir life fighting tirelessly for equal rights and respect. ")
    chapter4 = Chapter("@Ze reconsidered and decided that @ze should just be lit instead")

    # Now we create a tree with chapter1 as the root
    # This is where the strucure of the story, and the 
    # branching is defined. 
    # TODO automate the generation of the tree given some datastructure
    root = Node('0', chapter = chapter1)
    s0 = Node('1', chapter= chapter2, parent=root)
    s1a = Node('2', chapter = chapter3, parent=s0)
    s1b = Node('3', chapter =chapter4, parent=s0)

    # Initialize a Story object with the root node
    # representing the chapter_tree
    story = Story(root)
    adas_story = story.walk_chapter_tree('1/3')
    
    full_story_text = [node.chapter.generate(main_character) for node in adas_story]
    

    return "<br>".join(full_story_text)

def create_character(name, posessive_pronoun, personal_pronoun, reflexive_pronoun):
    """A stubbed out function for creating a character in a db"""
    
    character = Character(name, personal_pronoun, posessive_pronoun, reflexive_pronoun)
