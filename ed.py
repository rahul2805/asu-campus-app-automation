import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""
# KEYWORDS = ["aide", "researcher", "IT", "Front Desk", "Office", "Tutor", "Software", "Developer", "Website", "Computer",
            # "Grader", "Data Science", "Data Analyst"]
KEYWORDS = ["Interviewer", "researcher", "IT", "research", "Software", "Developer", "Website", "Computer", "Data Science", "Data Analyst"]

filepath_CL = "G:/CIS345/Automation jobs/samplee.pdf"

def search_page(driver):
    driver.find_element("xpath", "//button[@class='primaryButton ladda-button ng-binding']").click()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='auth-button'][type='submit']"))).click()

    except TimeoutException:
        print("Timed out waiting for page to load")
    
    job_links = driver.find_element("xpath", "//a[@class = 'jobProperty jobtitle']")
    print(job_links)

def drag_and_drop_file(drop_target, path):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)

def apply(driver, link, job_name):
    driver.get(link)
    time.sleep(2)
    # ""
    #Dept Name
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//p[@class='answer ng-scope section2LeftfieldsInJobDetails']")))
    except TimeoutException:
        pass
    dept_name = driver.find_elements("xpath", "//p[@class='answer ng-scope section2LeftfieldsInJobDetails']")[1].text

    createCL(job_name, dept_name)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@id='appLbl']")))
        return
    except TimeoutException:
        print("Timed out waiting for page to load")
    driver.find_element("xpath", "//button[@id = 'applyFromDetailBtn']").click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id = 'startapply']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//button[@id = 'startapply']").click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='shownext']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//button[@id = 'shownext']").click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id = 'radio-44674-Yes']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//input[@id = 'radio-44674-Yes']").click()

    driver.find_element("xpath", "//input[@id = 'radio-61829-No']").click()
    
    driver.find_element("xpath", "//span[@class = 'ui-selectmenu-icon ui-icon ui-icon-triangle-1-s linkColor']").click()
    # driver.implicitly_wait(3)
    try:
        driver.maximize_window()
    except:
        pass
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ui-selectmenu-menu ui-front ui-selectmenu-open']//ul//li[text()='ASU Employee Referral']"))).click()
    except TimeoutException:
        pass
    action = webdriver.ActionChains(driver)
    element = driver.find_element(By.ID, 'custom_44925_1291_fname_slt_0_44925-button_text') # or your another selector here
    action.move_to_element(element)
    action.perform()
    action.move_by_offset(0, -20)  
    action.perform()
    action.move_to_element(driver.find_element(By.ID, 'ui-id-7'))
    action.click().perform()

    driver.find_element("xpath", "//button[@id = 'shownext']").click()

    ##Adding a resume
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[@id='AddResumeLink']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//a[@id = 'AddResumeLink']").click()
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='profileBuilder']")))
    except TimeoutException:
        pass
    iframe = driver.find_element(By.XPATH, "//iframe[@id='profileBuilder']")
    driver.switch_to.frame(iframe)

    driver.find_element(By.XPATH, "//button[@id='btnSelectedSavedRC']").click()
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id = '32']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//input[@id = '32']").click()
    driver.find_element(By.XPATH, "//button[@class='primaryButton' and @type='button']").click()
    
    driver.switch_to.default_content()
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@id = 'AddCLLink']"))).click()
    except TimeoutException:
        pass

    ##Adding Cover letter
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='profileBuilder']")))
    except TimeoutException:
        pass
    iframe = driver.find_element(By.XPATH, "//iframe[@id='profileBuilder']")
    driver.switch_to.frame(iframe)

    drag_and_drop_file(driver.find_element(By.XPATH, "//button[@id='btnSelectedSavedRC']"), filepath_CL)
    time.sleep(10)

    # driver.find_element(By.XPATH, "//button[@id='btnSelectedSavedRC']").click()
    # try:
    #     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id = '37']")))
    # except TimeoutException:
    #     pass
    # driver.find_element("xpath", "//input[@id = '37']").click()
    # driver.find_element(By.XPATH, "//button[@class='primaryButton' and @type='button']").click()
    
    driver.switch_to.default_content()
    time.sleep(1)
    driver.find_element("xpath", "//button[@id = 'shownext']").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id = 'shownext']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//button[@id = 'shownext']").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id = 'shownext']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//button[@id = 'shownext']").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id = 'shownext']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//button[@id = 'shownext']").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id = 'shownext']")))
    except TimeoutException:
        pass
    driver.find_element("xpath", "//button[@id = 'shownext']").click()
    time.sleep(3)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@id = 'save']"))).click()
    except TimeoutException:
        pass
    # driver.find_element("xpath", "//button[@id = 'save']").click()
    time.sleep(4)
    
