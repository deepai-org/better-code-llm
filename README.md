# better-code-llm
Extracting better code from large language models

# Introduction

This is an experiment on techniques to extract better code from large language models. 
We ask the model to evaluate its own generated code.

# Running:

Add your openai key to a file `openai_key.txt` in the root directory.

`python3 main.py`


# Key Findings:

- Davinci 003 seems to be even better for code than Codex? 
- The latest GPT3 is usable without ChatGPT, and better in some ways
- GPT3 can judge the quality of its own code it wrote
- If you ask GPT3 to explain the code it wrote, often it reveals the code isn't what you asked for.
- Sometimes the model will generate a invalid response, but rarely!
- We can write wacky new types of functions, eg:
  - make_code_for_description(description)
  - make_description_for_code(code)
  - get_code_quality_rating(code)
  - code_has_bugs(code)

