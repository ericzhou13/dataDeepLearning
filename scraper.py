import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd


def scrape_zillow():
    # Start the undetected Chrome driver
    options = uc.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    
    
    # Navigate to Zillow
    driver.get("https://www.zillow.com/nj/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-81.03871508984373%2C%22east%22%3A-68.36049243359373%2C%22south%22%3A36.27167058638969%2C%22north%22%3A43.429726895461854%7D%2C%22mapZoom%22%3A7%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A40%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22price%22%3A%7B%22min%22%3A600000%2C%22max%22%3A650000%7D%2C%22mp%22%3A%7B%22min%22%3A2979%2C%22max%22%3A3227%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22usersSearchTerm%22%3A%22NJ%22%7D")
    # time.sleep(60)
    
    
    actions = ActionChains(driver)
    actions.move_by_offset(1000, 300).context_click().perform()
    actions.move_by_offset(-1000, 0).perform()
    count = 5
    price_count = 2000
    #how many pages we will scrape
    #500
    for i in range(13):
        df = pd.DataFrame(columns = [i for i in range(60)])
        # ul_elements = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/ul")
        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/ul"))
        )
        li_elements = ul_element.find_elements(By.XPATH, "./li")
        #for element in li_elements:
        #number of tiles we will click
        for j in range(len(li_elements)):
            cur_url = driver.current_url
            imgs = []
            try:
                imgs = WebDriverWait(li_elements[j], 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, ".//img[starts-with(@src, 'https://photos.zillowstatic.com/')]"))
                )
            except TimeoutException:
                imgs = []           
            for k in range(len(imgs)):
                imgs[k] = imgs[k].get_attribute('src')
            imgs = [s for s in imgs if "zillow_web" not in s]
            if len(imgs) > 0:
                actions.move_to_element(li_elements[j]).click().perform()
                try:
                    #find necessary elements
                    show_me = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-testid='facts-and-features-wrapper-footer']")))[0]
                    show_me = show_me.find_element(By.TAG_NAME, "button").click()

                    header = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-testid='fs-chip-container'] | //*[@data-testid='home-info']")))[0]

                    content = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-testid='fact-category']")))
                    content = driver.find_elements(By.XPATH, "//*[@data-testid='fact-category']")

                    #add all data to a dict
                    data = {}
                    idx = 0
                    img_str = ""
                    for img in imgs:
                        img_str += img + "\n"
                    data[idx] = img_str
                    idx += 1

                    header = header.text.split("\n")
                    header = header[0:2]
                    for c in header:
                        data[idx] = c
                        idx += 1
                
                    for el in content:
                        text = el.text.split('\n')
                        text = [s.lower() for s in text]
                        data[idx] = "||".join(text)
                        
                        idx += 1
                    
                    #convert and add dict to df
                    data[59] = cur_url
                    data[58] = driver.current_url
                    row = pd.DataFrame(data, index = [0])
                    df = pd.concat([df, row], ignore_index=False)

                    print("Current Page", count)
                    # print(df.head())
                except TimeoutException:
                    print(TimeoutException)
                    continue
                actions.move_by_offset(-li_elements[j].location['x'], 0).click().perform()
                time.sleep(1)
        df.to_csv(f"zillow_data_{price_count}k_{count}.csv", sep="~", index=True)
        #         
        next_page = driver.find_element(By.XPATH, "//*[@id='grid-search-results']/div[2]/nav/ul/li[10]/a")
        next_page.click()
        time.sleep(2)
        count += 1


    return df  

# Run the scraper
if __name__ == "__main__":
    search_query = "New Jersey"  # Example query
    num_pages_to_scrape = 20

    data = scrape_zillow()
    print(data)

    # Save to CSV
    # data.to_csv(f"zillow_data{1}.csv", sep="~", index=False)
    # print("Data saved to zillow_data.csv")
    