def createCL(job_name, dept):
    pdf = FPDF()

    pdf.add_page()
    pdf.set_font("Times", size = 12)

    f = open("G:/CIS345/Automation jobs/CL.txt", "r", encoding="latin-1")

    mydate = datetime.datetime.now()
    today = mydate.strftime("%B") + " " + str(datetime.date.today().day) + ", " + str(datetime.date.today().year)

    for i, x in enumerate(f):
        if i == 0:
            pdf.multi_cell(200,5, txt = today + "\n"+"\n", align = 'L')
            continue
        if i == 4:
            idx = x.index("opening for a") + 13 + 1
            x = x[0: idx] + job_name + x[idx:] #job_name[i]
            idx = x.index("through the University") - 1
            x = x[0: idx] + dept + x[idx:] #job_name[i]
        pdf.multi_cell(200,5, txt = x+ "\n", align = 'L')
    
    pdf.output("samplee.pdf")  


brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path

driver = webdriver.Chrome("G:/CIS345/chromedriver.exe", options=options)
# print(driver.title)
driver.get("https://students.asu.edu/employment/search")
# search_bar = driver.find_element_by_name("q")
# search_bar.clear()
driver.find_element("xpath", "//button[text()='Search On-Campus Jobs']").click()

delay = 10
username = "skamble3"
password = "Sub0dh_kamb1e"
driver.find_element("id", "username").send_keys(username)
driver.find_element("id", "password").send_keys(password)
driver.find_element("xpath", "//input[@type='submit' and @value='Sign In']").click()
# time.sleep(10)
timeout = 10
try:
    # element_present = EC.presence_of_element_located((By.XPATH , "//div[@class='label factor-label']"))
    # WebDriverWait(driver, timeout).until(element_present)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='auth-button'][type='submit']"))).click()

except TimeoutException:
    print("Timed out waiting for page to load")


iframe = driver.find_element(By.XPATH, "//iframe[@id='duo_iframe']")
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, "//div[@id='auth_methods']/fieldset/div[1]/button").click()

driver.switch_to.default_content()

# search_page(driver)
try:
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='primaryButton ladda-button ng-binding']"))).click()
except TimeoutException:
    print("Timed out waiting for page to load")
# driver.find_element("xpath", "//button[@class='primaryButton ladda-button ng-binding']").click()
try:
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='auth-button'][type='submit']"))).click()
except TimeoutException:
    print("Timed out waiting for page to load")

time.sleep(1)

FWS = "(FWS Eligible)"
# Click next button till appear
while(True):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(("xpath", "//a[@id = 'showMoreJobs']"))).click()
    except Exception:
        print("Running out of jobs, Kill yourself if you still didn't get it.")
        break

x = driver.find_elements("xpath", "//a[@class = 'jobProperty jobtitle']")
job_links = []
job_names = []
for jb in x:
    name = jb.text
    include = False
    for k in KEYWORDS:
        if k in name:
            include = True
            break
    if include:
        job_links.append(jb.get_attribute("href"))
        if FWS in name:
            name = name.replace(FWS, "")
            name = name.strip()
        job_names.append(name)

for i,job_link in enumerate(job_links):
    apply(driver, job_link, job_names[i])
    break
# print(job_names)
# search_bar.send_keys(Keys.RETURN)
# print(driver.current_url)
# driver.close()