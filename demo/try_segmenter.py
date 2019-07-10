#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 21:42:06 2019

@author: li-ming-fan
"""


# import sys
# sys.path.append("../ZhongLP")


from ZhongLP.segmenter import Segmenter



segmenter = Segmenter()
    
text = "-2019年1月21日国家统计局发布，2018年中国国内生产总值-90.0309万亿元，按可比价格计算，同比增长6.6%。证书编号：PS20190309。"   
print(text)

tokens = segmenter.segment(text)
print(tokens)

tokens_rep = segmenter.replace_patterned_tokens(tokens)
print(tokens_rep)

text_seg_rep = segmenter.segment_and_replace(text)
print(text_seg_rep)


#
text = '宣紙上走筆至此擱一半'
print(text)   
tokens = segmenter.segment(text)
print(tokens)

