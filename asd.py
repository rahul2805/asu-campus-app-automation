# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import Select

# classname = "drop-caption__border"

# brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# options = webdriver.ChromeOptions()
# options.binary_location = brave_path

# driver = webdriver.Chrome("G:/CIS345/chromedriver.exe", options=options)
# driver.get("https://pdftoimage.com/")



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

# def drag_and_drop_file(drop_target, path):
#     print(drop_target.parent)
#     driver = drop_target.parent
#     file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
#     file_input.send_keys(path)


# driver.maximize_window()
# filepath = "C:/Users/DELL/Desktop/FOA/FOA-20210426T033243Z-001/FOA-20210426T033243Z-001/FOA/Homework_1.pdf"

# drag_and_drop_file(driver.find_element(By.CLASS_NAME, classname), filepath)
# time.sleep(15)


from fpdf import FPDF
import datetime
 
pdf = FPDF()
 
pdf.add_page()
pdf.set_font("Times", size = 12)
 
f = open("G:/CIS345/Automation jobs/CL.txt", "r", encoding="latin-1")

mydate = datetime.datetime.now()
today = mydate.strftime("%B") + " " + str(datetime.date.today().day) + ", " + str(datetime.date.today().year)
print("Current day:", today)

for i, x in enumerate(f):
    if i == 0:
        pdf.multi_cell(200,5, txt = today + "\n"+"\n", align = 'L')
        continue
    if i == 4:
        idx = x.index("opening for a") + 13 + 1
        x = x[0: idx] + "Full Stack Developer" + x[idx:] #job_name[i]
        idx = x.index("through the University") - 1
        x = x[0: idx] + "the EdPlus" + x[idx:] #job_name[i]
    pdf.multi_cell(200,5, txt = x+ "\n", align = 'L')
  
pdf.output("samplee.pdf")  