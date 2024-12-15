import json


f = open('voice_actor_list.json', 'r', encoding='UTF-8')

json_str = f.read()

# JSON文字列をPythonの辞書に変換
data = json.loads(json_str)

# "name"キーに含まれる名前をリストアップ
names = [actor["name"] for actor in data["voiceActors"]]

print("名前一覧:", names)

f.close()