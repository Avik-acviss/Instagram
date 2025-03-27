import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.instagram.com/")

    user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@aria-label, "Phone number")]')))
    user.send_keys('testscraper552@gmail.com')

    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@aria-label, "Password")]')))
    password.send_keys('123456789@a')

    log_in = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, " _acan _acap _acas _aj1- _ap30")]')))
    log_in.click()

    not_now = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div')))
    not_now.click()

    search_keyword = input("Enter the keyword to search: ")

    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@aria-label, "Search input")]')))
    search_box.send_keys(search_keyword)
    time.sleep(2)

    first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "x1lliihq")]')))
    profile_link = first_result.get_attribute("href")
    first_result.click()

    try:
        post_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "x5n08af")]/span[contains(@class, "xdj266r")]'))).text
    except:
        post_count = "NA"

    try:
        followers_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//a[contains(@href, "followers")]/span)[1]'))).text
    except:
        followers_count = "NA"

    try:
        following_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//a[contains(@href, "following")]/span)[1]'))).text
    except:
        following_count = "NA"

    try:
        bio = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_ap3a _aaco _aacu _aacy _aad6 _aade')]"))).text
    except:
        bio = "NA"

    try:
        external_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'x6ikm8r x10wlt62')]/a")
        external_links = [link.get_attribute("href") for link in external_links]
    except:
        external_links = []

    print(f"Profile Data: {profile_link}, {post_count} posts, {followers_count} followers, {following_count} following, Bio: {bio}, Links: {external_links}")

    try:
        reels_section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/reels/")]')))
        reels_section.click()
    except:
        print("No reels found.")
        driver.quit()
        exit()

    video_link = None
    while not video_link:
        video_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/reel/")]')))

        for video in video_elements:
            video_url = video.get_attribute("href")
            if "/reel/" in video_url:
                video_link = video_url
                break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    if not video_link:
        print("No videos found.")
        driver.quit()
        exit()

    driver.get(video_link)
    time.sleep(3)

    try:
        likes_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "likes")]')))
        likes_text = likes_element.text.split()[0]
    except:
        likes_text = "NA"

    try:
        first_comment_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "_ap3a")]')))
        first_comment = first_comment_element.text
    except:
        first_comment = "NA"

    try:
        date_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//time[contains(@class, "x1p4m5qa")]')))
        reel_date = date_element.get_attribute("datetime")
    except:
        reel_date = "NA"

    print(f"Reel Data: {video_link}, Likes: {likes_text}, First Comment: {first_comment}, Date: {reel_date}")

    data = {
        search_keyword: {
            "profile_link": profile_link,
            "followers": followers_count,
            "following": following_count,
            "posts": post_count,
            "bio": bio,
            "external_links": external_links,
            "reels": {
                "link1": {
                    "url": video_link,
                    "likes": likes_text,
                    "first_comment": first_comment,
                    "date": reel_date
                }
            }
        }
    }

    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print("Scraping complete. Data saved in JSON format.")

except Exception as e:
    print("Error occurred:", str(e))

input("Press Enter to exit...")