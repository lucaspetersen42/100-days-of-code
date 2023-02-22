from selenium import webdriver

driver = webdriver.Chrome(executable_path=r"C:\Users\Lucas Petersen\Downloads\Drivers\chromedriver.exe")
URL = 'https://www.dicio.com.br/palavras-com-cinco-letras/'
x_path = '//*[@id="content"]/div[1]/p[2]'
driver.get(URL)
element = driver.find_element_by_xpath(x_path)
file = open('words.txt', 'w', encoding='utf-8')
file.write(element.text)
file.close()
driver.close()
