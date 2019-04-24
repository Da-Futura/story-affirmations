# Story Affirmations
Sometimes you need a little reminder that, "You're that bitch." 
Given your name and pronouns, this project will give you a whole
assortment of dramatic paragraphs with *you* as the protagonist.

eg. If you're Maria, and you use she/her pronouns, we might take the classic
excerpt from Harry Potter and the Half Blood Prince where Harry and Ginny 
first kiss, and generate the passage: 

> 'We won! Four hundred and fifty to a hundred and forty! We won!' _Maria_ looked around; there was Ginny running towards _her_; she had a hard, blazing look in her face as she threw her arms around _her_.

Honestly, I thought that this was just gonna be a find/replace when I started, but now I'm really falling down a rabbit hole here. 
Pronouns are complicated, and parsing seems fun. 

## Setup
After cloning the repo, run the bootstrap script to install basic python and
js dependencies.
```bash
./bin/bootstrap.sh
```

## Up and running
To run both the API and UI in hot-reload mode:
```bash
# must be run from the project root...
./bin/run_dev.sh
```

This will start parcel in `watch` mode and flask server in `development` mode.

To generate docs, point pycco at the api folder, and then append the typography, and custom slidesheet.
I use the hand alias:
`alias p="pycco src/api/*.py ; echo '<link href=\"https://fonts.googleapis.com/css?family=Raleway:100,400|PT+Mono|Bitter|Codystar|Ubuntu+Mono:400,700|VT323\" rel=\"stylesheet\"> <link rel=\"stylesheet\" href=\"story_docs.css\">' | tee -a docs/story_generator.html docs/hello.html docs/text_parser.html"`
