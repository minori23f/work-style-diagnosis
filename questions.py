"""Axis definitions and question data.

``agree_pole`` explicitly records which pole receives points when the user
agrees. This keeps scoring correct even when questions are reordered.
"""

AXES = {
    "RV": {
        "title": "判断の起点",
        "first_code": "R",
        "first_label": "現実重視",
        "second_code": "V",
        "second_label": "理想重視",
        "tie_question": "物事を考えるとき、より自分に近いのはどちらですか？",
        "tie_first": "確認できる事実や実現可能性を起点にする",
        "tie_second": "実現したい未来や理想の姿を起点にする",
    },
    "PF": {
        "title": "仕事の進め方",
        "first_code": "P",
        "first_label": "計画型",
        "second_code": "F",
        "second_label": "柔軟型",
        "tie_question": "仕事を進めるとき、より自分に近いのはどちらですか？",
        "tie_first": "先に道筋を決めてから進める",
        "tie_second": "進みながら状況に合わせて調整する",
    },
    "IC": {
        "title": "周囲との関わり方",
        "first_code": "I",
        "first_label": "個人型",
        "second_code": "C",
        "second_label": "協働型",
        "tie_question": "成果を生み出すとき、より自分に近いのはどちらですか？",
        "tie_first": "まず自分で深く考える",
        "tie_second": "まず周囲と意見を交わす",
    },
    "EN": {
        "title": "価値の生み出し方",
        "first_code": "E",
        "first_label": "既存改善型",
        "second_code": "N",
        "second_label": "新規開拓型",
        "tie_question": "価値を生み出すとき、より自分に近いのはどちらですか？",
        "tie_first": "現在あるものをより良くする",
        "tie_second": "これまでにないものを生み出す",
    },
}


QUESTIONS = [
    {"id": 1, "text": "新しい提案を評価するときは、実績やデータの確かさを重視する。", "axis": "RV", "agree_pole": "R"},
    {"id": 2, "text": "人と話しながら考えることで、新しいアイデアが浮かぶことが多い。", "axis": "IC", "agree_pole": "C"},
    {"id": 3, "text": "期限のある仕事では、中間目標を置いて段階的に進めたい。", "axis": "PF", "agree_pole": "P"},
    {"id": 4, "text": "行き詰まったときは、今のやり方を直すだけでなく、前提そのものを問い直したい。", "axis": "EN", "agree_pole": "N"},
    {"id": 5, "text": "途中で有効な情報が得られたら、当初の進め方をためらわず変更できる。", "axis": "PF", "agree_pole": "F"},
    {"id": 6, "text": "新しい仕事では、まず実現したい未来や生み出したい価値を思い描く。", "axis": "RV", "agree_pole": "V"},
    {"id": 7, "text": "現在の業務のどこに無駄があるかを見つけ、効率を高めることに面白さを感じる。", "axis": "EN", "agree_pole": "E"},
    {"id": 8, "text": "重要な判断では、人に相談する前に自分なりの考えを組み立てたい。", "axis": "IC", "agree_pole": "I"},
    {"id": 9, "text": "自分の考えは、早い段階で周囲に共有して意見をもらいたい。", "axis": "IC", "agree_pole": "C"},
    {"id": 10, "text": "経験のない方法でも、可能性があれば小さな実験から試してみたい。", "axis": "EN", "agree_pole": "N"},
    {"id": 11, "text": "案を考えるときは、使える時間・予算・人員などの条件を先に確認する。", "axis": "RV", "agree_pole": "R"},
    {"id": 12, "text": "仕事を始める前に、どの状態になれば完了かを明確にしておきたい。", "axis": "PF", "agree_pole": "P"},
    {"id": 13, "text": "うまくいった方法を整理し、誰でも再現できる形にすることが得意だ。", "axis": "EN", "agree_pole": "E"},
    {"id": 14, "text": "最初から手順を細かく決めるより、実際に動きながら自分に合う方法を見つけたい。", "axis": "PF", "agree_pole": "F"},
    {"id": 15, "text": "自分の担当については、進め方を任されると力を発揮しやすい。", "axis": "IC", "agree_pole": "I"},
    {"id": 16, "text": "十分な実績がなくても、将来性を感じる案なら検討を進めたい。", "axis": "RV", "agree_pole": "V"},
    {"id": 17, "text": "複数案のうち、実現しやすい案より、実現したときの価値が大きい案に惹かれる。", "axis": "RV", "agree_pole": "V"},
    {"id": 18, "text": "チームでは、互いの状況を共有しながら役割を調整すると成果を出しやすい。", "axis": "IC", "agree_pole": "C"},
    {"id": 19, "text": "複数の仕事を任されたら、先に優先順位と取り組む順番を決める。", "axis": "PF", "agree_pole": "P"},
    {"id": 20, "text": "すでに評価されている商品や仕組みを、さらに使いやすく磨く仕事に魅力を感じる。", "axis": "EN", "agree_pole": "E"},
    {"id": 21, "text": "完成形を考え抜いてから作るより、試作品への反応を見ながら修正したい。", "axis": "PF", "agree_pole": "F"},
    {"id": 22, "text": "既存の成功例を広げる仕事より、まだ確立されていない領域を切り開く仕事に惹かれる。", "axis": "EN", "agree_pole": "N"},
    {"id": 23, "text": "説明を受けるときは、具体例や数値があると内容を判断しやすい。", "axis": "RV", "agree_pole": "R"},
    {"id": 24, "text": "集中して質の高い成果を出すには、一人で中断されずに取り組む時間が必要だ。", "axis": "IC", "agree_pole": "I"},
]
