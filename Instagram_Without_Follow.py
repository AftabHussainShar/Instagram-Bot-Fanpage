from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# 59
# user
user = input('Enter User To Follows : ')
with open('user_credentials.txt', 'r') as file:
    lines_content = file.read()
    lines_content_comp = lines_content.split(',')
    Username = lines_content_comp[0]
    Password = lines_content_comp[-1]

#Chrome options and driver
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-geolocation")
chrome_options.add_argument("--disable-features=Geolocation")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.get("https://www.instagram.com/")
time.sleep(10)
try:
    accept_cookies_button = driver.find_element(By.XPATH,"//button[text()='Allow all cookies']")
    accept_cookies_button.click()
except:
    pass
# Set to store processed URLs
clicked_posts = set()
clicked_reels = set()
visited_profiles = set()
processed_urls = set()

# Function to read existing URLs from text files
def read_urls_from_file(filename):
    urls = set()
    try:
        with open(filename, "r") as f:
            for line in f:
                urls.add(line.strip())
    except FileNotFoundError:
        print(f"File '{filename}' not found. Creating a new one.")
    return urls

# Read existing URLs from text files
clicked_posts = read_urls_from_file("posts.txt")
visited_profiles = read_urls_from_file("profiles.txt")

username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

#credentials
username.clear()
password.clear()
username.send_keys(Username)
password.send_keys(Password)
login_button.click()
time.sleep(10)

