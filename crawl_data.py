from selenium import webdriver
import time

# Save the crawling reviews to cmt_file.txt and rating score to score_file.txt
cmt_file = open("cmt_file.txt", "w")
star_file = open("score_file.txt", "w")

# Get link to restaurants from txt file content link of the restaurants
with open("res_file_full.txt") as f:
    paths = f.read()
list_path = paths.split("\n")
# crawler data
driver = webdriver.Chrome('/Users/htran20/Downloads/chromedriver')
texts = []
scores = []
count_success = 1
for path in list_path:
    path_link = str(path)
    try:
        driver.get(path_link)
        print(count_success)
        count_success += 1
    except:
        continue
    count = 0
    # Page number
    while count < 5:
        count += 1
        try:
            review_pager = driver.find_element_by_class_name("review-pager")
            review_list = driver.find_element_by_class_name("review-list")
            review_content_list = review_list.find_elements_by_class_name("review-content")
            for review in review_content_list:
                star_element = review.find_element_by_class_name("i-stars")
                p = review.find_element_by_tag_name("p").text.replace('\n', ' ')
                star = star_element.get_attribute("title")
                cmt_file.write(p + "\n")
                star_file.write(star[0] + "\n")

            load_more = review_pager.find_element_by_class_name('next')
            load_more.click()
            # Sleep 2 second in waiting for the page to load
            time.sleep(2)
        except:
            continue


star_file.close()
cmt_file.close()
