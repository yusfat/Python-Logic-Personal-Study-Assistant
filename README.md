# Chat Knowledge Trainer 💬🧠

Python  
License  
Status

Chat Knowledge Trainer 💬

A lightweight open-source active-recall tool that helps you master every concept from a conversation and the logic of the code itself. Practice terms, meanings, categories, wrong answers, spaced repetition, and even deep code understanding - all in a simple terminal interface.

🎯 The Problem

After a long conversation or coding session, important ideas and implementation details fade quickly.  
Traditional note-taking or generic flashcard apps feel heavy and disconnected from the actual material.  
This project gives you a focused, beginner-friendly trainer that turns the entire knowledge base + the code into interactive practice.

✨ Features

Mixed quizzes (term → meaning)
Reverse practice (meaning → term)
Spaced repetition system
Wrong-answer tracking & review
Browse concepts by category
Full concept list review
Code Logic Deep Dive (targeted questions about key lines and decisions)
Strict Top-to-Bottom Code Walkthrough
Clean separation of data and code (knowledge.csv + the Python script)
Easy content management — just edit the CSV to add or update concepts
Recent-question avoidance and flexible answer matching

🚀 Why This Project?

Real learning happens through active recall and spaced practice, not passive rereading.  
By combining conversational knowledge with explicit code-structure training, you build both conceptual understanding and the ability to explain (and modify) the program itself.

💻 Quick Start

Option 1: CLI Version (Terminal / Termux)

How to Run

git clone 
cd 
python quiz.py   # or the actual filename of the script

Make sure knowledge.csv is present in the same folder. The program will create progress.json and recent.json automatically.
