import json
import logging
from utils import calculate_age_group, validate_user_data, process_user_list


DEFAULT_MAX_USERS = 1000


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_users_from_file(filepath):
    """
    Loads user data from a JSON file.
    Has a potential error if file not found or invalid JSON.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data["users"]
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        return []
    except KeyError:
        logging.error("JSON file missing 'users' key.")
        return []
    finally:
        print("Attempted to load user data.")


def display_user_summary(users_data):
    """
    Displays a summary of processed users.
    Inefficient iteration and string concatenation.
    """
    print("\n--- User Summary ---")
    active_count = 0
    age_groups = {}

    for user in users_data:
        if user.get('status') == 'active':
            active_count += 1


        group = user['age_group']
        if group in age_groups:
            age_groups[group] += 1
        else:
            age_groups[group] = 1

    print(f"Total processed users: {len(users_data)}")
    print(f"Active users: {active_count}")
    print("Age Group Distribution:")
    for group, count in age_groups.items():
        print(f"- {group}: {count}")


def main():
    """
    Main function to run the user processing application.
    Contains multiple issues including magic numbers, lack of type hints,
    and potential for unhandled exceptions.
    """
    user_file = 'users.json'

    # Example user data for demonstration if file doesn't exist
    sample_users = [
        {"id": 1, "name": "Alice", "age": 28, "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "age": 35, "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "age": 17, "email": "charlie@example.com"},
        {"id": 4, "name": "David", "age": 42, "status": "inactive"},  # Missing email
        {"id": 5, "name": "Eve", "age": "thirty", "email": "eve@example.com"},  # Bad age type
        {"id": 6, "name": "Frank", "age": 22, "email": "frank@example.com", "status": "active"},
        {"id": 7, "name": "Grace", "age": 55, "email": "grace@example.com", "status": "active"}
    ]

    users = load_users_from_file(user_file)
    if not users:
        logging.warning(f"No users loaded from {user_file}. Using sample data.")
        users = sample_users  # Fallback to sample data

    processed_users = process_user_list(users, DEFAULT_MAX_USERS)  # Pass a global constant

    display_user_summary(processed_users)

    # A simple, potentially vulnerable operation
    user_id_to_check = 2
    if user_id_to_check in [user['id'] for user in processed_users if 'id' in user]:
        print(f"\nUser with ID {user_id_to_check} found!")
    else:
        print(f"\nUser with ID {user_id_to_check} not found.")


    temp_data = {"key": "value"}


if __name__ == "__main__":
    main()