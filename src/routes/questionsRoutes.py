from flask import request, json, jsonify
import os

from . import router, getQuiz, questionsFileLocation
from ..utils.file import readFile, writeFile

# bikin soal untuk kuis yang udah ada
@router.route('/questions', methods=['POST'])
def createQuestion():
    body = request.json

    questionData = {
        "questions": []
    }

    if os.path.exists(questionsFileLocation):
        questionData = readFile(questionsFileLocation)

    questionData["questions"].append(body)
    
    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)

# minta data sebuah soal untuk kuis tertentu
@router.route('/quizzes/<quizId>/questions/<questionNumber>') # methods=["GET", "PUT", "DELETE"] PUT = update
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json

    questionFound = False
    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            questionFound = True
            return jsonify(question)
    
    if not questionFound: # validasi kalo questionNumber ga ada
        return jsonify("Question Number " + str(questionNumber) + " tidak ditemukan")

@router.route('/quizzes/<quizId>/questions/<questionNumber>', methods=["PUT", "DELETE"])
def updateDeleteQuestion(quizId, questionNumber):
    if request.method == "DELETE":
        return deleteQuestion(quizId, questionNumber)
    elif request.method == "PUT":
        return updateQuestion(quizId, questionNumber)

def deleteQuestion(quizId, questionNumber):
    questionData = readFile(questionsFileLocation)
    
    questionToBeDeleted = getThatQuestion(int(quizId), int(questionNumber)).json # ambil dari fungsi getThatQuestion

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i] == questionToBeDeleted:
            del questionData["questions"][i]
            # message = "Berhasil menghapus question Number " + questionNumber + " dari quiz id " + quizId
            break
        # else:
        #     message = "Gagal menghapus. Tidak ada quiz-id " + quizId + " atau question Number " + questionNumber

    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)

def updateQuestion(quizId, questionNumber):
    body = request.json
    
    questionData = readFile(questionsFileLocation)

    questionToBeUpdated = getThatQuestion(int(quizId), int(questionNumber)).json # ambil dari fungsi getThatQuestion
    
    for i in range(len(questionData["questions"])):
        if questionData["questions"][i] == questionToBeUpdated:
            # questionData["questions"][i]["quiz-id"] = body["quiz-id"] # ga bisa update quiz-id-nya kayanya
            questionData["questions"][i]["question-number"] = body["question-number"]
            questionData["questions"][i]["question"] = body["question"]
            questionData["questions"][i]["answer"] = body["answer"]
            questionData["questions"][i]["options"]["A"] = body["options"]["A"]
            questionData["questions"][i]["options"]["B"] = body["options"]["B"]
            questionData["questions"][i]["options"]["C"] = body["options"]["C"]
            questionData["questions"][i]["options"]["D"] = body["options"]["D"]
            break

    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)