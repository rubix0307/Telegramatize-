import openai

from config import OPENAI_API_KEY, model_engine


br = '\n'
data_txt_path = 'txt/'


post = open(f'{data_txt_path}post.txt', 'r', encoding='UTF-8').read()
prompt_text = open(f'{data_txt_path}prompt.txt', 'r', encoding='UTF-8').read()
prompt = f"{prompt_text}{br*2}Текст поста:{br}{post}"


openai.api_key = OPENAI_API_KEY
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=int(len(post) * 2),
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

answer = completion.choices[0].text.strip()
with open(f'{data_txt_path}answer.txt', 'w', encoding='UTF-8') as answer_file:
    answer_file.write(f'ㅤ{br}' + answer + f'{br}ㅤ')

print(answer)







