"""
本文件为api文件，用于计算各种数据
"""

def ptqrToken(qrsig) -> int:
    """
    计算ptqrtoken,需要qrsig
    :param qrsig: 获取二维码获得的qrsig
    :return: ptqrtoken
    """

    n, i, e = len(qrsig), 0, 0

    while n > i:
        e += (e << 5) + ord(qrsig[i])
        i += 1

    return 2147483647 & e

def bkn(skey):
    """
    计算bkn,需要skey
    :param skey: Cookies中的skey
    :return: bkn
    """

    t,n,o = 5381,0,len(skey)

    while n < o:
        t += (t << 5) + ord(skey[n])
        n += 1

    return t & 2147483647

def g_tk(p_skey):
    """
    计算g_tk,需要p_skey
    :param p_skey: Cookies里的p_skey
    :return: g_tk
    """

    t = 5381
    for i in p_skey:
        t += (t << 5) + ord(i)
    return t & 2147483647