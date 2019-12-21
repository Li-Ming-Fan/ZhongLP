from nltk.util import bigrams, trigrams
from nltk.text import Text
from nltk import FreqDist
from functools import reduce
from bidict import bidict
import numpy as np

corpus = [
    '<begin> 小鸟 声音 不大 ， 却 句 句 在理 ， 全场 都 静静 恭听。 <end>',
    '<begin> 他 说 ： “ 神 是否 创造 世界 ，即 神 对 世界 的 关系 如何 ，这个 问题 其实 就是 关于 精神 对 感性 一般 或 抽象 对 实在、类 对 个体 的 关系 如何 的 问题 ；这个 问题 是 属于 人类 认识 和 哲学 上 最 重要 又 最 困难 的 问题 之一 ， 整个 哲学史 其实 只在 这个 问题 周围 绕 圈子 ， 古代 哲学 中 斯多葛派 和 伊壁鸠鲁派 间 、 柏拉图派 和 亚里士多德派 间 、 怀疑派 和 独断派 间 的 争论 ， 中古哲学 中 唯名论者 和 实在论者 间 的 争论 ， 以及 近代 哲学 中 唯心主义者 和 实在论者 或 经验主义者 间 的 争论 ， 归根结底 都是 关于 这个 问题 。 <end>”',
    '<begin> 讨论 法 的 本位 问题 ， 应该 局限 于 实在 法效 用 的 实现 借助 于 何种 规范 手段 的 范围 内 ， 它 主要 应 讨论 " 法 是 什么 " 的 问题 ， 而 不是 " 法 应当 是 什么 " 的 问题 。 <end>',
    '<begin> 现在 ， 你 已是 全班 第一名 了 ， 我们 都要 向 你 学习 ， 我们 还会 继续 帮助 你 。 <end>',
    '<begin> 他们 的 罪恶 行径 也 从 反面 教育 我们 ， 革命 的 政治工作 对于 我们 党 的 各项 工作 ， 对于 我们 军队 和 人民 来说 ， 确实 是 不可以 须臾 离开 的 生命线 。 <end>',
    '<begin> 从 研究系 办 的 刊物 来看 ， 确实 登载 过 大量 的 讨论 社会主义 的 文章 ， 似乎 亦 拥护 社会主义 ， 但 实际上 这 只是 假象 。 <end>',
    '<begin> 他 那些 舞台 下 、 剧场 外 的 事 的确 是 鲜为人知 的 。 <end>',
    # '<begin> 他 说 的 确实 在理 <end>'
]

# 单字切分，暂时没用到
def atomic_split(param1, param2):
    if isinstance(param1, list):
        return param1 + list(param2.replace(' ', ''))
    else:
        return atomic_split(atomic_split([], param1), param2)


atomics = reduce(atomic_split, corpus)

#对语料的切分
def word_split(param1, param2):
    if isinstance(param1, list):
        return param1 + param2.split()
    else:
        return word_split(word_split([], param1), param2)


words = reduce(word_split, corpus)

#计算词频,索引
fd = FreqDist(words)

index = bidict()
pos = 0
for k, c in fd.items():
    index[k] = pos
    pos = pos + 1

#=====利用nltk的biggrams函数，建立gram矩阵==========================
grams = list(bigrams(words))

gc = np.zeros((fd.B(), fd.B()), dtype=np.int32)

#统计gram次数
for p1, p2 in grams:
    gc[index[p1], index[p2]] += 1

#统计gram概率
gp = np.zeros((fd.B(), fd.B()))


#平滑系数
ratio = 0.9

for row in range(0, fd.B()):
    for col in range(0, fd.B()):
        gp[row, col] = ratio * (gc[row, col] / fd[index.inv[row]]) + (
            1 - ratio) * (fd[index.inv[col]] / len(words))

#======================模型训练完成=================================

#=============求最短路径(非N-最短路径,算法和原方法不同，一个是因为对原算法有疑问，另一个为了快速完成DEMO)==================
def split(s, pos=0):
    if len(s) <= pos: return [{'key': '<end>'}]
    result = []
    for k in fd.keys():
        end = pos + len(k)
        if len(k) > 1 and end <= len(s) and k == s[pos:end]:

            result.append({'key': k, 'childs': split(s, end)})

    result.append({'key': s[pos:pos + 1], 'childs': split(s, pos + 1)})

    return result


def split_to_tree(s):
    return {'key': '<begin>', 'childs': split(input)}


def segment(node):
    k = node['key']
    childs = node.get('childs')

    if not childs:
        return

    i1 = index.get(k)
    for child in childs:
        i2 = index.get(child['key'])
        child['score'] = gp[i1, i2] if (i1 and
                                        i2) else (1 - ratio) * 1 / len(words)
        segment(child)


def shortest(node):
    childs = node.get("childs")
    score = node.get('score', 0)
    key = node.get('key')

    if not childs:
        return score, [key]

    current_score, current_seq = -1, []
    for child in childs:
        _score, _seq = shortest(child)
        if _score > current_score:
            current_score, current_seq = _score, _seq

    return current_score + score, [key] + current_seq


#================分词函数完成=================

input = '他说的确实在理'

# 将输入转化成tree
root = split_to_tree(input)
# 根据上面的gram概率模型，计算得分
segment(root)

#求最大得分
score, seq = shortest(root)
print(seq, score)

#
# https://www.jianshu.com/p/808cc55a3cd7
#