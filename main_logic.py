import requests
import json

# url = 'https://www.dota2.com/datafeed/patchnoteslist?language=english'
# response = requests.get(url)
# if response.status_code == 200:
#     data = response.json()
# else:
#     print(f'Ошибка: {response.status_code}')

# latest_patch = data['patches'][-3]
# # for time in data['patches']:
# #     print(time['patch_timestamp'], time['patch_number'])
# version = latest_patch['patch_number']

# url2 = f"https://www.dota2.com/datafeed/patchnotes?version={version}&language=english"
# response2 = requests.get(url2)
# patch_data = response2.json()
# # print(patch_data.keys())
# hero = patch_data['heroes']
# for i in hero:
#     if len(i.get('hero_notes', []))>2:
#         print(f'Герой id{i['hero_id']}, изменений {len(i['hero_notes'])}')
#         for note in i['hero_notes']:
#             indent = '  ' * note['indent_level']
#             print(f"{indent} - {note['note']}")
#         break
import requests

url = 'https://www.dota2.com/datafeed/patchnoteslist?language=russian'
# data = requests.get(url).json()

# latest_patch = data['patches']
# version = latest_patch['patch_number']


url = 'https://www.dota2.com/datafeed/herolist?language=english'
data = requests.get(url).json()
heroes = data['result']['data']['heroes']

with open('ability_ids.json', 'r', encoding='utf-8') as file:
    data_ability = json.load(file)

with open('abilities.json', 'r', encoding='utf-8') as file:
    data_name_abilities = json.load(file)


# url2 = f"https://www.dota2.com/datafeed/patchnotes?version={version}&language=russian"
# response2 = requests.get(url2)
# patch_data = response2.json()
# # print(patch_data.keys())
# hero = patch_data['heroes']

def get_patched(version: str):
    url2 = f"https://www.dota2.com/datafeed/patchnotes?version={version}&language=russian"
    response2 = requests.get(url2)
    patch_data = response2.json()
    hero = patch_data['heroes']
    return hero


def chanched_hero(id: int, heroes: list) -> list:
    for i in heroes:
        if i['hero_id'] == id:
            return i.get('hero_notes', [])
    return []


def chanched_talents(id: int, heroes: list) -> list:
    for i in heroes:
        if i['hero_id'] == id:
            return i.get('talent_notes', [])
    return []


def chanched_abilki(id: int, heroes: list) -> list:
    for i in heroes:
        if i['hero_id'] == id:
            return i.get('abilities', [])
    return []


def find_hero(hero_name):
    for hero in heroes:
        if hero['name_loc'].lower() == hero_name.lower():
            return hero['id']


def format_notes(nots):
    lines = []
    if not nots:
        return '  (изменений нет)'
    for note in nots:
        indent = '  ' * note['indent_level']
        lines.append(f"{indent}- {note['note']} ")
    return f'\n'.join(lines)


def name_ability(abilities):
    tech_name = data_ability.get(str(abilities))
    if not tech_name:
        return 'Неизвестная способность'
    ability_inf = data_name_abilities.get(tech_name)
    if ability_inf is None:
        return 'Неизвестная способность'
    return ability_inf.get('dname', 'Без названия')


def format_abilki(abilities):
    lines = []
    if not abilities:
        return '  (изменений нет)'
    for abilka in abilities:
        lines.append(f"Способность - {name_ability(abilka['ability_id'])}")
        lines.append(format_notes(abilka['ability_notes']))
    return '\n'.join(lines)


def changes_hero(name: str, version: str):
    if not (find_hero(name)):
        return 'Герой не найден'

    heroes = get_patched(version)
    names = find_hero(name)

    part = []
    part.append(f'ПАТЧ - {version}')
    part.append(f'Герой - {name}, {names}')

    part.append('Общие изменения:')
    part.append(format_notes(chanched_hero(names, heroes)))

    part.append('Изменения талантов:')
    part.append(format_notes(chanched_talents(names, heroes)))

    part.append('Изменения способностей:')
    part.append(format_abilki(chanched_abilki(names, heroes)))

    return f'\n'.join(part)


name = input()
version = input()