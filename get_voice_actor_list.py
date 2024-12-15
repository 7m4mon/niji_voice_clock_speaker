# にじボイスの声優リストを取得する
# API Key を環境変数に登録して実行

import requests, os, json

url = "https://api.nijivoice.com/api/platform/v1/voice-actors"

headers = {
    "accept": "application/json",
    "x-api-key": os.environ['NIJIVOICE_API_KEY']
}

response = requests.get(url, headers=headers)

print(response.text)

data = json.loads(response.text)

# ファイルに保存
with open("voice_actor_list.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(data, indent=4, ensure_ascii=False))
