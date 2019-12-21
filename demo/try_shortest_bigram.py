


import sys
# sys.path.append("../ZhongLP")


from ZhongLP.segmenter_pk.shortest_bigram import ShortestBigramSegmenter

from ZhongLP.segmenter_pk.shortest_bigram import save_data_to_pkl, load_data_from_pkl



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

# 用户自定义词典
usr_dict = {"剧场外": 1}



segmenter = ShortestBigramSegmenter()
# segmenter._token_index = index
# segmenter._token_freq = fd
# segmenter._bigram_freq = gp
segmenter._custom_dict = usr_dict


file_token_index = "token_index.pkl"
file_bigram_freq = "bigram_freq.pkl"

# save_data_to_pkl(index, file_token_index)
# save_data_to_pkl(gp, file_bigram_freq)



#================测试=================

# input = '他说的确实在理'
input = "求最大得分的路径"
input = "".join("他 那些 舞台 下 、 剧场 外 的 事 的确 是 鲜为人知 的 。".split())

tokens = segmenter.segment(input)
print(tokens)

