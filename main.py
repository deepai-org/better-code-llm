import json
from multiprocessing import Pool

from helpers import desc_to_code, code_to_desc, descriptions_are_same, code_is_parsable, \
    code_without_names, code_quality_rating, code_has_bugs, descriptions_similarity_score

functions = [
    'function to generate the x-y, points on a circle, given the number of points',
    'function to generate the x-y, points on a octagon, given the radius',
    'function to draw a line using opencv, given the start and end points',
    'function to draw a circle using opencv, given the center and radius',
    'function to start a docker container that uses a gpu, given the docker image name',
    'function to get the list of docker container ids that are running and return them as a list',
]


def get_one_sample(input_description):
    try:
        code = desc_to_code(input_description)
        print("wrote some code")

        if code_is_parsable(code):
            print("code is parsable")
            names_removed = code_without_names(code)
            print("removed names")
            # print("removed names:", names_removed)

            quality = code_quality_rating(code)
            print("got quality rating:", quality)
            has_bugs = code_has_bugs(code)
            print("has bugs:", has_bugs)

            description_of_names_removed = code_to_desc(names_removed)
            print("wrote a description")

            # check if the description of the code without names is the same as the input description
            similarity = descriptions_similarity_score(input_description, description_of_names_removed)

            print("similarity to original description:", similarity)

            sample_obj = {
                "code": code,
                "description_of_names_removed": description_of_names_removed,
                "similarity_to_original_description": similarity,
                "names_removed": names_removed,
                "quality": quality,
                "has_bugs": has_bugs
            }

            return sample_obj

        else:
            print("code is not parsable")
            return None
    except Exception as e:
        print("got uncaught exception:", e)
        return None


def main():
    # print(gpt3('Say this is a test'))

    # result = descriptions_are_same(
    #     'This function generates a given number of points (num_points) evenly spaced out on a circle, and returns them as a list of tuples.',
    #     'python function to generate the x-y, points on a circle, given the number of points')
    # print(result)

    # input_description = 'function to generate the x-y, points on a circle, given the number of points'
    input_description = functions[5]

    num_samples = 10

    pool = Pool(num_samples)
    samples = pool.map(get_one_sample, [input_description] * num_samples)

    # remove None values from samples
    samples = [sample for sample in samples if sample is not None]


    print(json.dumps(samples, indent=2))


    # samples looks like an array of these now:
    #   {
    #     "code": "def my_function(num_points):\n    circle_points = []\n    for i in range(num_points):\n        angle = 2 * i * math.pi / num_points\n        x = math.cos(angle)\n        y = math.sin(angle)\n        circle_points.append((x, y))\n    return circle_points\n\npoints = my_function(10)\nprint(points)",
    #     "description_of_names_removed": " This function takes in a number (y) and uses it to calculate 10 points on the circumference of a circle. It then stores the coordinates of each point in a list and returns the list.",
    #     "similarity_to_original_description": 100.0,
    #     "names_removed": "\n\ndef x(y):\n    z = []\n    for i in range(y):\n        angle = 2 * i * math.pi / y\n        x = math.cos(angle)\n        y = math.sin(angle)\n        z.append((x, y))\n    return z\n\npoints = x(10)\nprint(points)",
    #     "quality": 90.0,
    #     "has_bugs": 10.0
    #   },


    # Compute an overall score for each sample:
    #   - similarity to original description
    #   - quality
    #   - has bugs

    for sample in samples:
        similarity = sample["similarity_to_original_description"]
        quality = sample["quality"]
        has_bugs = sample["has_bugs"]
        total_score = min(similarity,quality) - has_bugs # subtract has_bugs because we want to penalize samples that have bugs
        sample["total_score"] = total_score

    # Sort the samples by total score
    samples.sort(key=lambda x: x["total_score"], reverse=True)

    # Print the top 3 samples
    print("Top 3 samples:")
    for i in range(3):
        print("Top Sample", i+1)
        print("Code:", samples[i]["code"])
        print("Description of names removed:", samples[i]["description_of_names_removed"])
        print("Similarity to original description:", samples[i]["similarity_to_original_description"])
        print("Quality:", samples[i]["quality"])
        print("Has bugs:", samples[i]["has_bugs"])
        print("Total score:", samples[i]["total_score"])
        print("")
        print("")
        print("")
        print("")



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
    # code = desc_to_code(input_description)
    # print("Made code:")
    # print(code)
    #
    # new_description = code_to_desc(code)
    # print("Made description:")
    # print(new_description)
    #
    # print("Are descriptions the same?")
    # same = descriptions_are_same(input_description, new_description)
    # print(same)
    #
    # # now generate code again from the new description
    # code = desc_to_code(new_description)
    # print("Made code:")
    # print(code)
    #
    # # now generate description again from the new code
    # new_new_description = code_to_desc(code)
    # print("Made description:")
    # print(new_new_description)
    #
    # print("Are descriptions the same?")
    # same = descriptions_are_same(new_description, new_new_description)
    # print(same)
    #


if __name__ == '__main__':
    main()
