# -*- coding:utf-8 -*-
import math
    # gamma压缩 获取gamma值
def __gamma__(num):
    if num == 1:
        return 0
    tail_len = int(math.log(num,2))
    bin_t = __getbin__(tail_len)
    #print(bin(bin_t))
    bin_result = num & bin_t                        #原二进制后tail_len位
    #print(bin(bin_result))
    len_code = __getbin__(tail_len,True)       #编码中 尾长
    #print(bin(len_code))
    result = 0x00
    result = (result << tail_len) | len_code
    result = (result << tail_len) | bin_result
    return result
#解gamma编码
def __gammaUncompress__(num):
    if num == 0:
        return 1
    temp= bin(num)
    #print(temp)
    counter = 0
    length_all = len(temp)-2
    i = 2
    while temp[i] == '1' and i < length_all:
        counter += 1
        i += 1
    counter += 1
    tail = __getbin__(length_all-counter,False)
    #print('tail = ',bin(tail))
    tail = tail & num
    result = 0x01
    result = result << (length_all - counter)
    result = result | tail
    return result

    #转换为一元码
def __getbin__(len,last_zero=False):
    a = 0
    if len == 1:
        if not last_zero:
            return 0x01
        else:
            return 0x02

    for i in range(len):
        a = a | 0x01
        a = a << 1
    if not last_zero:
        a = a >> 1
    return a
