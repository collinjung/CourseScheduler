import csv
import functools
from login import *

USER = ''
WEEK = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'H': 'Thursday', 'TH': 'Thursday', 'F': 'Friday', 'SA': 'Saturday', 'S': 'Saturday', 'U': 'Sunday', 'SU': 'Sunday'}
LOG_DAYS = ''
LOG_TIME = ''


"""
------------- SEARCHING AND ADDING STANFORD COURSES --------------
    Functions:
        add_course(): Adds full text key (Including date, time, and course number/title) to the user file
        search_courses(): Searches csv containing all Stanford courses
"""
def add_course(course):
    global USER
    global LOG_DAYS
    global LOG_TIME
    print("The course you want to add is " + course['Cross-listings'] + ": " + course['Title'])
    print("This course is worth " + course['Units'] + ' unit(s).')
    if len(course['UG Reqs']) == 0:
        print("This course doesn't fulfill any UG reqs.")
    else: 
        print("This course fulfills these UG reqs: " + course['UG Reqs'])
    check = make_log_day()
    while check == 0:
        check = make_log_day()
    check = make_log_time()
    while check == 0:
        check = make_log_time()
    full_log = LOG_DAYS + '%' + LOG_TIME + '%' + course['Subject'] + course['Course Number'] + '%' + course['Title']
    with open(USER + '.txt', 'a') as f:
        f.write(full_log + '\n')
    print("Successfully added this course to your calendar.")


def search_courses():
    # Open csv containing course info
    with open('CourseList.csv', mode='r', encoding='utf-8-sig') as f:
        # Read all courses
        courses = list(csv.DictReader(f))

        # Make a list of subject names
        subjects = set()
        for subj in courses:
            subjects.add(subj['Subject'])

        # Find subject that user is searching for
        search = input("What subject are you searching for? (i.e. 'AA', 'CS')").upper()
        while search not in subjects:
            search = input("That's not a valid course subject. Please try again: ").upper()

        # Make a list of the courses in the given subject and a list consisting solely of the names of the courses
        filtered_courses = [crs for crs in courses if crs['Subject'] == search]
        filtered_courses_names = [crs['Subject'] + ' ' + crs['Course Number'] for crs in filtered_courses]
        chunks = [filtered_courses_names[i:i + 5] for i in range(0, len(filtered_courses_names), 5)]
        chunks[-1] = chunks[-1] + ['']*(len(chunks[-2]) - len(chunks[-1]))

    # Print all the courses in the filtered list
    for crs in chunks:
        print("{: >20} {: >20} {: >20} {: >20} {: >20}".format(*crs))
    
    # Print a description of the user's desired course
    course = input("Here is a list of courses with that subject. For a description of a course in this list, enter the course subject and number (i.e. 'CS 106A', 'PHYSICS 15'): ").upper()
    while course not in filtered_courses_names:
        course = input("That course doesn't exist. Please try again with a valid course subject and number: ").upper()
    print(filtered_courses[filtered_courses_names.index(course)]['Description'])

    # Add course to calendar or search for a new course
    if input("Would you like to add this course to your calendar? Y/N ").upper() in 'YES':
        add_course(filtered_courses[filtered_courses_names.index(course)])
    else:
        if input("Would you like to search for another course? Y/N ").upper() in 'YES':
            search_courses()


"""
------------- HELPER FUNCTIONS --------------
    Functions:
        make_log_day(): Makes a text key with the course date info to add to user file
        make_log_time(): Makes a text key with the course time info to add to user file
        cmp_times(): Comparison function to sort events/classes by time
"""
def make_log_day():
    global LOG_DAYS
    global WEEK
    LOG_DAYS = ''
    days = input("What day(s) of the week does this class/event meet? Please respond with either 'M, T, W, Th, F, Sa, or Su' separated by spaces if needed (ex: M T W): ")
    days = days.upper().split()
    full_days = []
    for day in days:
        if day.strip() not in WEEK:
            print("Sorry, you have inputted an invalid response. Please try again.")
            LOG_DAYS = ''
            return 0
        full_days.append(WEEK[day])
        if day == 'TH':
            day = 'H'
        if day == 'SA':
            day = 'S'
        if day == 'SU':
            day = 'N'
        LOG_DAYS += day
    days_text = ''
    for day in full_days:
        days_text += ', ' + day
    days_text = days_text[2:]
    print("Your class/event meets on " + days_text)
    if input("If this is incorrect, type 1. Otherwise, press enter to continue") == '1':
        return 0
    return 1


