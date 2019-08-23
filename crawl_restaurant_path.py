from selenium import webdriver

# Craw the link of the restaurants and save it to res_file.txt
res_file = open("res_file.txt", "w")
with open("listPage30.txt") as f:
    pages = f.read()
list_page = pages.split("\n")
# crawler data
driver = webdriver.Chrome('/Users/htran20/Downloads/chromedriver')
texts = []
scores = []
for name in list_page:
    path_link = str(name)
    driver.get(path_link)

    wrap = driver.find_element_by_id("wrap")
    res_list = wrap.find_element_by_class_name("spinner-container__373c0__N6Hff")
    main_container = res_list.find_element_by_class_name("mainContentContainer__373c0__32Mqa")
    res_list_1 = main_container.find_elements_by_class_name("lemon--li__373c0__1r9wz")
    for review in res_list_1:
        try:
            res_content_list = review.find_element_by_class_name("lemon--a__373c0__IEZFH")
            p = res_content_list.get_attribute("href")
            res_file.write(p + "\n")
        except:
            continue

res_file.close()
