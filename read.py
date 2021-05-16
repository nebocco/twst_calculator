import csv
import json

with open('./twst.csv') as f:
    l = list(csv.reader(f))

with open('./magic.csv') as f:
    g = list(csv.reader(f))

chars = [
    "リドル",
    "エース",
    "デュース",
    "ケイト",
    "トレイ",
    "レオナ",
    "ジャック",
    "ラギー",
    "アズール",
    "ジェイド",
    "フロイド",
    "カリム",
    "ジャミル",
    "ヴィル",
    "エペル",
    "ルーク",
    "イデア",
    "オルト",
    "マレウス",
    "シルバー",
    "セベク",
    "リリア"
]

costumes = [
    "制服",
    "アーキタイプ・ギア",
    "運動着",
    "アスレチック・ギア",
    "実験着",
    "バースト・ギア",
    "式典服",
    "プレジション・ギア",
    "寮服",
    "おめかしバースデー",
    "ビーンズ・カモ",
    "ガラ・クチュール",
    "なりきり花婿",
    "星送りの衣",
    "スターゲイズ・ギア"
]

chardict = {x:i for i, x in enumerate(chars)}
cosdict = {x:i for i, x in enumerate(costumes)}
attr = ['R', 'G', 'B']
kanji = ['火', '木', '水', '無']

with open('./magic_detil.csv') as f:
    mad = list(csv.reader(f))

magics = []
for row in mad[1:]:
    magics.append({
        "name": row[0],
        "attr": kanji.index(row[1]),
        "text": row[2],
        "power": int(row[3] != '弱'),
        "combo": int(row[4])
    })

magic_names = [x["name"] for x in magics]

res = list()
for i, (row, r2) in enumerate(zip(l[1:], g[2:])):
    if row[1] == '':
        break
    assert row[1] == r2[0] and row[2] == r2[1]
    res.append({
        "id": i,
        "name": chardict[row[1]],
        "costume": cosdict[row[2]],
        "rarity": row[3],
        "type": row[4],
        "attr": (attr.index(row[5]) + 2) % 3,
        "magics": [
            [
                [magic_names.index(r2[2]), r2[3]],
                [magic_names.index(r2[4]), r2[5]],
                [magic_names.index(r2[6]), r2[7]]
            ],
            [
                [magic_names.index(r2[8]), r2[9]],
                [magic_names.index(r2[10]), r2[11]],
                [magic_names.index(r2[12]), r2[13]]
            ]
        ],
        "buddies": [[chardict[x], i - (i + 2) // 3] for i, x in enumerate(row[8:14]) if x != '']
    })

magic_text = sum((r2[3:14:2] for r2 in g[2:]), [])
print(*sorted(set(magic_text)), sep='\n')

with open('./static/twst.json', 'w') as f:
    f.write(json.dumps({
        "characters": [{"id": i, "name": x} for i, x in enumerate(chars)],
        "costumes": [{"id": i, "name": x} for i, x in enumerate(costumes)],
        "cards": res, 
        "magics": magics
    }))