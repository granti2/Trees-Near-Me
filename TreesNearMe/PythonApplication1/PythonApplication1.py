
from flask import Flask, render_template
app = Flask(__name__)

import json
from collections import defaultdict

# Load the tree data from file
with open('C:\\Users\\Grant Ingram\\Documents\\Trees\\champion-trees-near-me.json', 'r') as f:
    TREE_DATA = json.load(f)

# Do some pre-filtering of the data before
# the server starts
# Here we are keeping a count of trees found in unique counties and unique species
COUNTIES = defaultdict(int)
SPECIES = defaultdict(int)

for tree in TREE_DATA:
  # Split the common and scientifc names
  tree['Common'] = tree['Species'].split(',')[0]
  tree['Scientific'] = tree['Species'].split(',')[1]
  # Increment the counters
  COUNTIES[tree['Location']] = COUNTIES[tree['Location']] + 1
  SPECIES[tree['Common']] = SPECIES[tree['Common']] + 1

@app.route('/')
def main():
  # Function to render templates/index.html with county/species data
  return render_template('index.html', counties=COUNTIES, species=SPECIES)

@app.route('/all')
def all():
  # Function to render all of the trees
  return render_template('trees.html', data=TREE_DATA)

@app.route('/by_county/<county>')
def by_county(county):
  # Function to render a subset of trees based on county
  filtered = []
  for tree in TREE_DATA:
    if tree['Location'] == county:
      filtered.append(tree)
  return render_template('trees.html', data=filtered)

@app.route('/by_species/<species>')
def by_species(species):
  # Function to render a subset of trees based on species
  filtered = []
  for tree in TREE_DATA:
    if tree['Common'] == species:
      filtered.append(tree)
  return render_template('trees.html', data=filtered)

@app.route('/treefacts')
def Tree_facts():
    return render_template('Tree_facts.html')


app.run(host='localhost', port=5000, debug=True)