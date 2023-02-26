import openai

from config import OPENAI_API_KEY, model_engine, br






def get_unique_post(prompt):
    
    openai.api_key = OPENAI_API_KEY
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2000,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    answer = completion.choices[0].text.strip()
    with open(f'answer.txt', 'w', encoding='UTF-8') as answer_file:
        answer_file.write(f'ㅤ{br}' + answer + f'{br}ㅤ')
    
    return answer


