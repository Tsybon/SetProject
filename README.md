# SetProject

Головна суть скриптів - перевіряти зміни сайту для пошуку потенційних дефейсі. Також у скрипті "check_subdomains.py" є алгоритм пошуку піддоменів сайту.
Дефейс сайту перевіряється "вагою" сайту та часом відповіддю серверу. Цю ідею можна доробити використовуючи ML для аналізу аномалій.

Для роботи скриптів необхідно підплючити GoolgeAPI та надати доступ до Google Spreadsheet. Після чого створити наступні сторінки у таблиці:

common_domains - список доменів, які необхідно перевірити
domains_to_check - результати пошуку піддоменів із common_domains сторінки
checkdeface - сторінка де буде зберігатись інформація щодо стану сайту.

Приклади:

<img width="730" alt="checkdeface" src="https://github.com/user-attachments/assets/fe69654e-43d4-4dbf-9c2b-976f33512d5a">
<img width="632" alt="domains_to_check" src="https://github.com/user-attachments/assets/8232c87a-6382-47c3-8701-626db7bcf3bb">
<img width="630" alt="common_domains" src="https://github.com/user-attachments/assets/07c0a4f6-7c83-4da0-bd27-1d06b7051a1d">
