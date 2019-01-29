import csv
import os
import time

question_labels = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_labels = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# parameters to call the import data: filename = "data/answers.csv" or filename = "data/questions.csv"

def import_data(filename):
    exists = os.path.isfile(filename)
    if not exists:
        return None
    else:
        with open(filename, 'r') as f:
            read_dictionary = csv.DictReader(f)
            result = []
            for row in read_dictionary:
                result.append(dict(row))
            return result



def export_data(filename, labels, some_data_do_add):
    exists = os.path.isfile(filename)
    #next_id = id_generator()
    #story.update({'id': next_id})    # we can insert multiple items with update, add date generator
    with open(filename, "a+") as f:
        writer = csv.DictWriter(f, fieldnames=labels, delimiter=',')
        if not exists:
            writer.writeheader()
        writer.writerow(some_data_to_add)


#  print(import_data("sample_data/question.csv"))