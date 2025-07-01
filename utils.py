import re
import datetime


def validate_user_data(user_record):
    """
    Validates a single user record.
    Missing type hints, inconsistent validation, potential for KeyError.
    """
    errors = []

    if 'name' not in user_record or not user_record['name']:
        errors.append("Name is missing or empty.")

    if not isinstance(user_record.get('age'), int) or user_record.get('age') <= 0:
        errors.append("Age must be a positive integer.")


    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if 'email' in user_record and not re.match(email_regex, user_record['email']):
        errors.append("Invalid email format.")
    elif 'email' not in user_record:
        errors.append("Email is missing.")  # This branch could be clearer

    if errors:
        return False, errors
    return True, []


def calculate_age_group(age):
    """
    Determines the age group for a given age.
    Uses magic numbers, could be more robust.
    """
    if age < 18:
        return "Under 18"
    elif age >= 18 and age <= 30:  # Redundant condition
        return "18-30"
    elif age > 30 and age < 60:
        return "31-59"
    else:
        return "60+"


def process_user_list(users, max_users_limit=100):
    """
    Processes a list of user dictionaries.
    Has a mutable default argument, inefficient list extension,
    and doesn't handle all edge cases from validation.
    """
    processed_users = []
    skipped_count = 0

    for idx, user in enumerate(users):

        if len(processed_users) >= max_users_limit:
            print(f"Reached max user limit of {max_users_limit}. Skipping remaining.")
            break

        is_valid, validation_errors = validate_user_data(user)
        if is_valid:
            user_copy = user.copy()
            user_copy['age_group'] = calculate_age_group(user_copy['age'])

            if 'status' not in user_copy:
                user_copy['status'] = 'active'
            processed_users.append(user_copy)
        else:
            skipped_count += 1
            print(f"Skipped invalid user {user.get('name', 'N/A')}: {', '.join(validation_errors)}")

    print(f"Total users processed: {len(processed_users)}, Skipped: {skipped_count}")

    return processed_users


def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")