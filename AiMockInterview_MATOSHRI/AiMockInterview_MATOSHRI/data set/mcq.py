import csv
import random

# Replace with the correct path to your file
file_path = 'data set/MCQQuestions.csv'

# Function to load CSV data
def load_csv_data(file_path):
    questions_data = []
    try:
        # Try opening the CSV file with the 'latin1' encoding
        with open(file_path, mode='r', newline='', encoding='latin1') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                questions_data.append(row)

        return questions_data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except UnicodeDecodeError:
        print(f"Error: The file '{file_path}' could not be decoded. Try using a different encoding.")
        return []

# Function to ask questions
def ask_questions(questions_data, category):
    filtered_questions = [q for q in questions_data if q['Category'].lower() == category.lower()]
    if len(filtered_questions) < 10:
        print(f"Not enough questions in the selected category '{category}'. Showing {len(filtered_questions)} questions.")
        questions_to_ask = filtered_questions
    else:
        # Select random 10 questions from the category
        questions_to_ask = random.sample(filtered_questions, 10)
    
    correct_answers = 0

    # Ask each question and check the answer
    for i, question in enumerate(questions_to_ask, 1):
        print(f"\nQuestion {i}: {question['Questions']}")
        print(f"1. {question['option 1']}")
        print(f"2. {question['option 2']}")
        print(f"3. {question['option 3']}")
        print(f"4. {question['option 4']}")
        
        # Get user's answer
        user_answer = input("Select the correct option (1/2/3/4): ").strip()

        # Determine which option corresponds to the user's selection
        selected_option = question[f'option {user_answer}'].strip()

        # Check if the selected option matches the correct answer
        correct_answer = question['Correct Answer'].strip()
        
        if selected_option == correct_answer:
            correct_answers += 1
            print("Correct!\n")
        else:
            print(f"Wrong! The correct answer was {correct_answer}.\n")

    # Calculate percentage
    percentage = (correct_answers / 10) * 100

    # Print the total correct answers and percentage
    print(f"Total correct answers: {correct_answers} out of 10")
    print(f"Your score: {percentage:.2f}%")

# Main function
def main():
    # Load the data from the CSV
    questions_data = load_csv_data(file_path)

    if questions_data:
        # List categories (convert each category to lowercase)
        categories = set(q['Category'].lower() for q in questions_data)
        print("Available Categories:")
        for category in categories:
            print(f"- {category}")
        
        # User selects a category (case-insensitive)
        selected_category = input("\nPlease select a category: ").lower()
        
        if selected_category in categories:
            ask_questions(questions_data, selected_category)
        else:
            print(f"Error: Category '{selected_category}' is not available.")
    else:
        print("No data available.")

# Run the main function
if __name__ == "__main__":
    main()
