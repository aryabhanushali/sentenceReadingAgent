# SentenceReadingAgent

A simple rule-based program that answers questions about basic English sentences.

## What It Does

Given a sentence and a question, the agent finds the answer using pattern matching (no machine learning or external libraries).

It supports common question types:

- **Who** → person  
- **What** → object/action  
- **Where** → place  
- **When / What time** → time  
- **How** → method  
- **How far / long / big** → quantity or description  
- **Why** → reason (from “because”, “since”, “so”)  
- **Which** → specific item

## Example

```python
from SentenceReadingAgent import SentenceReadingAgent

agent = SentenceReadingAgent()

sentence = "Ada brought a short note to Irene."

print(agent.solve(sentence, "Who brought the note?"))  
# Ada

print(agent.solve(sentence, "What did Ada bring?"))  
# note

print(agent.solve(sentence, "Who did Ada bring the note to?"))  
# Irene

print(agent.solve(sentence, "How long was the note?"))  
# short
