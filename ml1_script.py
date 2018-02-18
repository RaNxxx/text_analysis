# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer
from nltk.probability import LidstoneProbDist
from nltkx import NgramModel

NEWLINE = "\n"

def open_corpus(corpus_path):
    """
    corpus_path(str) に指定されたファイルを開き、改行を消してひとつの文字列(str)にして返す
    """

    file_open = open(corpus_path,"r")

    file_lines = file_open.readlines()
    file_list = [element.replace("\n","") for element in file_lines]

    file_str = ""

    for element in file_list:
        file_str += element

    return file_str

#corpus_path = "corpus/dazai_melos.txt"
#print(open_corpus(corpus_path))


def tokenize(text):
    """
    日本語の text(str)を受け取って、単語ごとに切って、strのリストにして返す

    >>> tekenize("吾輩は猫である") -> ['吾輩', 'は', '猫', 'で', 'ある']
    """

    # ヒント
    # janomeの使い方は、http://mocobeta.github.io/janome/ 参照。
    # http://mocobeta.github.io/janome/api/janome.html#janome.tokenizer.Token も要チェック。

    t = Tokenizer()
    l = []

    for token in t.tokenize(text):
        l.append(token.surface)

    return l

#text = open_corpus(corpus_path)
#print(tokenize(text))


def train_model(corpus_path, n=2):
    """
    corpus_path(str)に指定されたファイルのテキストから言語モデルを学習し、n-gramで学習してモデルオブジェクトを返す
    """

    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)

    # ヒント
    # >>> model = NgramModel(n, words, estimator)
    # で、NgramModelオブジェクトが学習＆生成される。
    # words(list of str) は訓練データとなる文を、単語ごとに切ったもの。
    # estimatorは、Smoothing(平滑化)といって、1度も出ていない単語の出現確率を他の単語から推定する手法のための推定器で、ここではおまじないと考えて良い

    text = open_corpus(corpus_path)
    model = NgramModel(n, tokenize(text), estimator)

    return model

#n = 3
#print(train_model(corpus_path, n))


def per_word_cross_entropy(model, text):
    """
    model(NgramModel)とtext(str)をとり、modelにおけるtextのper-word クロスエントロピー(float)を返す
    """

    # ヒント
    # >>> model.entropy(words)
    # で words(list of str) で構成されるテキストの文全体のエントロピーが出せるので、これを文の単語数で割れば良い

    n = len(tokenize(text))
    m = model.entropy(tokenize(text))

    return m/n

#model = train_model(corpus_path, n)
#print(per_word_cross_entropy(model, "走れ、ひろきメロ！お前はやればできる子だ。信じとる！"))
#print(per_word_cross_entropy(model, "ひろきは、下賤の者で単純な男であった"))
#print(per_word_cross_entropy(model, "ランは天才である"))


def get_average_entropy(model, corpus_path, max_lines_to_load=-1):
    """
    corpus_path(str)に指定したファイルの冒頭 max_lines_to_load(int) 行の文の言語モデルオブジェクト model(NgramModel)
    で計ったクロスエントロピーの平均値を返す。
    例）max_lines_to_load = 30 の場合、冒頭30行の平均 per-word クロスエントロピーを返す
    """

    file_open = open(corpus_path,"r")

    file_lines = file_open.readlines()
    file_list = [element.replace("\n","") for element in file_lines]

    lines = file_list[:max_lines_to_load]
    total_entropy = 0

    for element in lines:
        if not len(element) == 0:
            total_entropy += per_word_cross_entropy(model,element)

    average_entropy = total_entropy / len(lines)
    return average_entropy

#max_lines_to_load = 30
#print(get_average_entropy(model, corpus_path, max_lines_to_load))



if __name__ == "__main__":
    n = 5
    max_lines_to_load = 100

    # 宮沢賢治 銀河鉄道の夜を学習して言語モデルをつくる
    model = train_model("./corpus/kenji_ginga.txt", n)

    print("宮沢賢治 / 注文の多い料理店: {0}".format(get_average_entropy(model, "./corpus/kenji_ryoriten.txt", max_lines_to_load)))
    print("宮沢賢治 / 風の又三郎: {0}".format(get_average_entropy(model, "./corpus/kenji_matasaburo.txt", max_lines_to_load)))
    print("宮沢賢治 / ツェねずみ: {0}".format(get_average_entropy(model, "./corpus/kenji_tsuenezumi.txt", max_lines_to_load)))
    print("太宰治 / 走れメロス: {0}".format(get_average_entropy(model, "./corpus/dazai_melos.txt", max_lines_to_load)))
    print("森鴎外 / あそび: {0}".format(get_average_entropy(model, "./corpus/ogai_asobi.txt", max_lines_to_load)))
    print("夏目漱石 / こころ: {0}".format(get_average_entropy(model, "./corpus/soseki_kokoro.txt", max_lines_to_load)))
    print("夏目漱石 / 道草: {0}".format(get_average_entropy(model, "./corpus/soseki_michikusa.txt", max_lines_to_load)))
