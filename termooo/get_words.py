from selenium import webdriver

driver = webdriver.Chrome(executable_path=r"C:\Users\Lucas Petersen\Downloads\Drivers\chromedriver.exe")
url = 'https://www.dicio.com.br/palavras-com-cinco-letras/'
x_path = '/html/body/div[2]/div[3]/div[2]/div[1]/p[2]'
driver.get(url)
element = driver.find_element_by_xpath(x_path)
file = open('words.txt', 'w', encoding='utf-8')
file.write(element.text)
file.close()
driver.close()
