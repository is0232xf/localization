# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 17:35:55 2016

@author: Fujiichang
"""
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

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


class BayesFilter(object):
    def __init__(self, p_s_a, p_o_s):
        self.p_s_a = p_s_a
        self.p_o_s = p_o_s

    def update_p_s(self, o, p_s_bar):
        g = 5 * [0]
        f = 5 * [0]

        for s in range(5):
            g[s] = self.p_o_s[s][o] * p_s_bar[s]

        sum_g = sum(g[s] for s in range(5))
        for s in range(5):
            f[s] = g[s]/sum_g
        return f

    def update_p_s_bar(self, p_s, a):
        p_s_bar = 5 * [0]
        for s in range(5):
            p_s_bar[s] = sum([self.p_s_a[m][a][s] * p_s[m] for m in range(5)])
        return p_s_bar


class Controller(object):

    def __init__(self, goals):
        self.goals = goals

    def calculate_expectation(self, f):
        expectation = sum(f[s] * s for s in range(5))
        return int(round(expectation, 0))

    def determine_a(self, p_s, determined_s_log):
        determined_s = self.calculate_expectation(p_s)
        determined_s_log.append(determined_s)
        next_goal = self.goals[0]
        if next_goal == determined_s:
            self.goals.pop(0)
            if self.is_terminated() is False:
                next_goal = self.goals[0]
        if next_goal - determined_s < 0:
            a = 0
        elif next_goal - determined_s > 0:
            a = 1
        else:
            a = 2
        return a

    def is_terminated(self):
        return is_empty(self.goals)


class Simulator(object):
    def __init__(self, p_s_a, p_o_s):
        self._s = 0
        self.p_s_a = p_s_a
        self.p_o_s = p_o_s

    def _draw_s(self, previous_s, a):
        p_s = self.p_s_a[previous_s][a]
        new_s = multinomial(p_s)
        return new_s

    def get_o(self):
        o = multinomial(self.p_o_s[self._s])
        return o

    def set_a(self, a):
        self._s = self._draw_s(self._s, a)

    def get_s(self):
        return self._s


def main():
    o_log = []
    determined_s_log = []
    a_log = []
    actual_s_log = []
    actual_s_log.append(0)
    simulator = Simulator(p_s_a, p_o_s)
    estimator = BayesFilter(p_s_a, p_o_s)
    goals = [4, 0]
    controller = Controller(goals)
    p_s_bar = 5 * [0]
    p_s_bar[0] = 1
    t = 0

    while True:
        print "step:", t, "############"
        o = simulator.get_o()
        o_log.append(o)
        print "o =", o
        p_s = estimator.update_p_s(o, p_s_bar)
        show_p_s(p_s)

        a = controller.determine_a(p_s, determined_s_log)

        if controller.is_terminated() is True:
            print_result(o_log, actual_s_log, determined_s_log, a_log, t)
            break

        a_log.append(a)
        print "a =", a
        simulator.set_a(a)
        s = simulator.get_s()
        print "s =", s
        actual_s_log.append(s)
        t = t + 1
        p_s_bar = estimator.update_p_s_bar(p_s, a)
        show_p_s(p_s_bar)


def is_empty(goals):
    return len(goals) == 0


def print_result(o_log, actual_s_log, determined_s_log, a_log, t):
        print "Finish"
        print "o   = " + str(o_log)
        print "s   = " + str(actual_s_log)
        print "e_s = " + str(determined_s_log)
        print "a   = " + str(a_log)
        show_result(actual_s_log, determined_s_log)
        show_merged_result(actual_s_log, determined_s_log)
        calculate_correct_answer(actual_s_log, determined_s_log, t)


def show_p_s(p_s):
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


def calculate_correct_answer(s_log, d_s_log, t):
    count = 0
    for i in range(len(s_log) - 1):
        if s_log[i] == d_s_log[i]:
            count = count + 1
    correct_answer = 100 * count / t
    print "Percentage of correct answer : " + str(correct_answer) + " %"

if __name__ == '__main__':
#    '''
#    docstring
#    '''
#    n = 100
#    state_number = 5
#    s = 0
#    a = 2
#    o = 0
#    t = 0
#    flg = 0
#    o_log = []
#    s_log = []
#    a_log = []
#    p_s = state_number * [0]
#    p_s_bar = state_number * [0]
#    d_s_log = []
#
#    while True:
#
#        # 観測前のp_sを推測
#        if t == 0:
#            p_s_bar = state_number * [0]
#            p_s_bar[0] = 1
#        else:
#            p_s_bar = estimate_s.calculate_predicted_distribution(p_s_a, p_s, a)
#        show_p_s(p_s_bar, s)
#
#        # oをドロー
#        o = draw_o(p_o_s, s)
#        print "o = "+str(o)
#        o_log.append(o)
#
#        # 観測後のp_sを推測
#        p_s = estimate_s.calculate_corrected_distribution(p_o_s, p_s_bar, o)
#        show_p_s(p_s, s)
#        determined_s = estimate_s.calculate_expectation(p_s)
#        print "determined_s = "+str(determined_s)
#        d_s_log.append(determined_s)
#        if determined_s == 4:
#            flg = 1
#
#        if determined_s == 0 and t > 5:
#            break
#
#        # aをドロー
#        a = draw_a(flg, p_s)
#        if a == -1:
#            break
#        a_log.append(a)
#
#        # sをドロー,時間の更新
#        if t == 0:
#            s_log.append(0)
#        s = draw_p_s(s, a)
#        print "s = "+str(s)
#        s_log.append(s)
#        t = t + 1
    main()
