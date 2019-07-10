#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 21:24:01 2019

@author: li-ming-fan
"""

#
def convert_traditional_to_simplified(text):
    """
    """
    return text    

#
def convert_limited_to_banjiao(text, list_limited=None):
    """
    """
    return text

def convert_limited_to_quanjiao(text, list_limited=None):
    """
    """
    return text

#
def clean_simply_text_line(text):
    """ strip and standardize blank tokens
    """
    text = text.strip()
    text = " ".join(text.split())
    return text

#  
def segment_sentences(text, delimiters = None):
    """ 
    """
    if delimiters is None:
        delimiters = ['?', '!', ';', '？', '！', '。', '；', '…', '\n']
    #
    text = text.replace('...', '。。。').replace('..', '。。')
    #
    # 引用(“ ”)中有句子的情况
    # text = text.replace('"', '').replace('“', '').replace('”', '')
    #
    len_text = len(text)
    
    sep_posi = []
    for item in delimiters:
        posi_start = 0
        while posi_start < len_text:
            try:
                posi = posi_start + text[posi_start:].index(item)  #
                sep_posi.append(posi)
                posi_start = posi + 1               
            except BaseException:
                break # while
        #
    #
    sep_posi.sort()
    num_sep = len(sep_posi)
    #
    
    #
    list_sent = []
    #
    if num_sep == 0: return [ text ]
    #
    posi_last = 0
    for idx in range(0, num_sep - 1):
        posi_curr = sep_posi[idx] + 1
        posi_next = sep_posi[idx + 1]
        if posi_next > posi_curr:
            list_sent.append( text[posi_last:posi_curr] )
            posi_last = posi_curr
    #
    posi_curr = sep_posi[-1] + 1
    if posi_curr == len_text:
        list_sent.append( text[posi_last:] )
    else:
        list_sent.extend( [text[posi_last:posi_curr], text[posi_curr:]] )
    #
    return list_sent
    

