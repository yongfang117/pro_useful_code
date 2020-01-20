#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# 打开文件
fo = open("input.txt", "r")
 
a = [x for x in fo.readlines()]
a[-1] = a[-1] + "\n"
a.sort()

fi = open("output.txt", "w")
fi.writelines(a)

# 关闭文件
fi.close()
fo.close()