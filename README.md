# Mason Rummy

A command-line Mason version of Rummy written in Python 3.2.0

Created with love for George Mason University

Mason Rummy is rummy with a five-suit deck -- the fifth suit's symbol is the green Patriot. Object-oriented.

Options:
  + 2 or 3 player games
  + With or without stacked deck
  + New or returning player
  + Scores for previous players will be stored in scores.csv
  + Deck is imported from any .deck file with proper formatting

# How to Play

There are three rounds of Mason Rummy, and at the end the lowest score wins.

The goal is to lay down as many cards as possible each turn. The current player will draw a card, and then lay down a meld, run, or add to an existing meld or run. To finish a turn, the current player discards one card. A round is over when one player runs out of cards.

# Formatting

Formatting is non-negotiable

## scores.csv

Scores are saved in scores.csv
scores.csv has four columns: name, games won, games lost, and best score
Example included

## .deck
The deck is read from a .deck file
The .deck file must have 65 card descriptions, separated by any whitespace
Card descriptions are suit + value: CDHSP/123456789TJQKA
Example included

# License

Mason Rummy is licensed under the [MIT license.](https://github.com/bridgetlane/mason-rummy/blob/master/LICENSE)
