# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 18:21:13 2019

@author: limingfan
"""

import jieba
# jieba.load_userdict("../z_data/user_domain.dict") 
# jieba.initialize() # 手动初始化（可选）


import re

class Segmenter():
    
    pattern_int = re.compile(r'^[0-9]+$')
    pattern_float = re.compile(r'^[0-9,]*\.[0-9,]+$')
    pattern_percent = re.compile(r'^[\.0-9,]+%+$')    
    pattern_longalnum = re.compile(r'^[0-9,%\\/\.a-zA-Z]+$')
    
    def __init__(self):
        
        self.flag_replace = 1
        
        #
        self.long_alnum_threshold = 8
        
        self.list_patterns = []
        self.list_patterns.append( (self.pattern_int, "[tkn_int]") )
        self.list_patterns.append( (self.pattern_float, "[tkn_float]") )
        self.list_patterns.append( (self.pattern_percent, "[tkn_percent]") )
        
        self.list_patterns_length = []
        self.list_patterns_length.append(
                (self.pattern_longalnum, "[tkn_alnum]", self.long_alnum_threshold) )
        #
        
        #
        self.reset()
        #
    
    #
    def reset(self):
        
        pass
    
    #
    def load_user_dict(self, file_path):
        
        pass
            
    def add_token(self, token, pos="n", count=1000):
        
        pass
    
    def remove_token(self, token, pos="n"):
        
        pass
    
    #
    def segment(self, text):
        """
        """        
        list_no_rep = self.segment_no_replacement(text)
        #
        if self.flag_replace:
            return self.replace_patterned_tokens(list_no_rep)
        else:
            return list_no_rep
        #
    
    def segment_no_replacement(self, text):
        """
        """
        return list(jieba.cut(text))
        
    def replace_patterned_tokens(self, list_no_replacement):
        """
        """
        list_rep = []
        for token in list_no_replacement:
            for pattern, rep_token in self.list_patterns:
                if pattern.match(token):
                    list_rep.append(rep_token)
                    break
            else:
                for pattern, rep_token, thr in self.list_patterns_length:
                    if pattern.match(token) and len(token) >= thr:
                        list_rep.append(rep_token)
                        break
                else:
                    list_rep.append(token)
                #
        #
        # for - break
        #
        return list_rep
    
    #
    @staticmethod
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

        
#
if __name__ == '__main__':
    
    segmenter = Segmenter()
    segmenter.start()
    
    text = "-2019年1月21日国家统计局发布，2018年中国国内生产总值-90.0309万亿元，按可比价格计算，同比增长6.6%。证书编号：PS20190309。"   
    print(text)   
    tokens = segmenter.segment(text)
    print(tokens)
    
    text = '宣紙上走筆至此擱一半'
    print(text)   
    tokens = segmenter.segment(text)
    print(tokens)
    
    segmenter.close()
    
    
    
