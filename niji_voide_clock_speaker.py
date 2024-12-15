# coding: UTF-8

# にじボイスの声優が現在時刻を読み上げる
# API Key を環境変数に登録して実行

import requests, json, random, os
from pydub import AudioSegment
from pydub.playback import play

voice_actor_list = ['水戸 明日菜', '漆夜 蓮', '冬月 初音', '陽斗・エイデン・グリーンウッド', '苔村 まりも', '野本 藍一郎', 'ぽの', 'ラピス', '朝霧 瑞樹', '三浦 隼人', '遠野 澄花', 'セドリック・E・ウィットモア', '若草 ひかり', '羽依', 'キア', '高槻 リコ', '深海 結涼', 'タルト', '神崎 怜司', '月城 美蘭', '久世 凛', '灯真', 'ヴィヴィアン', '桜庭 恭平', 'イルミル', '篠崎 優也', 'ノエラ', 'ヴィクター・D・アシュフォード', 'エヴァニア・ノクターン', 'ロザリア・ガーネット', '李 昊天', '蘭華', 'トリッカ', '霧島 律', '春玲', '白熊 愛鈴', '星川 青葉', 'シャルロッテ', '高嶺 陽菜', '森野 颯太', '若宮 紬', '黛 セナ', '高坂 茉莉', '淵', '深景', 'レヴィエル', '久咲 悠仁', 'ティ二ー', '白天', '黒崎 里穂', 'イリヤ・カレント', 'リ ュウセイ', '白石 玲奈', '如月 要', 'ラファエル・グリモワール', '春野 奏汰', '篝', '小夜', '天野 柩', '森宮 千乃', '森下 和花', 'フィーナ・ルナリエ', '月白 織', '燻 秋雄', '春日  ひまり', '篠ノ井 志乃', '凛堂 葵', '橘 志穂', 'ミミ', 'ベン・カーター', 'エリオル', '玄蔵', '桜庭 詩織', 'ルチカ', '水瀬 玲奈', '橘 すずか', 'ジャナーフ', 'シュネー・レオパーダ', '月島 千遥', '有馬 慎一郎', '新堂 慶介', 'オリバー・ジェームズ', 'ハオラン', '小鳥遊 緑音', '碧海 凪', 'マーピン・ティンカー', '燐灯', '金城 夏海', 'エリカ・ヴァルトハイム', '照月院 輝臣', 'ミレア', 'リリィ・アルト', '高宮 涼香', '神薙 瞳', '深沢 美咲', '椎名 結衣', '跳々', 'アナスタシア', '宝泉寺 ミリア', '春乃 セリーヌ 白鳥']
    
def lookup_actor_id(target_name):
    f = open('voice_actor_list.json', 'r', encoding='UTF-8')
    json_str = f.read()
    # JSON文字列をPythonの辞書に変換
    data = json.loads(json_str)
    # 指定されたキーに対応するIDを取得
    actor_id = '1fc717fe-ebf9-402b-9d8c-c59cda93d5dc' # デフォルトは '水戸 明日菜'
    if target_name == 'ランダム':
        target_name = random.choice(voice_actor_list)

    for actor in data["voiceActors"]:
        if actor["name"] == target_name:
            actor_id = actor["id"]
            break
    print("話者:" + target_name + ", ID:" + actor_id)
    return actor_id

def generate_voice(actor, tts_content, filename = "downloaded_audio.mp3", speed = 1.0):
    id = lookup_actor_id(actor)
    url = "https://api.nijivoice.com/api/platform/v1/voice-actors/" + id + "/generate-voice"

    payload = {
        "format": "mp3",
        "script": tts_content,
        "speed": str(speed)
    }
    headers = {
        "accept": "application/json",
        "x-api-key": os.environ['NIJIVOICE_API_KEY'],
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.text)
    # JSON文字列をPythonの辞書に変換
    data = json.loads(response.text)

    # audioFileDownloadUrlキーの値を取り出す
    audio_file_download_url = data["generatedVoice"]["audioFileDownloadUrl"]

    # ファイルをダウンロードして保存
    response = requests.get(audio_file_download_url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"MP3ファイルを '{filename}' に保存しました。")
    else:
        print(f"ファイルのダウンロードに失敗しました。ステータスコード: {response.status_code}")

    return filename

def test_speak_current_time():
    from datetime import datetime
    # 現在の日付と時間を取得
    now = datetime.now()

    # フォーマットを指定して出力
    formatted_datetime = now.strftime("%Y年%m月%d日%H時%M分だよ")
    print(formatted_datetime)
    sentense = formatted_datetime
    #sentense = "これらのフレーズを使えば、文章がより洗練され、IELTS Task 1のフォーマルな手紙のトーンに適したものになります！ぜひ練習に取り入れてみてください"
    tx_mp3_filename = generate_voice('ランダム', sentense, formatted_datetime + ".mp3")
    # MP3ファイルを読み込んで再生
    sound = AudioSegment.from_mp3(tx_mp3_filename)
    play(sound)

test_speak_current_time()