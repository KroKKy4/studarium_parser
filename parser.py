import requests
from bs4 import BeautifulSoup
import pandas as pd

# Список для хранения всех заданий
all_tasks_text = []

for theme_counter in range(1, 28):
    url = f'https://studarium.ru/working/11/{theme_counter}/page-1'
    domain_name = 'https://studarium.ru'

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        pagination = soup.find('ul', class_='pagination')  # Найдите класс или ID, который содержит пагинацию
        page_count = 2  # Начальное количество страниц

        if pagination:
            # Здесь можно извлечь количество страниц путем анализа текста или с помощью ссылок на страницы
            pages = pagination.find_all('a')
            if pages:
                page_count = max(int(page.get_text()) for page in pages if page.get_text().isdigit())

        for page_counter in range(1, page_count + 1):
            url = f'https://studarium.ru/working/11/{theme_counter}/page-{page_counter}'

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            tasks = soup.find_all('div', class_='container conta gap_bottom')

            for task in tasks:
                number_span = task.find('span')
                number = number_span.get_text().strip().rstrip('.') if number_span else 'Неизвестно'

                spans = task.find_all('span')

                # Список для хранения текста задания для конкретного номера
                current_task_text_parts = []

                # Добавляем текст из span'ов
                for span in spans:
                    current_task_text_parts.append(span.get_text().strip())

                    # Находим изображение, если оно есть
                job_img = task.find('div', class_='job_img_warp_c mtb')
                img_link = None  # Изначально предположим, что изображение отсутствует

                if job_img:
                    img_tag = job_img.find('img')
                    if img_tag and img_tag.get('src'):
                        img_link = img_tag['src']
                    else:
                        print('У задания нет изображения')

                        # Сохраняем тексты заданий
                full_text = ' '.join(current_task_text_parts).strip()

                # Если изображение было найдено, формируем полную ссылку
                full_image_link = domain_name + img_link if img_link else 'Изображение отсутствует'

                # Получаем ответ
                answer = task.find_next('div', class_='help')
                if answer:
                    answer_text = answer.get_text(strip=True)
                    if "Верный ответ:" in answer_text:
                        result = answer_text.split("Верный ответ:")[1].strip().split()[0]
                        if "P.S." in result:
                            result = result.split("P.S.")[0].strip()
                    else:
                        result = "Ответ не найден"
                else:
                    result = "Ответ не найден"

                    # Добавляем данные о задании в общий список
                all_tasks_text.append({
                    "Номер": number,
                    "Текст задания": full_text,
                    "Ссылка на изображение": full_image_link,
                    "Ответ": result
                })
        all_tasks_text.append({})

    except Exception as e:
        print(f'Произошла ошибка при обработке темы {theme_counter}: {e}')

    # Сохраняем все данные в Excel в конце
df = pd.DataFrame(all_tasks_text)
output_file = 'tasks.xlsx'
df.to_excel(output_file, index=False)
print(f'Данные успешно записаны в {output_file}')
