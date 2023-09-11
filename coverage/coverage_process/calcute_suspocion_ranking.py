"""
计算可疑度排名

# Top-n
Top-n 是一个用于评估故障定位准确性的简单指标。它表示在排名前 n 的函数(或代码片段)中，有多少个是真正与故障相关的。通常，如果一个故障定位方法能够在 top-n 列表中准确地标识出故障相关的函数，那么这个方法就被认为是有效的。

# MAR (Mean Average Rank)

# MFR (Mean First Rank)

"""
import os
import numpy as np
import pandas as pd
from tqdm import tqdm


class CalcuteSuspicionRanking():
    def __init__(self):
        self.suspicion_method = None
        self.suspicion_method_list = None
        self.suspicion_matrix_map = None
        curren_path = os.path.dirname(os.path.abspath(__file__))
        self.suspicion_matrix_father_path = "/root/kratos_testcase/coverage/coverage_process/function_res/suspicion_res"
        self.suspicion_ranking_matrix_save_father_path = "/root/kratos_testcase/coverage/coverage_process/function_res/suspicion_ranking_res"
        if not os.path.exists(self.suspicion_ranking_matrix_save_father_path):
            os.makedirs(self.suspicion_ranking_matrix_save_father_path)
        # 生效的问题件
        self.run_testcase_list = ["11307", "10805", "3442"]
        # self.run_testcase_list = ["1", "2"]

        # ranking方法列表
        self.suspicion_ranking_method_list = ["MAR", "MFR", "Top-1", "Top-5", "Top-10", "Top-20", "Top-50", "Top-All",
                                              "Ranking"]
        # 可疑度方法列表
        self.suspicion_method_list = None
        # 结果矩阵
        self.suspicion_ranking_matrix = {}
        # 故障函数map
        self.fault_function_dict = {
            "11307": ["_ZN6Kratos5Model15DeleteModelPartERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE"],
            "3442": [
                "_ZN6Kratos40ResidualBasedEliminationBuilderAndSolverINS_10UblasSpaceIdN5boost7numeric5ublas17compressed_matrixIdNS4_15basic_row_majorImlEELm0ENS4_15unbounded_arrayImSaImEEENS8_IdSaIdEEEEENS4_6vectorIdSC_EEEENS1_IdNS4_6matrixIdS7_SC_EESF_EENS_12LinearSolverISG_SJ_NS_9ReordererISG_SJ_EEEEE26ResizeAndInitializeVectorsESt10shared_ptrINS_6SchemeISG_SJ_EEERSP_ISD_ERSP_ISF_ESW_RNS_16PointerVectorSetINS_7ElementENS_13IndexedObjectESt4lessImESt8equal_toImESP_ISY_ESt6vectorIS14_SaIS14_EEEERNSX_INS_9ConditionESZ_S11_S13_SP_IS1A_ES15_IS1B_SaIS1B_EEEERNS_11ProcessInfoE"],
            "10805": ["_ZN6Kratos40FindNeighbourElementsOfConditionsProcess7ExecuteEv"],
            "1": ["2"],
            "2": ["1"]
        }

    def set_suspicion_method_dict(self):
        suspicion_method_list = []
        for suspicion_method in self.suspicion_matrix_map[self.run_testcase_list[0]]:
            if suspicion_method == "testcase_name":
                continue
            suspicion_method_list.append(suspicion_method)
        self.suspicion_method_list = suspicion_method_list
        # 构建pd矩阵
        pd.options.mode.chained_assignment = None  # 关闭 SettingWithCopyWarning 警告
        self.suspicion_ranking_matrix = pd.DataFrame(np.nan,
                                                     index=self.suspicion_method_list,
                                                     columns=self.suspicion_ranking_method_list)

    def get_all_suspicion_ranking(self):
        """
        获取所有可疑度排名
        :return:
        """
        # 读取所有文件
        suspicion_matrix_paths = os.listdir(self.suspicion_matrix_father_path)
        self.get_suspicion_matrix(
            suspicion_matrix_paths)
        print("开始计算可疑度排名")
        for suspicion_method in tqdm(self.suspicion_method_list):
            self.suspicion_method = suspicion_method
            # 计算可疑度排名
            self.calcute_suspicion_ranking()
            # 第一列为function_name
            a = 1
            # 获取可疑度排名
        # 保存可疑度排名矩阵
        print("保存可疑度排名矩阵: ",
              os.path.join(self.suspicion_ranking_matrix_save_father_path, "suspicion_ranking_matrix.xlsx"))
        self.suspicion_ranking_matrix.to_excel(
            os.path.join(self.suspicion_ranking_matrix_save_father_path, "suspicion_ranking_matrix.xlsx"))

        return 0

    def calcute_suspicion_ranking(self):
        """
        获取可疑度排名
        :return:
        """
        self.get_top_n(-1)
        self.get_top_n(1)
        self.get_top_n(5)
        self.get_top_n(10)
        self.get_top_n(20)
        self.get_top_n(50)
        self.get_mfr()
        self.get_mar()
        self.get_ranking()
        return 0

    def get_suspicion_matrix(self, suspicion_matrix_paths):
        """
        获取可疑度矩阵
        :return:
        """
        suspicion_matrix_map = {}
        # 读取可疑度矩阵
        for suspicion_matrix_path in suspicion_matrix_paths:
            if suspicion_matrix_path.split("_")[0] not in self.run_testcase_list:
                continue
            # 读取可疑度矩阵
            suspicion_matrix_map[suspicion_matrix_path.split("_")[0]] = pd.read_excel(os.path.join(
                self.suspicion_matrix_father_path, suspicion_matrix_path))
        self.suspicion_matrix_map = suspicion_matrix_map
        # 获取可疑度方法字典
        self.set_suspicion_method_dict()

    def save_suspicion_ranking_matrix(self):
        """
        保存可疑度排名矩阵
        :return:
        """
        pass

    def get_ranking(self):
        """
        获取排名
        :return:
        """
        ranking_list = []
        for testcase_name in self.run_testcase_list:
            # 获取每个testcase排行n的函数
            top_n_function_list = self.get_top_n_function_list(
                -1, self.suspicion_matrix_map[testcase_name])
            # 判断是否包含故障函数
            for fault_function in self.fault_function_dict[testcase_name]:
                ranking_list.append(
                    testcase_name + "_" + str(top_n_function_list.index(fault_function)))
            # 计算top-n
        self.suspicion_ranking_matrix["Ranking"][self.suspicion_method] = ','.join(ranking_list)
        return ranking_list

    def get_top_n(self, n):
        """
        获取top-n
        # Top-n
        Top-n 是一个用于评估故障定位准确性的简单指标。
        它表示在排名前 n 的函数(或代码片段)中，有多少个是真正与故障相关的。
        通常，如果一个故障定位方法能够在 top-n 列表中准确地标识出故障相关的函数，那么这个方法就被认为是有效的。

        :return:
        """
        # 获取每个testcase排行n的函数
        #
        # suspicion_matrix = suspicion_matrix.sort_values(
        #     by="suspicion_value", ascending=False)
        # 统计命中次数
        contain_fault_function_num = 0
        ranking_list = []
        for testcase_name in self.run_testcase_list:
            # 获取每个testcase排行n的函数
            top_n_function_list = self.get_top_n_function_list(
                n, self.suspicion_matrix_map[testcase_name])
            # 判断是否包含故障函数
            if self.fault_function_dict[testcase_name][0] in top_n_function_list:
                contain_fault_function_num += 1
            # 计算top-n
        top_n = contain_fault_function_num / len(self.run_testcase_list)
        if n == -1:
            self.suspicion_ranking_matrix["Top-All"][self.suspicion_method] = top_n
        else:
            self.suspicion_ranking_matrix["Top-" + str(n)][self.suspicion_method] = top_n
        # 存储
        return top_n

    def get_top_n_function_list(self, n, suspicion_matrix):
        """
        获取top-n的函数
        :return:
        """
        # 获取每个testcase排行n的函数
        suspicion_matrix_desc = suspicion_matrix.sort_values(
            by=self.suspicion_method, ascending=False)
        if n == len(self.suspicion_method_list):
            top_n_function_list = suspicion_matrix_desc["testcase_name"].tolist()
        else:
            top_n_function_list = suspicion_matrix_desc["testcase_name"].tolist()[:n]
        # top_n_function_list = suspicion_matrix_desc["testcase_name"].tolist()
        return top_n_function_list

    def get_mar(self):
        """
        获取MAR
        MAR (Mean Average Rank) 是一个用于评估多个故障的平均排名的指标。给定m个故障，每个故障i在排名列表中的位置为 rank;，MAR 定义为:
        MAR-rank;mi 1
        如果 MAR的值较低，则表示故障定位方法较为准确。
        :return:
        """
        ranking_list = []
        for testcase_name in self.run_testcase_list:
            # 获取每个testcase排行n的函数
            top_n_function_list = self.get_top_n_function_list(
                -1, self.suspicion_matrix_map[testcase_name])
            # 判断是否包含故障函数
            ranking = -1
            for fault_function in self.fault_function_dict[testcase_name]:
                if ranking == -1:
                    ranking = top_n_function_list.index(fault_function)
                ranking = min(ranking, top_n_function_list.index(fault_function))
            ranking_list.append(
                ranking)
            # 计算top-n
        mar = sum(ranking_list) / len(self.run_testcase_list)
        # 保存
        self.suspicion_ranking_matrix["MAR"][self.suspicion_method] = int(mar)
        return mar

    def get_mfr(self):
        """
        获取MFR
        MFR (Mean First Rank) 是一个类似于MAR的指标，但它只考虑每个故障的“第1个”出现的排名。
        如果一个故障在多个位置有多个实例，MFR 只关心第一个实例的排名。MFR的计算公式与 MAR类似
        :return:
        """
        # 获取每个testcase排行n的函数
        #
        # suspicion_matrix = suspicion_matrix.sort_values(
        #     by="suspicion_value", ascending=False)
        # 统计命中次数
        ranking_list = []
        for testcase_name in self.run_testcase_list:
            # 获取每个testcase排行n的函数
            top_n_function_list = self.get_top_n_function_list(
                -1, self.suspicion_matrix_map[testcase_name])
            # 判断是否包含故障函数
            ranking_list.append(
                top_n_function_list.index(self.fault_function_dict[testcase_name][0]))
            # 计算top-n
        mfr = sum(ranking_list) / len(self.run_testcase_list)
        # 保存
        self.suspicion_ranking_matrix["MFR"][self.suspicion_method] = int(mfr)
        return mfr


calcute_suspicion_ranking = CalcuteSuspicionRanking()
calcute_suspicion_ranking.get_all_suspicion_ranking()
