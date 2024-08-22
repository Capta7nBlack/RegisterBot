def find_element_before_key(s, key):
    key_position = s.find(key)
    if key_position == -1:
        return None
    substring_before_key = s[:key_position].strip()
    
    # Find the last space in the substring before the key
    last_space_pos = substring_before_key.rfind(' ')
    
    if last_space_pos == -1:
        # No space found, return the string starting from the key
        return s[:key_position]
    else:
        # Construct new string excluding the element before the last space
        new_string = substring_before_key[last_space_pos:] + s[:key_position]
        return new_string

def digit_string(string):
    new = ""
    for char in string:
        if char.isdigit():
            new = new + char
    print(new)
    return new


def file_reader(schedule):
    with open(schedule, 'r') as file:
        courses = {}
        for line in file:
            if not line.strip():
                continue
            
            # Skip lines without a colon
            if ':' not in line:
                continue

            course_name, sections = line.strip().split(':')
            
            
            section = sections.split(",")
            
            for item in section:
                print(item)
                item = item.strip()
                print(item)
            if len(section) == 3:
                lecture = digit_string(section[0])
                lab_section = digit_string(section[1])
                recitation = digit_string(section[2])
                courses[course_name] = {
                    'lecture' : f'{lecture}',
                    'lab_section' : f'{lab_section}',
                    'recitation' : f'{recitation}'
                }
            elif len(section) == 2:
                for idx, _ in enumerate(section):

                    lecture = find_element_before_key(section[idx], "L")
                    if lecture:
                        print("in file_reader where lecture = find_element_before_key")
                        print(lecture)
                        break
                for idx, _ in enumerate(section):

                    lab_section = (find_element_before_key(section[idx], "Lb"))
                    if lab_section:
                        print("in file_reader where lecture = find_element_before_key")
                        print(lab_section)
                        break
                for idx, _ in enumerate(section):

                    recitation = (find_element_before_key(section[idx], "R"))
                    if recitation:
                        break
                for idx, _ in enumerate(section):

                    seminar = (find_element_before_key(section[idx], "S"))
                    if seminar:
                        break
            
                
                if lab_section:
                    lecture = digit_string(lecture)
                    lab_section = digit_string(lab_section)
                    courses[course_name] = {
                        'lecture' : f'{lecture}',
                        'lab_section' : f'{lab_section}'
                    }
                elif recitation:
                    lecture = digit_string(lecture)
                    recitation = digit_string(recitation)
                    courses[course_name] = {
                    'lecture' : f'{lecture}',
                    'recitation' : f'{recitation}'
                    }
                elif seminar:
                    lecture = digit_string(lecture)
                    seminar = digit_string(seminar)
                    courses[course_name] = {
                        'lecture' : f'{lecture}',
                        'seminar' : f'{seminar}'
                    }
            elif len(section) == 1:
                lab_section = (find_element_before_key(section[0], "Lb"))
                seminar = (find_element_before_key(section[0], "S"))
                if lab_section:
                    lab_section = digit_string(lab_section)
                    courses[course_name] = {
                        'lab_section' : f'{lab_section}'

                    }
                elif seminar:
                    seminar = digit_string(seminar)
                    courses[course_name] = {
                        'seminar' : f'{seminar}'
                    }
                else:
                    lecture = digit_string(section[0])
                    courses[course_name] = {
                        'lecture' : f'{lecture}'
                    }
            else:
                print("The file either has more than 3 sections or no written. Both are incorrect.")
        return courses
    


def dict_reader_lab(dict, course):
    sections = []

    inside_keys = list(dict[course].keys())

    values = list(dict[course].values())

    for idx, inside_key in enumerate(inside_keys):
         
        if inside_keys[idx] == 'lab_section':
            
            
            sections.append(f'Section {values[idx]}')
            print(inside_keys[idx])
            print(sections[0])
            return sections[0]
    else:
        return None
    


def dict_reader_lecture(dict, course):
    sections = []

    inside_keys = list(dict[course].keys())

    values = list(dict[course].values())


    for idx, inside_key in enumerate(inside_keys):
         
        if inside_keys[idx] == 'lecture':
            sections.append(f'Section {values[idx]}')
            print(inside_keys[idx])
            print(sections[0])
            return sections[0]
    else:
        return None
    


def dict_reader_recitation(dict,course):

    sections = []

    inside_keys = list(dict[course].keys())

    values = list(dict[course].values())

    for idx, inside_key in enumerate(inside_keys):
         
        if inside_keys[idx] == 'recitation':
            sections.append(f'Section {values[idx]}')
            return sections[0]
    else:
        return None
    



def dict_reader_seminar(dict, course):
    sections = []
    

    
    
    inside_keys = list(dict[course].keys())

    values = list(dict[course].values())


    for idx, inside_key in enumerate(inside_keys):
         
        if inside_keys[idx] == 'seminar':
            sections.append(f'Section {values[idx]}')
            return sections[0]
    else:
        return None