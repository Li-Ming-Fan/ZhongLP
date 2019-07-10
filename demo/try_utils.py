#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 21:53:40 2019

@author: li-ming-fan
"""

from ZhongLP import zh_utils


text =  "   ih kkk .  lll. "
print(text)

text_c = zh_utils.clean_simply_text_line(text)
print(text_c)


