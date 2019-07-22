# Story Affirmations
The beginning of an attempt to model a Choose Your Own Adventure Game

## Semi-Literate docs
https://da-futura.github.io/story-affirmations/story_generator.html

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
