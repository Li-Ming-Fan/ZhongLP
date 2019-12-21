#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 21:53:40 2019

@author: li-ming-fan
"""

import sys
# sys.path.append("../ZhongLP")

from ZhongLP.converter import Converter

text = '宣紙上走筆至此擱一半'
print(text)   

cvt = Converter()
text = cvt.convert2simplified(text)
print(text)



