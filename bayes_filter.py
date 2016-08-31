# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 17:35:55 2016

@author: Fujiichang
"""
import random
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import estimate_s

p_o_s = [[0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]]
#
#p_o_s = [[0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]]
#
#p_o_s = [[0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]]

p_s_a = [[[1, 0, 0, 0, 0], [0.1, 0.9, 0, 0, 0], [1, 0, 0, 0, 0]],
         [[0.9, 0.1, 0, 0, 0], [0, 0.1, 0.9, 0, 0], [0, 1, 0, 0, 0]],
         [[0, 0.9, 0.1, 0, 0], [0, 0, 0.1, 0.9, 0], [0, 0, 1, 0, 0]],
         [[0, 0, 0.9, 0.1, 0], [0, 0, 0, 0.1, 0.9], [0, 0, 0, 1, 0]],
         [[0, 0, 0, 0.9, 0.1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]]


def show_p_s(p_s, s):
    plt.ylim([0.0, 1.0])
    plt.bar(range(len(p_s)), p_s, align='center')
    plt.show()


def show_merged_result(s, determined_s):
    plt.gca().invert_yaxis()
    plt.xlabel("state")
    plt.ylabel("time")
    plt.plot(determined_s, range(len(determined_s)), "-+", markersize=10)
    plt.plot(s, range(len(s)), "g--x", markersize=10)
    plt.legend(['determined_s', 'actual_s'])
    plt.show()


def show_result(s, determined_s):
    plt.subplot(211)
    plt.title("determined_s")
    plt.xlabel("state")
    plt.ylabel("time")
    plt.gca().invert_yaxis()
    plt.gca().yaxis.set_minor_locator(tick.MultipleLocator(1))
    plt.plot(determined_s, range(len(determined_s)), '--o')

    plt.subplot(212)
    plt.title("actual_s")
    plt.xlabel("state")
    plt.ylabel("time")
    plt.gca().invert_yaxis()
    plt.gca().yaxis.set_minor_locator(tick.MultipleLocator(1))
    plt.plot(s, range(len(s)), '--o')
    plt.tight_layout()
    plt.show()


def cout_list(p_s):
    count_dict = collections.Counter(p_s)
    return len(count_dict.items())

def multinomial(p):
    sum_p = sum(p)
    assert(sum_p >= 1)
    cum_sum = len(p)*[0]
    cum_sum = calculate_cum_sum(p)
    K = len(cum_sum)
    u = random.random()

    for k in range(K):
        if u <= cum_sum[k]:
            return k
    return k - 1


def calculate_cum_sum(p):
    K = len(p)
    cum_sum = K*[0]
    for n in range(K):
        if n == 0:
            cum_sum[n] = p[n]
        elif n != 0:
            cum_sum[n] = cum_sum[n-1] + p[n]
    return cum_sum


def draw_p_s(s, a):
    p_s = state_number * [0]
    p_s = p_s_a[s][a]
    d_p_s = multinomial(p_s)
    return d_p_s


def draw_a(flg, p_s):
    max_value_list = [i for i, x in enumerate(p_s) if x == max(p_s)]
    if len(max_value_list) != 1:
        print "Command: stay"
        return 2
    if flg == 0:
        print "Command: move right"
        return 1
    elif flg == 1:
        print "Command: move left"
        return 0


def draw_o(p_o_s, s):
    '''
    '''
    p_o = 0
    p_o = multinomial(p_o_s[s])
    return p_o

if __name__ == '__main__':
    '''
    docstring
    '''
    n = 100
    state_number = 5
    s = 0
    a = 2
    o = 0
    t = 0
    flg = 0
    o_log = []
    s_log = []
    a_log = []
    p_s = state_number * [0]
    p_s_bar = state_number * [0]
    d_s_log = []

    while True:

        # 観測前のp_sを推測
        if t == 0:
            p_s_bar = state_number * [0.2]
        else:
            p_s_bar = estimate_s.calculate_predicted_distribution(p_s_a, p_s, a)
        show_p_s(p_s_bar, s)

        # oをドロー
        o = draw_o(p_o_s, s)
        print "o = "+str(o)
        o_log.append(o)

        # 観測後のp_sを推測
        p_s = estimate_s.calculate_corrected_distribution(p_o_s, p_s_bar, o)
        show_p_s(p_s, s)
        determined_s = estimate_s.calculate_expectation(p_s)
        d_s_log.append(determined_s)
        if determined_s == 4:
            flg = 1

        if t > 5:
            if determined_s == 0:
                print "Finish"
                print "o   = " + str(o_log)
                print "s   = " + str(s_log)
                print "e_s = " + str(d_s_log)
                print "a   = " + str(a_log)
                show_result(s_log, d_s_log)
                show_merged_result(s_log, d_s_log)
                break

        # aをドロー
        a = draw_a(flg, p_s)
        if a == -1:
            break
        a_log.append(a)

        # sをドロー,時間の更新
        if t == 0:
            s_log.append(0)
        s = draw_p_s(s, a)
        print "s = "+str(s)
        s_log.append(s)
        t = t + 1
