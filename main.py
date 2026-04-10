import json
import random
import time
import os


QUESTIONS_FILE = "questions.json"
SCORE_FILE = "score.json"
TIME_LIMIT = 10  # секунд на вопрос


class Question:
    def __init__(self, text, options, answer, category):
        self.text = text
        self.options = options
        self.answer = answer
        self.category = category

    def ask(self):
        print(f"\n📚 Category: {self.category}")
        print(f"❓ {self.text}")

        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")

        start = time.time()
        user_input = input("Your answer (number): ")

        if time.time() - start > TIME_LIMIT:
            print("⏰ Time's up!")
            return False

        try:
            return self.options[int(user_input) - 1] == self.answer
        except:
            return False


class QuizEngine:
    def __init__(self):
        self.questions = self.load_questions()
        self.score = 0

    def load_questions(self):
        if not os.path.exists(QUESTIONS_FILE):
            # дефолтные вопросы
            return [
                Question("Capital of France?", ["Paris", "London", "Berlin"], "Paris", "Geography"),
                Question("2 + 2?", ["3", "4", "5"], "4", "Math"),
                Question("Python is?", ["Snake", "Language", "Car"], "Language", "Tech"),
            ]

        with open(QUESTIONS_FILE, "r") as f:
            data = json.load(f)
            return [Question(**q) for q in data]

    def save_score(self):
        data = {"last_score": self.score}
        with open(SCORE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def show_last_score(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                print(f"📊 Last score: {data.get('last_score', 0)}")

    def run(self):
        print("=== Advanced Quiz App ===")
        self.show_last_score()

        random.shuffle(self.questions)

        for q in self.questions:
            correct = q.ask()
            if correct:
                print("✅ Correct!")
                self.score += 1
            else:
                print(f"❌ Wrong! Correct answer: {q.answer}")

        print(f"\n🏁 Final score: {self.score}/{len(self.questions)}")
        self.save_score()


if __name__ == "__main__":
    QuizEngine().run()
