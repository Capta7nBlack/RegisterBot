from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
from reader import file_reader, dict_reader_lab, dict_reader_lecture, dict_reader_recitation, dict_reader_seminar



email = ""
password = ""



courses = file_reader("schedule.txt")
print(courses)



start_time = time.time()

def time_since_launch():
    """Returns the time in seconds since the program was launched."""
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time



# if len(courses) == 3:
#     course = list(courses.keys())[0]
#     lecture_section = courses[0][0]






class DriverManager:
    _instance = None

    @staticmethod
    def get_driver():
        if DriverManager._instance is None:
            options = Options()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-notifications')
            options.add_experimental_option("detach", True)
            options.add_experimental_option("prefs",{ "profile.managed_default_content_settings.images": 2,})

            # options.add_argument('--headless=new')
            DriverManager._instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return DriverManager._instance




driver = DriverManager.get_driver()
if len(email) == 0:
    raise ValueError("The email value is invalid, probably empty")
if len(password) == 0:
    raise ValueError("The password value is invalid, probably empty")
try:
    
    driver.maximize_window()
    driver.get('https://registrar.nu.edu.kz/user/login')
    print ("Opened registrar")

    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "name"))
    ).send_keys(email)
    print ("Email entered")


    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "pass"))
    ).send_keys(password)
    print ("Password entered")


    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "op"))
    ).click()

    print("Seeking for course registration button")

    print(f"Time since launch: {time_since_launch()} seconds")
    Switch = True
    while(Switch):
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Course registration']"))).click()
            print("Clicked Course registration button")
            Switch = False
        except:
            driver.refresh()
            print("The course registration button was not found. Refreshing the page")
    
    # driver.get("https://registrar.nu.edu.kz/my-registrar/course-registration")
    # TO make use of buttons as after first circle html code is remembered
    
    for course in courses:
        # if driver.current_url() !="https://registrar.nu.edu.kz/my-registrar/course-registration":
        driver.get("https://registrar.nu.edu.kz/my-registrar/course-registration")

        schedule = False
        try:
            search = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "titleText-inputEl")))
            search.send_keys(course)
            
            print(f"Wrote course name into search: {course}")
        except:
            print("Could not write course name into search")
            
        try:
            enter = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "show_courses_button-btnIconEl")))
            enter.click()
            print("Pressed enter")
        except:
            print("Could not press enter")
        
        try:
            print(f"Checking whether the course - {course} - is accessible")
            open = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[text()='OPEN']")))
            open.click()
            schedule = True
            print(f"The course - {course} - is accessible")    
            open.click()
            try:
                add = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//a[@class='green-button'  and contains(text(), 'Add to Selected Courses')] ")))
                add.click()
                print(f"Added course - {course} - to the schedule table")
            except:
                print(f"Could not add the course - {course} - in the schedule table")
        
        except:
            print(f"The course - {course} - is not open or is already in schedule table")
            
        try: 
            if not schedule:
                selected = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[text()='SELECTED COURSE']")))
                schedule = True
                print(f"The course - {course} - was skipped due it not having the priority to register")
                
        except:
            pass
      
        try: 
            if not schedule:
                priority = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[text()='You are not in the current priority. Please check the priority requirements.']")))
                schedule = True
                print(f"The course - {course} - was skipped due it not having the priority to register")
                continue
        except:
            pass

        try:
            if not schedule:
                registered = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), \"Instructor's Permission Required. Registration through Add Course form only!\")]")))
                print(f"The course - {course} - was skipped due it not having the instruction's persimission to register")
                continue
        except:
            pass

        try:
            if not schedule:
                instruction_permission = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COURSE REGISTERED')]")))
                print(f"The course - {course} - was skipped because it is already registered")
                continue
        except:
            pass


        print(f"Time since launch: {time_since_launch()} seconds")

        
        driver.get("https://registrar.nu.edu.kz/my-registrar/course-registration/selected")
        time.sleep(1)
    
        lecture_section = dict_reader_lecture(courses, course)
        lab_section = dict_reader_lab(courses, course)
        recitation_section = dict_reader_recitation(courses, course)
        seminar_section = dict_reader_seminar(courses, course)
        print(lecture_section)

        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, f"course-cloud")))
            driver.find_element(By.XPATH, f"//span[contains(text(), '{course.upper()}')]").click()

            print(f"Pressed the course - {course} in the schedule table")
        except:
            print(f"Could not press the course - {course} in the schedule table")
            pass

        # Lecture
        if lecture_section:
            try:
                print(f"Trying to find section for course - {course}")
                print(lecture_section)
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//input[@value='{lecture_section}' and contains(@name, 'Lecture')]"))).click()
                print(f"Clicked on {lecture_section} for course - {course}")
            except:
                print(f"Could not find the {lecture_section} for {course}")
                pass

        # Lab section
        if lab_section:
            try:
                print(f"Trying to find section for course - {course}")
                print(lab_section)
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//input[@value='{lab_section}' and contains(@name, 'Lab')]"))).click()
                print(f"Clicked on {lab_section} for course - {course}")
            except:
                print(f"Could not find the {lab_section} for {course}")
                pass
        # Recitation
        if recitation_section:
            print(recitation_section)
            
            try:
                print(f"Trying to find section for course - {course}")
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//input[@value='{recitation_section}' and contains(@name, 'Recitation')]"))).click()
                print(f"Clicked on {recitation_section} for course - {course}")
            except:
                print(f"Could not find the {recitation_section} for {course}")
                pass
        

        # SEMINAR
        if seminar_section:
            
            try:
                print(f"Trying to find section for course - {course}")
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//input[@value='{seminar_section}' and contains(@name, 'Seminar')]"))).click()
                print(f"Clicked on {seminar_section} for course - {course}")
            except:
                print(f"Could not find the {seminar_section} for {course}")
                pass


        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//a[@class='green-button'  and contains(text(), 'Register')] "))).click()
            print(f"The course {course} has been registered successfuly")
        except:
            print(f"The register button was not found for {course}")
            pass

        # WAITLIST ACCEPTANCE HANDLING
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "button-1006-btnIconEl"))).click()
            print("Accepted Waitlist")
        except:
            pass


        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "button-1005-btnIconEl"))).click()
            print("The register button was closed")
        except:
            print("Could not close register button")
            pass
except Exception as e:
    pass
#     print("The error catched: ", e)

#     # Wait for 3 seconds

print(f"Time since launch: {time_since_launch()} seconds")