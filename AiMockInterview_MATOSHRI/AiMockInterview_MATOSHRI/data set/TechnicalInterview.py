import csv
import difflib
import random
import speech_recognition as sr

def load_csv(file_path):
    """
    Load the CSV file containing questions, answers, and categories.
    """
    data = []
    try:
        with open(file_path, mode='r', encoding='latin1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append({'question': row['Question'], 'answer': row['Answer'], 'category': row['Category']})
    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}")
    return data

def filter_questions_by_category(data, category):
    """
    Filter questions by the selected category.
    """
    return [item for item in data if item['category'].lower() == category.lower()]

def convert_speech_to_text():
    """
    Use SpeechRecognition library to convert speech to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your answer...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition service: {e}")
            return ""

def calculate_match_percentage(actual_answer, user_answer):
    """
    Calculate the matching percentage between actual answer and user answer.
    """
    matcher = difflib.SequenceMatcher(None, actual_answer.lower(), user_answer.lower())
    return matcher.ratio() * 100

def main():
    # File path for the CSV
    csv_file_path = "Questions_Answers.csv"  # Replace with the path to your CSV file

    # Load questions and answers from CSV
    print("Loading questions and answers from the CSV file...")
    data = load_csv(csv_file_path)

    # Get available categories
    categories = set(item['category'] for item in data)
    print("\nAvailable Categories:", ", ".join(categories))

    # Ask user to select a category
    selected_category = input("\nSelect a category: ").strip()
    filtered_questions = filter_questions_by_category(data, selected_category)

    if not filtered_questions:
        print(f"No questions available for the category '{selected_category}'.")
        return

    # Select 5 random questions from the chosen category
    questions_to_ask = random.sample(filtered_questions, min(5, len(filtered_questions)))

    total_percentage = 0
    answered_questions = 0

    # Iterate through selected questions
    for idx, item in enumerate(questions_to_ask):
        print(f"\nQuestion {idx + 1}: {item['question']}")

        # Convert speech to text
        user_answer = convert_speech_to_text()
        if not user_answer:
            print("No valid answer detected. Skipping...\n")
            continue

        # Calculate match percentage
        match_percentage = calculate_match_percentage(item['answer'], user_answer)
        total_percentage += match_percentage
        answered_questions += 1

        print(f"Actual Answer: {item['answer']}")
        print(f"Your Answer: {user_answer}")
        print(f"Match Percentage: {match_percentage:.2f}%\n")

    # Calculate and display the overall percentage
    if answered_questions > 0:
        overall_percentage = total_percentage / answered_questions
        print(f"Overall Match Percentage for {answered_questions} questions: {overall_percentage:.2f}%")
    else:
        print("No answers were provided. Overall match percentage cannot be calculated.")

if __name__ == "__main__":
    main()
