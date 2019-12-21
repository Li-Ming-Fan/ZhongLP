

import sys
sys.path.append("../ZhongLP")

from ZhongLP import utils_zh


text = "....?????"
print(text)

text_quan = utils_zh.convert_ban_to_quan(text)
print(text_quan)

text_ban = utils_zh.convert_quan_to_ban(text_quan)
print(text_ban)
