# First part of the implementation for all methods in the class
import math
import pandas as pd
import os
from tqdm import tqdm

class SuspicionCalculator:
    def __init__(self, bug_name, save_path):
        self.formules_susp = {}
        self.bug_name = int(bug_name)
        self.set_res_save_path(save_path)
        # n_if = 该代码部分导致失败的测试用例数量
        self.n_if = 0
        # n_ip = 该代码部分导致通过的测试用例数量
        self.n_ip = 0
        # n_nf = 未执行该代码部分并导致失败的测试用例数量
        self.n_nf = 0
        # n_np = 未执行该代码部分并导致通过的测试用例数量
        self.n_np = 0

    def set_res_save_path(self, save_path):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_path = os.path.join(save_path, str(
            self.bug_name)+"_suspicion.xlsx")
        self.save_path = save_path
    # Initialize formula names

    def init_formulas(self):
        self.formules_susp["testcase_name"] = {}
        for x in ['Ochiai', 'Ample', 'Anderberg', 'Arithmetic mean', 'Cohen', 'Dice', 'Euclid', 'Fleiss', 'Geometric mean',
                  'Goodman', 'Hamann', 'Hamming etc.', 'Harmonic mean', 'Jaccard', 'Kulczynski1', 'Kulczynski2', 'M1',
                  'M2', 'Ochiai2', 'Overlap', 'Rogers & Tanimoto', 'Rogot1', 'Rogot2', 'Russell & Rao', 'Scott',
                  'Simple matching', 'Sokal', 'Sorensen-Dice', 'Tarantula', 'Wong1', 'Wong2', 'Wong3', 'Zoltar',
                  'Naish2(Op2)', 'DStar(D*)', 'GP13']:
            self.formules_susp[x] = {}

    def calculate_suspicion_parameters(self, run_count_all):
        for testcase_name, run_count in run_count_all.items():
            # 如果是bug测试用例
            if testcase_name == self.bug_name:
                # 如果bug执行过这个函数，那么n_if = 1
                if run_count != 0:
                    self.n_if = 1
                else:
                    self.n_nf = 1
            # 如果是正常测试用例
            else:
                # 如果正常测试用例执行过这个函数，那么n_ip += 1
                if run_count != 0:
                    self.n_ip += 1
                else:
                    self.n_np += 1

    def set_all_function_name(self, function_matrix):
        for function_name, run_count_all in function_matrix.iterrows():
            for testcase_name, run_count in run_count_all.items():
                self.formules_susp["testcase_name"][testcase_name] = testcase_name
            break

    # Calculate all methods for each method name in method_set

    def calculate_all_methods(self, function_matrix):
        self.init_formulas()
        # self.set_all_function_name(function_matrix)
        for function_name, run_count_all in tqdm(function_matrix.iterrows()):
            self.calculate_suspicion_parameters(run_count_all)

            n_if = self.n_if
            n_ip = self.n_ip
            n_nf = self.n_nf
            n_np = self.n_np
            self.formules_susp['testcase_name'][function_name] = function_name

            # Calling all the methods
            self.calculate_Ochiai(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Ample(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Anderberg(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Arithmetic_mean(
                function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Cohen(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Dice(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Euclid(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Fleiss(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Geometric_mean(
                function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Goodman(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Hamann(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Hamming_etc(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Harmonic_mean(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Jaccard(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Kulczynski1(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Kulczynski2(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_M1(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_M2(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Ochiai2(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Overlap(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Rogers_Tanimoto(
                function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Rogot1(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Rogot2(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Russell_Rao(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Scott(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Simple_matching(
                function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Sokal(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Sorensen_Dice(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Tarantula(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Wong1(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Wong2(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Wong3(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Zoltar(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_Naish2_Op2(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_DStar_D(function_name, n_if, n_ip, n_np, n_nf)
            self.calculate_GP13(function_name, n_if, n_ip, n_np, n_nf)

        # 将字典转换为DataFrame
        df = pd.DataFrame(self.formules_susp)

        # 存储为Excel文件
        df.to_excel(self.save_path, index=False)

        return 0
    # Ochiai method

    def calculate_Ochiai(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / math.sqrt((n_if + n_ip) * (n_if + n_nf))
            self.formules_susp['Ochiai'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Ample method
    def calculate_Ample(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = math.fabs(n_if / (n_if + n_nf) - n_ip / (n_ip + n_np))
            self.formules_susp['Ample'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Anderberg method
    def calculate_Anderberg(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_if + 2 * (n_nf + n_ip))
            self.formules_susp['Anderberg'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Arithmetic mean method
    def calculate_Arithmetic_mean(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (2 * n_if * n_np - 2 * n_nf * n_ip) / \
                ((n_if + n_ip) * (n_np + n_nf) + (n_if + n_nf) * (n_ip + n_np))
            self.formules_susp['Arithmetic mean'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Cohen method
    def calculate_Cohen(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (2 * n_if * n_np - 2 * n_nf * n_ip) / \
                ((n_if + n_ip) * (n_np + n_ip) + (n_if + n_nf) * (n_nf + n_np))
            self.formules_susp['Cohen'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Dice method
    def calculate_Dice(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = 2 * n_if / (n_if + n_nf + n_ip)
            self.formules_susp['Dice'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Euclid method
    def calculate_Euclid(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = math.sqrt(n_if + n_np)
            self.formules_susp['Euclid'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Fleiss method
    def calculate_Fleiss(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (4 * n_if * n_np - 4 * n_nf * n_ip - (n_nf - n_ip) *
                          (n_nf - n_ip)) / (2 * n_if * n_nf * n_ip + 2 * n_np * n_nf * n_ip)
            self.formules_susp['Fleiss'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Geometric mean method
    def calculate_Geometric_mean(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (n_if * n_np - n_nf * n_ip) / math.sqrt((n_if + n_ip)
                                                                 * (n_np + n_nf) * (n_if + n_nf) * (n_ip + n_np))
            self.formules_susp['Geometric mean'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Goodman method
    def calculate_Goodman(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (2 * n_if - n_nf - n_ip) / (2 * n_if + n_nf + n_ip)
            self.formules_susp['Goodman'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Hamann method
    def calculate_Hamann(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (n_if + n_np - n_nf - n_ip) / \
                (n_if + n_nf + n_ip + n_np)
            self.formules_susp['Hamann'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Hamming etc. method
    def calculate_Hamming_etc(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if + n_np
            self.formules_susp['Hamming etc.'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Harmonic mean method
    def calculate_Harmonic_mean(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = ((n_if * n_np - n_nf * n_ip) * (n_if + n_ip) * (n_np + n_nf) + (n_if + n_nf) * (n_ip + n_np)) / \
                ((n_if + n_ip) * (n_np + n_nf) * (n_if + n_nf) * (n_ip + n_np))
            self.formules_susp['Harmonic mean'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Jaccard method
    def calculate_Jaccard(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_if + n_nf + n_ip)
            self.formules_susp['Jaccard'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Kulczynski1 method
    def calculate_Kulczynski1(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_nf + n_ip)
            self.formules_susp['Kulczynski1'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Kulczynski2 method
    def calculate_Kulczynski2(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_nf + n_ip)
            self.formules_susp['Kulczynski2'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # M1 method
    def calculate_M1(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (n_if + n_np) / (n_nf + n_ip)
            self.formules_susp['M1'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # M2 method
    def calculate_M2(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_if + n_np + 2*(n_if + n_ip))
            self.formules_susp['M2'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Ochiai2 method
    def calculate_Ochiai2(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if * n_np / \
                math.sqrt((n_if + n_ip) * (n_np + n_nf)
                          * (n_if + n_nf) * (n_ip + n_np))
            self.formules_susp['Ochiai2'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Overlap method
    def calculate_Overlap(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / min(n_if, min(n_nf, n_ip))
            self.formules_susp['Overlap'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Rogers & Tanimoto method
    def calculate_Rogers_Tanimoto(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (n_if + n_np) / (n_if + n_np + 2 * (n_nf + n_ip))
            self.formules_susp['Rogers & Tanimoto'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Rogot1 method
    def calculate_Rogot1(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = 0.5 * \
                (n_if / (2 * n_if + n_nf + n_ip) + n_np / (2 * n_np + n_nf + n_ip))
            self.formules_susp['Rogot1'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Rogot2 method
    def calculate_Rogot2(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = 0.25 * (n_if / (n_if + n_ip) + n_if /
                                 (n_if + n_nf) + n_np / (n_np + n_ip) + n_np / (n_np + n_nf))
            self.formules_susp['Rogot2'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Russell & Rao method
    def calculate_Russell_Rao(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_if + n_nf + n_ip + n_np)
            self.formules_susp['Russell & Rao'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Scott method
    def calculate_Scott(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (4 * n_if * n_np - 4 * n_nf * n_ip - (n_nf - n_ip) *
                          (n_nf - n_ip)) / ((2 * n_if + n_nf + n_ip) * (2 * n_np + n_nf + n_ip))
            self.formules_susp['Scott'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Simple matching method
    def calculate_Simple_matching(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (n_if + n_np) / (n_if + n_nf + n_ip + n_np)
            self.formules_susp['Simple matching'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Sokal method
    def calculate_Sokal(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (2 * (n_if + n_np)) / \
                (2 * (n_if + n_np) + n_nf + n_ip)
            self.formules_susp['Sokal'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Sorensen-Dice method
    def calculate_Sorensen_Dice(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = 2 * n_if / (2 * n_if + n_nf + n_ip)
            self.formules_susp['Sorensen-Dice'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Tarantula method
    def calculate_Tarantula(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = (n_if / (n_if + n_nf)) / \
                (n_if / (n_if + n_nf) + n_ip / (n_ip + n_np))
            self.formules_susp['Tarantula'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Wong1 method
    def calculate_Wong1(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if
            self.formules_susp['Wong1'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Wong2 method
    def calculate_Wong2(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if - n_ip
            self.formules_susp['Wong2'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Wong3 method
    def calculate_Wong3(self, function_name, n_if, n_ip, n_np, n_nf):
        if n_ip <= 2:
            suspicious = n_if - n_ip
        elif n_ip > 2 and n_ip <= 10:
            suspicious = n_if - (2 + 0.1 * (n_ip - 2))
        else:
            suspicious = n_if - (2.8 + 0.001 * (n_ip - 10))
        self.formules_susp['Wong3'][function_name] = suspicious

    # Zoltar method
    def calculate_Zoltar(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_if + n_nf + n_ip +
                                 10000 * n_nf * n_ip / n_if)
            self.formules_susp['Zoltar'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # Naish2(Op2) method
    def calculate_Naish2_Op2(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if - n_ip / (n_ip + n_np + 1)
            self.formules_susp['Naish2(Op2)'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # DStar(D*) method
    def calculate_DStar_D(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if / (n_ip + n_nf)
            self.formules_susp['DStar(D*)'][function_name] = suspicious
        except ZeroDivisionError:
            pass

    # GP13 method
    def calculate_GP13(self, function_name, n_if, n_ip, n_np, n_nf):
        try:
            suspicious = n_if * (1 + 1 / (2 * n_ip + n_if))
            self.formules_susp['GP13'][function_name] = suspicious
        except ZeroDivisionError:
            pass
