import datetime

# Asks for user inputs - returns tuple of length
# 3 containing start_date, end_date, and query - all strings
def get_inputs() -> tuple:
    # Sub-function to check date - If it is valid -> True, if not -> False
    def date_checker(string_date: str) -> bool:
        # If the user inputs an incorrect format, the length will not be 10.
        if len(string_date) != 10:
            return False

        # Turn string to number
        string_date = string_date.replace("-", "")

        # Must check if all non-hyphen chars are numbers
        if not string_date.isdigit():
            return False

        # Convert each component to an int - total date, year, and month
        int_date = int(string_date)
        year, month, day = (int(string_date[:4]),
                                int(string_date[4:6]),
                                int(string_date[6:]))

        # Check if date is within oldest and newest APOD entries
        current_date = str(datetime.date.today()).replace("-", "")
        if not 19950616 <= int_date <= int(current_date):
            return False

        # Check if month is valid
        if not 1 <= month <= 12:
            return False

        # Check if day is valid for 31 day months
        if month in (1, 3, 5, 7, 8, 10, 12):
            if not 1 <= day <= 31:
                return False

        # Special case for Feb. on leap-years
        elif year % 4 != 0 and month == 2:
            if not 1 <= day <= 28:
                return False

        # Special case for Feb.
        elif year % 4 == 0 and month == 2:
            if not 1 <= day <= 29:
                return False

        # Otherwise check if day fits within 30
        elif not 1 <= day <= 30:
            return False

        return True

    # Loop to ask for start date until valid input is received
    while True:
        # Ask for date
        start_date = input('Start date YYYY-MM-DD: ')

        # None string will be replaced with default Jan. 2024 in build_url()
        if not start_date:
            break

        # Otherwise must be valid
        elif date_checker(start_date):
            break

    # Loop to ask for end date until valid input is received
    while True:
        # Ask for date
        end_date = input('End date YYYY-MM-DD: ')

        # If both inputs are none - will default to January
        if not end_date and not start_date:
            break

        # If end date is valid we need to check if it is after start date
        elif date_checker(end_date):
            int_end_date = int(end_date.replace("-", ""))

            # If start_date doesn't exist check if it is after default date
            if not start_date and int_end_date >= 20240101:
                break

            # Else check if it's greater than inputted start date
            else:
                int_start_date = int(start_date.replace("-", ""))

                if int_end_date >= int_start_date:
                    break

    # Loop to ask for query until valid input received
    while True:
        search_query = input('Query: ')

        # Only if a valid word is submitted can we search - then break loop
        if search_query.strip():
            search_query = search_query.lower()
            break

    # These are all strings
    return start_date, end_date, search_query

# Function to score and filter results based on query
def search_description(search_result: dict, query: str) -> tuple:
    # Split words of query into list by whitespaces - destroy repeat entries by converting to set and back to list
    query_list = list(set(query.split()))

    # Counter for most and 2nd most matches
    most_matches = -1
    second_most_matches = -2

    # Lists for duplicate cases
    first_possibilities = []
    second_possibilities = []

    # Looping through each entry in the search result
    for dic in search_result:
        # Ensure URL is not Youtube
        if "youtube" not in dic["url"]:
            # Wipe query match counter after searching each entry
            matches = 0
            explanation_list = dic["explanation"].lower().split()
            # Loop through query list and explanation list to find number of matches
            for query in query_list:
                for explanation in explanation_list:
                    if query == explanation:
                        matches += 1

            # If greater than or equal to the greatest counter
            if matches >= most_matches:

                # If equivalent update duplicate list
                if matches == most_matches:
                    first_possibilities.append(dic["url"])

                # Otherwise pass current duplicate list to second and clear first
                else:
                    second_possibilities.clear()
                    second_possibilities += first_possibilities
                    first_possibilities = [dic["url"]]

                # Finally update second counter to match first and first to match current number of hits
                second_most_matches = most_matches
                most_matches = matches

            # Only if greater than 2nd counter but not more than 1st
            elif matches >= second_most_matches:

                # If duplicate add to list
                if matches == second_most_matches:
                    second_possibilities.append(dic["url"])

                # If greater clear list and make new one
                else:
                    second_possibilities = [dic["url"]]

                # Update second counter
                second_most_matches = matches

    # If there's only one greatest hit and multiple 2nd greatest hits, 2nd greatest needs to be the first in the original search_result dict
    if len(first_possibilities) == 1:
        best_url = first_possibilities[0]
        second_best_url = second_possibilities[0]

    # If there's multiple 1st greatest hits, 1st greatest needs to be second-to-last and 2nd, last, entries of the search_result dict
    else:
        best_url = first_possibilities[-2]
        second_best_url = first_possibilities[-1]

    return best_url, second_best_url
