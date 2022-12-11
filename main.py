# curl https://api.openai.com/v1/completions \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer YOUR_API_KEY" \
# -d '{"model": "text-davinci-003", "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'
import ast

import requests

openai_key = open("openai-key.txt").read().strip()

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
    return result.json()


def descriptions_are_same(description1, description2):
    prompt = '''

    Given two descriptions of functions, write YES if the functions do the identical task, and NO if they are different. Give only a one-word answer.

    Function 1: This function generates a given number of points (num_points) evenly spaced out on a circle, and returns them as a list of tuples.
    Function 2: python function to generate the x-y, points on a square, given the number of points

    Answer: NO
    '''

    result = gpt3(
        f'Given two descriptions of functions, write YES if the functions do the identical task, and NO if they are different. Give only a one-word answer.\nFunction 1: {description1}\nFunction 2: {description2}\nAnswer:')

    one_word_answer = result['choices'][0]['text']

    if "YES" in one_word_answer:
        return True
    elif "NO" in one_word_answer:
        return False
    else:
        raise Exception(f"Unexpected answer: {one_word_answer}")

    # return result['choices'][0]['text']

def make_code_for_description(description):
    '''
# Given the description of a function, write the code in python.
# python function to generate the x-y, points on a circle, given the number of points

def
    '''

    result = gpt3(f'# Given the description of a function, write the code in python.\n{description}\n\ndef my_function')

    result_text = result['choices'][0]['text']
    return "def my_function"+result_text


def make_description_for_code(code):
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

    result = gpt3(f'# Given the code of a function, write the description in natural language.\n{code}\n\n# Explanation of the code:\n#')

    result_text = result['choices'][0]['text']
    return result_text

def get_code_quality_rating(code):
    # this will call gpt3 and return 0-100
    # 0 is bad, 100 is good

    result = gpt3(f'Given the code of a function, give a quality, clarity, cleanliness and good-engineering score. Give only a single overall number score from 0-100 with 0 being awful and 100 being perfect.\nFunction: {code}\nScore:')

    one_word_answer = result['choices'][0]['text']
    return float(one_word_answer)

def code_has_bugs(code):
    # this will call gpt3 and return True or False

    result = gpt3(f'Given the code of a function, think carefully about the safety and correctness of the code. If you see any bugs, say YES. If you do not see any bugs, say NO. Give only a one word answer.\nFunction: {code}\nCode has bugs:')

    one_word_answer = result['choices'][0]['text']
    if "YES" in one_word_answer:
        return True
    elif "NO" in one_word_answer:
        return False
    else:
        raise Exception(f"Unexpected answer: {one_word_answer}")

def code_without_names(code):
    # Take code and use GPT3 to remove all variable names and other identifiers

    # replace all variable names with "X"

    result = gpt3(f'Given the code of a function, remove all variable names and other identifiers, replacing them with x. The code should still be valid. Give only the code.\nFunction: {code}\nCode without names:')
    result_text = result['choices'][0]['text']
    return result_text


def code_is_parsable(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def main():
    # print(gpt3('Say this is a test'))

    # result = descriptions_are_same(
    #     'This function generates a given number of points (num_points) evenly spaced out on a circle, and returns them as a list of tuples.',
    #     'python function to generate the x-y, points on a circle, given the number of points')
    # print(result)

    #input_description = 'function to generate the x-y, points on a circle, given the number of points'
    input_description = "function to generate the x-y, points on a octagon, given the radius"

    num_samples = 10
    samples = []
    sample_descriptions=[]
    for i in range(num_samples):
        code = make_code_for_description(input_description)
        print("wrote some code")

        if code_is_parsable(code):
            print("code is parsable")
            names_removed = code_without_names(code)
            print("removed names:", names_removed)
            continue

            samples.append(code)
            quality = get_code_quality_rating(code)
            print("got quality rating:", quality)
            has_bugs = code_has_bugs(code)
            print("has bugs:", has_bugs)

            # description = make_description_for_code(code)
            # print("wrote a description")
            # sample_descriptions.append(description)

        else:
            print("code is not parsable")
    #
    # valid_samples = []
    # for i, description in enumerate(sample_descriptions):
    #     matches_original = descriptions_are_same(description, input_description)
    #     print(f"Sample {i} matches original: {matches_original}")
    #     if matches_original:
    #         valid_samples.append(samples[i])
    #
    # print(valid_samples)
    #
    #
    #
    #
    # code = make_code_for_description(input_description)
    # print("Made code:")
    # print(code)
    #
    # new_description = make_description_for_code(code)
    # print("Made description:")
    # print(new_description)
    #
    # print("Are descriptions the same?")
    # same = descriptions_are_same(input_description, new_description)
    # print(same)
    #
    # # now generate code again from the new description
    # code = make_code_for_description(new_description)
    # print("Made code:")
    # print(code)
    #
    # # now generate description again from the new code
    # new_new_description = make_description_for_code(code)
    # print("Made description:")
    # print(new_new_description)
    #
    # print("Are descriptions the same?")
    # same = descriptions_are_same(new_description, new_new_description)
    # print(same)
    #


if __name__ == '__main__':
    main()
