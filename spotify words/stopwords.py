with open('pt_stopwords.txt', 'r') as file:
    PORTUGUESE_STOP_WORDS = file.read().splitlines()
    file.close()

with open('en_stopwords.txt', 'r') as file:
    ENGLISH_STOP_WORDS = file.read().splitlines()
    file.close()