def make_log_time():
    global LOG_TIME
    LOG_TIME = ''
    time = input("What time does this class/event occur? Please respond with 24 hour time separated by a dash (ex: 9:30-11:30)")
    if time.count(':') != 2:
        print("Not a valid response. Please try again.")
        return 0
    times = time.split('-')
    if len(times) != 2:
        print("Not a valid response. Please try again.")
        return 0
    LOG_TIME += time
    return 1


def cmp_times(event1, event2):
    t1_start = event1[1].split('-')
    t2_start = event2[1].split('-')
    
    t1_hr_1 = t1_start[0].split(':')[0]
    t1_min_1 = t1_start[0].split(':')[1]
    t2_hr_1 = t2_start[0].split(':')[0]
    t2_min_1 = t2_start[0].split(':')[1]
    
    if t1_hr_1 != t2_hr_1:
        return int(t1_hr_1) - int(t2_hr_1)
    return int(t1_min_1) - int(t2_min_1)


"""
------------- ADD/REMOVE EVENTS FUNCTIONS --------------
    Functions:
        add_event(): Adds an event to the calendar
        del_event(): Removes an event/course from the calendar
"""
def add_event():
    title = input("What is the title of your event? ")
    description = input("Give a brief description of your event: ")
    check = make_log_day()
    while check == 0:
        check = make_log_day()
    check = make_log_time()
    while check == 0:
        check = make_log_time()
    full_log = LOG_DAYS + '%' + LOG_TIME + '%' + title + '%' + description
    with open(USER + '.txt', 'a') as f:
        f.write(full_log + '\n')
    print("Successfully added this event to your calendar.")   
 

def del_event():
    global USER
    print("Here is a list of all your events and courses")
    events = []
    with open(USER + '.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() == '':
                continue
            if line.split('%')[2] not in events:
                events.append(line.split('%')[2])
        for event in events:
            print('  ' + event)
        to_remove = input("Which class/event would you like to remove? Please input the title exactly as it appears in the list above: ")
    with open(USER + '.txt', 'w') as f:
        for line in lines:
            if line.strip() == '':
                continue
            if to_remove != line.split('%')[2]:
                f.write(line)
    print("Successfully removed " + to_remove + ' from your schedule.')


def view_calendar():
    print("Here are your current events: ")
    calendar = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
    with open(USER + '.txt', 'a') as f:
        pass
    with open(USER + '.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() == '':
                continue
            parts = line.split('%')
            days = list(parts[0])
            time = parts[1]
            title = parts[2]
            description = parts[3]
            for day in days:
                day = WEEK[day]
                calendar[day].append([title, time, description])
        for day in calendar.keys():
            sorted_list = sorted(calendar[day], key=functools.cmp_to_key(cmp_times))
            calendar[day] = sorted_list
        print("This is your current schedule: ")
        for day in calendar.keys():
            print(day)
            if len(calendar[day]) == 0:
                print("    No events for this day")
            else:
                for event in calendar[day]:
                    print('    ' + event[1].strip() + '   ', end='')
                    print(event[0].strip() + ': ' + event[2].strip())





"""
---------- UTILITY --------------
    Functions:
        menu(): Prints list of user action options
        run_program(): Runs respective program based on user input from menu() function
        main(): Logs in the user and starts up program
"""
def menu():
    print("------------------")
    print("-      Menu      -")
    print("------------------")
    print("[1] View schedule")
    print("[2] Add event to schedule")
    print("[3] Delete from schedule")
    print("[4] Search courses")
    print("[5] Quit program")
    action = input("Please enter your desired action (Number between 1-5): ")
    while action not in ['1', '2', '3', '4', '5']:
        action = input("That's not a valid action. Please try again (To view the options again, type 'help'): ")
        if action == 'help':
            print("------------------")
            print("-      Menu      -")
            print("------------------")
            print("[1] View schedule")
            print("[2] Add event to schedule")
            print("[3] Delete event from schedule")
            print("[4] Search/Add courses")
            print("[5] Quit program")
            action = input("Please enter your desired action (Number between 1-5): ")
    run_program(action)


def run_program(action):
    if action == '1':
        view_calendar()
    elif action == '2':
        add_event()
    elif action == '3':
        del_event()
    elif action == '4':
        search_courses()
    elif action == '5':
        print("See you next time! Goodbye.")
        quit()
    else:
        menu()


def main():
    print("Let's get your schedule planned!")
    global USER
    USER = account_check()
    if USER:
        while(True):
            menu()
        

if __name__ == '__main__':
    main()
