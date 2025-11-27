from typing import List, Dict, Union, Optional, Any

Student = Dict[str, Union[str, List[int]]]
students: List[Student] = []


def find_student(name: str) -> Optional[Student]:
    """Helper function to find a student by name (case-insensitive)."""
    for student in students:
        if student['name'].lower() == name.lower():
            return student  # type: ignore
    return None


def add_new_student() -> None:
    """Handles Option 1: Add a new student."""
    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    if find_student(name):
        print(f"Student '{name}' already exists.")
    else:
        new_student: Student = {'name': name, 'grades': []}
        students.append(new_student)


def add_grades_to_student() -> None:
    """Handles Option 2: Add grades to a student."""
    name = input("Enter student name: ").strip()

    student = find_student(name)

    if student is None:
        print(f"Student '{name}' not found.")
        return


    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip()

        if grade_input.lower() == 'done':
            break

        try:
            grade = int(grade_input)

            if 0 <= grade <= 100:
                student['grades'].append(grade)  # type: ignore
            else:
                print("Invalid input. Grade must be between 0 and 100.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def calculate_average(grades: List[int]) -> Optional[float]:
    """Calculates the average grade. Handles ZeroDivisionError for empty lists."""
    try:
        if not grades:
            raise ZeroDivisionError
        return sum(grades) / len(grades)
    except ZeroDivisionError:
        return None


def show_report() -> None:
    """Handles Option 3: Show Report (All Students)."""
    print("--- Student Report ---")

    if not students:
        print("Student list is empty. Please add students first.")
        return

    report_data: List[float] = []
    has_valid_grades = False

    for student in students:
        avg = calculate_average(student['grades'])
        student_name = student['name']

        if avg is None:
            print(f"{student_name}'s average grade is N/A.")
        else:
            formatted_avg = f"{avg:.1f}"
            print(f"{student_name}'s average grade is {formatted_avg}.")
            report_data.append(avg)
            has_valid_grades = True

    print("-" * 20)

    if has_valid_grades:
        max_avg = max(report_data)
        min_avg = min(report_data)
        overall_avg = sum(report_data) / len(report_data)

        print(f"Max Average: {max_avg:.1f}")
        print(f"Min Average: {min_avg:.1f}")
        print(f"Overall Average: {overall_avg:.1f}")


def find_best_performer() -> None:
    """Handles Option 4: Find the best performer."""
    if not students:
        print("Student list is empty.")
        return

    def get_avg_for_max(student: Student) -> float:
        avg = calculate_average(student['grades'])  # type: ignore
        return avg if avg is not None else -1.0

    try:
        best_student: Student = max(students, key=get_avg_for_max)
        best_avg = calculate_average(best_student['grades'])  # type: ignore

        if best_avg is None or best_avg == -1.0:
            print("No student has grades. Cannot determine the best performer.")
        else:
            print(f"The student with the highest average is {best_student['name']} with a grade of {best_avg:.1f}.")

    except ValueError:
        print("Error occurred while trying to find the best student.")


def main_menu() -> None:
    """Main function containing the menu loop."""
    first_run = True

    while True:
        if first_run:
            print("--- Student Grade Analyzer ---")
            print("1. Add a new student")
            print("2. Add grades for a student")
            print("3. Generate a full report")
            print("4. Find the top student")
            print("5. Exit program")
            first_run = False
        else:
            print("\n--- Student Grade Analyzer ---")
            print("1. Add a new student")
            print("...")

        try:
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                add_new_student()
            elif choice == '2':
                add_grades_to_student()
            elif choice == '3':
                show_report()
            elif choice == '4':
                find_best_performer()
            elif choice == '5':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main_menu()
