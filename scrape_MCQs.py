import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.learninsta.com/[URL]...'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
page_body = soup.body
mcqs = page_body.select('p')

items = []
flag = 1

for i in mcqs[4:-3]:
    if str(i.find('span')) != 'None':
        break

    if flag==1:
        questions = i.text.split('\n')
        question_no = questions[0].split(' ', 1)[1].strip('.')
        question = questions[1]
        #print([x[0].strip() for x in questions[2][0]])
        #print('\nq1', questions[2])
        
        if questions[2][0]!='(':
            question = question + ' ' + questions[2]
            options = [x[4:].strip() for x in questions[3:]]
        else:
            options = [x[4:].strip() for x in questions[2:]]

        #print('\nq', question)
        info = {
            "question_no": question_no.strip(),
            "question": question.strip(),
            "options": options
        }
    elif flag==0:
        answer = i.get_text().strip('')[12:]
        info["answer"] = answer.split("\n",1)[0].strip('.')
        items.append(info)
        #print(info)
    #print('\n')
    flag = 1-flag

        

df = pd.DataFrame(items)

len_options = []
for i in range(len(df['options'].to_list())):
    len_options.append(len(df['options'].to_list()[i]))

print(max(len_options))

if max(len_options)==4:
    option_list = ['option1', 'option2', 'option3', 'option4']
elif max(len_options)==3:
    option_list = ['option1', 'option2', 'option3']
elif max(len_options)==5:
    option_list = ['option1', 'option2', 'option3', 'option4', 'option5']

option_df = pd.DataFrame(df['options'].to_list(), columns = option_list)

answers = df['answer']

df = pd.concat([df.drop(['options', 'answer'], axis=1), option_df, answers], axis=1)

df.to_csv('sheet2.csv')
