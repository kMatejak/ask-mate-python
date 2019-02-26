from flask import Flask, flash, redirect, render_template, \
     request, url_for
import logic


app = Flask(__name__)
app.static_folder = 'static'


@app.route('/')
def route_latest_questions():
    # latest_questions = logic.get_latest_questions()
    latest_questions = logic.get_questions()
    return render_template('list.html',
                           questions=latest_questions)


@app.route('/list')
def index():
    questions = logic.get_questions()

    return render_template('list.html',
                           questions=questions)


@app.route('/question/<question_id>')
def question_page(question_id: str):
    question = logic.get_question_by_id(question_id)
    answers = logic.get_answer_by_question_id(question_id)

    return render_template('question.html',
                           question=question,
                           answers=answers)


@app.route('/question/<question_id>/edit', methods=['GET'])
def route_edit_question(question_id):
    question = logic.get_question_by_id(question_id)

    return render_template('edit.html',
                           form_url=url_for('route_edit_question'),
                           edit_question=question,
                           button_title='Save Changes',
                           edition=True)


@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    new_data = request.form.to_dict()
    message = new_data["message"]
    title = new_data["title"]
    logic.edit_question(question_id, message, title)

    return redirect('/question/%s' % question_id)


@app.route('/answer/<answer_id>/edit', methods=['GET'])
def route_edit_answer(answer_id):
    answer = logic.get_answer_by_id(answer_id)

    return render_template('edit_answer.html',
                           answer=answer,
                           edition=True)


@app.route('/answer/<answer_id>/edit', methods=['POST'])
def edit_answer(answer_id):
    new_data = request.form.to_dict()
    message = new_data["message"]
    question_id = logic.get_question_id_by_answer_id(answer_id)
    # image = new_data["image"]  # can be enabled when image will be implemented in form
    logic.edit_answer(answer_id, message)   # image

    return redirect('/question/%s' % question_id)


@app.route("/add-question", methods=['GET'])
def route_new_question():

    return render_template('edit.html',
                           form_url=url_for('route_new_question'),
                           button_title='Add Question',
                           )


@app.route("/add-question", methods=['POST'])
def new_question():
    form = request.form.to_dict()
    question = logic.new_question(form)
    question_id = question['id']

    return redirect("/question/%s" % question_id)


@app.route("/<question_id>/new-answer", methods=['GET'])
def route_new_answer(question_id: str):
    question = logic.get_question_by_id(question_id)
    return render_template('new_answer.html',
                           question=question)


@app.route("/<question_id>/new-answer", methods=['POST'])
def new_answer(question_id):
    # save it to file
    form = request.form.to_dict()
    logic.new_answer(form, question_id)

    return redirect("/question/%s" % question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    logic.delete_question(question_id)

    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id: str):
    question_id = logic.get_question_id_by_answer_id(answer_id)
    logic.delete_answer(answer_id)

    return redirect('/question/%s'% question_id)


@app.route("/sorted/")
def sorted_condition():
    sort_by = request.args.get('sort_by')
    order = request.args.get('order')
    questions = logic.sort_questions(sort_by, order)

    return render_template('list.html',
                           questions=questions,
                           sort_by=sort_by,
                           order=order)


@app.route("/search/", methods=['POST'])
def search():
    phrase = request.form['phrase']
    question_list = logic.search(phrase)
    return render_template('list.html', questions = question_list)



if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
