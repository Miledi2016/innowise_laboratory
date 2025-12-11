CURRENT_YEAR = 2025

def generate_profile(age: int) ->str:
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"

def main():
    user_name = input("Enter your full name:  ")

    birth_year = input("Enter your birth year: ")
    birth_year = int(birth_year)

    current_age = CURRENT_YEAR - birth_year

    hobbies = []


    while True:
        hobby = input("Enter your favorite hobby or type 'stop' to finish: ")
        if hobby.lower() == 'stop':
            break

        if hobby.strip():
            hobbies.append(hobby.strip())


    life_stage = generate_profile(current_age)

    user_profile = {
        "name": user_name,
         "age": current_age,
         "birth_year": birth_year,
         "life_stage": life_stage,
         "hobbies": hobbies
    }

    print("\n---")
    print(f"Name: {user_profile['name']}")
    print(f"Age: {user_profile['age']}")
    print(f"Life Stage: {user_profile['life_stage']}")


    if not user_profile['hobbies']:
        print("You didn't mention any hobbies")
    else:
        num_hobbies = len(user_profile['hobbies'])
        print(f"favorite hobbies ({num_hobbies}): ")
    for hobby in user_profile ['hobbies']:
        print (f"-{hobby}")

    print("---")


if __name__ == "__main__":
    main()




