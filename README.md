# Shakespearean Word Visualizer

<img width="1680" alt="image" src="https://github.com/KhairKhair/Shakespearean-Word-Visualizer/assets/135009781/0aa4a729-65a9-4c04-82be-6504f77a1076">





## Description
This project is a tool designed to visualize the distribution of words in Shakespeare's plays across different genres: Comedy, Tragedy, and History. It leverages Natural Language Processing (NLP) techniques to learn separate word embeddings for each genre using the Skip-gram model. The project utilizes Python libraries such as Pandas, PyTorch, Plotly, and Dash to process the text data and create interactive visualizations.

## Features
- **NLP and Word Embeddings:** Uses the Skip-gram model to learn word embeddings separately for Comedy, Tragedy, and History genres.
- **Data Cleaning and Preprocessing:** Removes punctuation and converts words to lowercase for uniform analysis.
- **Genre-specific Analysis:** Separates plays into Comedy, Tragedy, and History for targeted analysis.
- **Interactive Visualizations:** Utilizes Plotly and Dash to create interactive scatter plots showing word distributions and embeddings.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/shakespearean-word-visualizer.git
   cd shakespearean-word-visualizer

2. pip install -r requirements.txt

## Usage - trainer (processes csv file and learns embedding using pytorch then visualizes data using dash)
### note - requires shakespeare_plays.csv to be in same directory as trainer.ipynb
1. run trainer.ipynb

## Usage - visualizer (uses pre-learned embedding to visualize word-space using plotly and dash)
### note - requires comedy_embeddings.pt, tragedy_embeddings.pt, history_embeddings.pt, common_words.npy, all_words.npy to be in same directory as visualizer.py
1. run visualizer.py


