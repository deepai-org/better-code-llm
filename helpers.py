import time

import requests
import ast

openai_key = open("openai-key.txt").read().strip()


def retry_wrapper(func, *args, **kwargs):
    # Retry a function up to 3 times if it fails
    for i in range(3):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print(f"Retrying {func.__name__}...")
            time.sleep(1)


# make it a decorator:
def retry(func):
    def wrapper(*args, **kwargs):
        return retry_wrapper(func, *args, **kwargs)

    return wrapper


# and then use it like this:
# @retry


def gpt3(prompt):
    # print(prompt)
    headers = {
        "Content-Type": "application/json",
        'Authorization': "Bearer " + openai_key
    }
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 256
    }
    result = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    result.raise_for_status()
    j =  result.json()
    return j['choices'][0]['text']


@retry
def desc_to_code(description):
    result = gpt3(f'# Given the description of a function, write the code in python.\n{description}\n\ndef my_function')

    return "def my_function" + result


@retry
def descriptions_are_same(description1, description2):
    result = gpt3(
        f'Given two descriptions of functions, write YES if the functions do the identical task, and NO if they are different. Give only a one-word answer.\nFunction 1: {description1}\nFunction 2: {description2}\nAnswer:')

    one_word_answer = result

    if "YES" in one_word_answer:
        return True
    elif "NO" in one_word_answer:
        return False
    else:
        raise Exception(f"Unexpected answer: {one_word_answer}")

    # return result


@retry
def descriptions_similarity_score(description1, description2):
    result = gpt3(
        f'Given two descriptions of functions, write the likelihood that they perform the identical task or operation. Give only the score from 0 to 100, with 0 being completely different and 100 being identical operations.\nFunction 1: {description1}\nFunction 2: {description2}\nScore:')

    one_word_answer = result
    return float(one_word_answer)



@retry
def code_to_desc(code):
    '''
    Given the code of a function, write the description in natural language.
    def generate_points_on_circle(num_points):
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = math.cos(angle)
            y = math.sin(angle)
            points.append((x, y))
        return points

    '''

    result = gpt3(
        f'# Given the code of a function, write the description in natural language.\n{code}\n\n# Explanation of the code:\n#')

    return result


@retry
def code_quality_rating(code):
    # this will call gpt3 and return 0-100
    # 0 is bad, 100 is good

    result = gpt3(
        f'Given the code of a function, give a quality, clarity, cleanliness and good-engineering score. Give only a single overall number score from 0-100 with 0 being awful and 100 being perfect.\nFunction: {code}\nScore:')

    return float(result)


@retry
def code_has_bugs(code):
    # this will call gpt3 and return True or False

    result = gpt3(
        f'Given the code of a function, think carefully about the safety and correctness of the code. Give the likelihood that there bugs. If you definitely see any bugs, write 100. If you are completely sure you do not see any bugs, say 0. Give the score between 0 and 100. Give only the score. \nFunction: {code}\nBug score:')

    return float(result)


@retry
def code_without_names(code):
    # Take code and use GPT3 to remove all variable names and other identifiers

    # replace all variable names with "X", "Y", "Z", etc.

    result = gpt3(
        f'Given the code of a function, remove all variable names and other identifiers, replacing them with x, y, z etc.. The code should still be valid. Give only the code.\nFunction: {code}\nCode without names:')
    result_text = result
    return result_text


def code_is_parsable(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