#not now
try:
    not_now_button = driver.find_element(By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37'][text()='Not now']")
    not_now_button.click()
except NoSuchElementException:
    print("Not now button not found.")
    
time.sleep(4)

#not now
try:
    not_now_button = driver.find_element(By.XPATH, "//button[@class='_a9-- _ap36 _a9_1']")
    not_now_button.click()
except NoSuchElementException:
    print("Not now button not found.")
    
#click on search
try:
    search_button = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Search"]')
    search_button.click()
    print("Search button clicked.")
except Exception as e:
    print("Error:", e)

# write username    
try:
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search input"]')
    search_input.send_keys(user)
    #search_input.send_keys(Keys.ENTER)
    print("Keys sent to the search box.")
except Exception as e:
    print("Error:", e)
    
# take fist user
try:
    time.sleep(4)
    anchor_elements = driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3")
    if anchor_elements:
        first_anchor = anchor_elements[1]
        first_anchor.click()
    else:
        print("No anchor elements with the specified class found.")
except Exception:
    print("Error: Failed to find anchor elements.")
    

time.sleep(7)

# Function to scroll
def scroll_to_end():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  

while True:
    old_height = driver.execute_script("return document.body.scrollHeight")
    scroll_to_end()
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == old_height:
        break
    
# Find all posts
posts = driver.find_elements(By.XPATH, "//div[contains(@class,'x1lliihq')]/a[contains(@href, '/p/')]")
reels = driver.find_elements(By.XPATH, "//a[contains(@class, 'x1i10hfl') and contains(@href, '/reel/')]")
posts = posts + reels


def wait_for_element_to_be_clickable(xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

# English detect unction 
def is_english(text):
    return all(ord(char) < 128 for char in text)

#load more comments
def click_load_more_comments():
    try:
        while True:
            load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xdj266r.xat24cr.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.xl56j7k")))
            if load_more_button:
                load_more_button.click()
                time.sleep(2)
            else:
                break
    except Exception:
        print("Load All Comments")

# Iterate through each post
for post in posts:
    post_href = post.get_attribute('href')
    if '/p/' in post_href:  # If it's a post
        post_id = post_href.split('/p/')[1].split('/')[0]
    elif '/reel/' in post_href:  # If it's a reel
        post_id = post_href.split('/reel/')[1].split('/')[0]
    else:
        print("Unknown item type:", post_href)
        continue
    
    # Click on the post
    if post_id not in clicked_posts:
        driver.execute_script("arguments[0].scrollIntoView();", post)
        time.sleep(1) 
        post.click()
        time.sleep(2)  
        clicked_posts.add(post_id)
        with open('posts.txt', 'a') as f:
            f.write(post_id + '\n')
            
        click_load_more_comments()
        
        # Collect All Comments
        list_items = driver.find_elements(By.XPATH, "//li[contains(@class, '_a9zj') and .//span[@class='_ap3a _aaco _aacu _aacx _aad7 _aade']]")

        # Read comments
        for list_item in list_items:
            comment_text_element = list_item.find_element(By.XPATH, ".//span[@class='_ap3a _aaco _aacu _aacx _aad7 _aade']")
            comment_text = comment_text_element.text
        
            if is_english(comment_text):
                
                # Like the post
                try:
                    span_element = list_item.find_element(By.XPATH, ".//span[@class='_a9zu']")
                    span_element.click()
                    time.sleep(1)
                    print("Click Like button-Comment")
                except Exception as e:
                    print("Not Like button-Comment")
                time.sleep(1)
                try:
                    a_elements = list_item.find_elements(By.TAG_NAME, "a")
                    if a_elements:
                        href = a_elements[0].get_attribute("href")
                        if href in visited_profiles:
                            print("URL already processed:", href)
                        else:
                            ActionChains(driver).key_down(Keys.CONTROL).click(a_elements[0]).key_up(Keys.CONTROL).perform()
                            driver.switch_to.window(driver.window_handles[-1])
                            visited_profiles.add(href)
                            with open("profiles.txt", "a") as f:
                                f.write(href + "\n")  
                            try:
                                # Follow the user
                                # button_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, '_acan')]")))
                                # button_element.click()
                                time.sleep(12)
                                
                                #like max posts 
                                posts = driver.find_elements(By.XPATH, "//div[contains(@class,'x1lliihq')]/a[contains(@href, '/p/')]")
                                reels = driver.find_elements(By.XPATH, "//a[contains(@class, 'x1i10hfl') and contains(@href, '/reel/')]")
                                posts = posts + reels
                                ip=0
                                #itrate through posts
                                for post in posts:
                                    if ip==4:
                                        break
                                    post_href = post.get_attribute('href')
                                    if '/p/' in post_href:  # If it's a post
                                        post_id = post_href.split('/p/')[1].split('/')[0]
                                    elif '/reel/' in post_href:  # If it's a reel
                                        post_id = post_href.split('/reel/')[1].split('/')[0]
                                    else:
                                        print("Unknown item type:", post_href)
                                        continue
                                    if post_id not in clicked_posts:
                                        driver.execute_script("arguments[0].scrollIntoView();", post)
                                        time.sleep(1) 
                                        post.click()
                                        # Like the post
                                        try:
                                            time.sleep(2)
                                            x, y = pyautogui.locateCenterOnScreen('like.png', confidence=0.5)
                                            x = x - 30
                                            pyautogui.click(x, y)
                                            time.sleep(1)
                                        except pyautogui.ImageNotFoundException:
                                            print("Like button image not found on the screen.")
                                        time.sleep(2)
                                        # Close comment
                                        try:
                                            close_button = driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//div[@class='x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81']//div[@class='x6s0dn4 x78zum5 xdt5ytf xl56j7k']")
                                            close_button.click()
                                        except NoSuchElementException:
                                            print("Close button not found. Skipping to the next comment.")
                                        ip=ip+1
                                        time.sleep(2)  
                                                        
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                            except TimeoutException:
                                print("Follow button not found or unable to click.")
                except TimeoutException:
                    print("Follow button not found")
        
        try:
            close_button = driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//div[@class='x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81']//div[@class='x6s0dn4 x78zum5 xdt5ytf xl56j7k']")
            close_button.click()
        except NoSuchElementException:
            print("Could not find the close button for the post modal.")
            time.sleep(1)
# SMTP START 
sender_email = "arehmannn999@gmail.com"
receiver_email = "hrosales015@gmail.com"
password = "jxcb xvop ajct eldo"
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Bot Instagram Instagram_Without_Follow Is Completed"
body = "Bot Instagram Instagram_Without_Follow Is Completed"
message.attach(MIMEText(body, "plain"))
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(sender_email, password)
server.sendmail(sender_email, receiver_email, message.as_string())
server.quit()
# SMTP END

# Close the browser
driver.quit()
