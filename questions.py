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
    {"id": 3, "text": "仕事を始める前に、手順や期限を整理しておきたい。", "axis": "PF", "agree_pole": "P"},
    {"id": 4, "text": "問題が起きたときは、現在の方法を修正するより、前提から見直したい。", "axis": "EN", "agree_pole": "N"},
    {"id": 5, "text": "詳細な計画を固めるより、まず着手して状況に合わせて調整したい。", "axis": "PF", "agree_pole": "F"},
    {"id": 6, "text": "仕事に取り組むときは、現状の制約よりも実現したい姿を起点に考える。", "axis": "RV", "agree_pole": "V"},
    {"id": 7, "text": "現在の仕組みにある問題を特定し、一つずつ改善することが得意だ。", "axis": "EN", "agree_pole": "E"},
    {"id": 8, "text": "難しい問題に直面したときは、まず一人でじっくり考えたい。", "axis": "IC", "agree_pole": "I"},
    {"id": 9, "text": "自分の考えは、早い段階で周囲に共有して意見をもらいたい。", "axis": "IC", "agree_pole": "C"},
    {"id": 10, "text": "未経験の方法でも、可能性を感じれば小さく試してみたい。", "axis": "EN", "agree_pole": "N"},
    {"id": 11, "text": "意見を決める前に、確認できる事実を十分に集めたい。", "axis": "RV", "agree_pole": "R"},
    {"id": 12, "text": "複数の仕事があるときは、先に優先順位と順番を決めたい。", "axis": "PF", "agree_pole": "P"},
    {"id": 13, "text": "実績のある方法を工夫し、さらに完成度を高めることに魅力を感じる。", "axis": "EN", "agree_pole": "E"},
    {"id": 14, "text": "予定外の変化が起きたときは、当初の計画にこだわらず進め方を変えたい。", "axis": "PF", "agree_pole": "F"},
    {"id": 15, "text": "自分の担当については、進め方を任されると力を発揮しやすい。", "axis": "IC", "agree_pole": "I"},
    {"id": 16, "text": "十分な根拠がそろっていなくても、将来性を感じれば検討を進めたい。", "axis": "RV", "agree_pole": "V"},
    {"id": 17, "text": "現在の課題を考えるときは、まず理想的な状態を思い描く。", "axis": "RV", "agree_pole": "V"},
    {"id": 18, "text": "チームで仕事をするときは、途中経過をこまめに共有したい。", "axis": "IC", "agree_pole": "C"},
    {"id": 19, "text": "期限のある仕事では、中間目標を設定して段階的に進めたい。", "axis": "PF", "agree_pole": "P"},
    {"id": 20, "text": "現在あるものの品質や効率を高める仕事に魅力を感じる。", "axis": "EN", "agree_pole": "E"},
    {"id": 21, "text": "最初に方法を細かく決めず、進めながら自分に合うやり方を探したい。", "axis": "PF", "agree_pole": "F"},
    {"id": 22, "text": "既存のものを改善するより、新しい領域を切り開く仕事に魅力を感じる。", "axis": "EN", "agree_pole": "N"},
    {"id": 23, "text": "抽象的な構想よりも、具体的ですぐに実行できる案に納得しやすい。", "axis": "RV", "agree_pole": "R"},
    {"id": 24, "text": "分からないことがあったときは、まず自分で調べて考えを整理したい。", "axis": "IC", "agree_pole": "I"},
    {"id": 25, "text": "チームで目標や成果を共有できると、仕事への意欲が高まる。", "axis": "IC", "agree_pole": "C"},
    {"id": 26, "text": "複数の案を比べるときは、実現しやすさよりも、目指す価値の大きさを重視する。", "axis": "RV", "agree_pole": "V"},
    {"id": 27, "text": "ある程度うまくいっている仕事でも、さらに精度を高める余地を探したい。", "axis": "EN", "agree_pole": "E"},
    {"id": 28, "text": "会議では、あらかじめ決めた議題と時間配分に沿って進めたい。", "axis": "PF", "agree_pole": "P"},
    {"id": 29, "text": "限られた時間や予算は、既存の取り組みを強化するより、新しい可能性を試すために使いたい。", "axis": "EN", "agree_pole": "N"},
    {"id": 30, "text": "完成形を考えてから作るより、試作品を作って修正を重ねたい。", "axis": "PF", "agree_pole": "F"},
    {"id": 31, "text": "集中して成果を出すには、周囲に中断されず一人で取り組む時間が必要だ。", "axis": "IC", "agree_pole": "I"},
    {"id": 32, "text": "説明を受けるときは、具体例や数値が示されていると納得しやすい。", "axis": "RV", "agree_pole": "R"},
]
