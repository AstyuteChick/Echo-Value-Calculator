
import heapq
from evc_errors import DataMismatchError, InvalidInputError, InternalLogicError

def adjust_req_er(er_req: float, rc: float, buff_val: float)-> float: 
    er_adj = er_req * (1 - (buff_val / rc))
    if er_adj <= 100: er_adj = 0.0
    return er_adj

class GameData:
    rel_val_stat_names = ["Crit Rate(%)", "Crit Damage(%)", "Atk(%)", "Flat Atk", "HP(%)", "Flat HP", "Def(%)", "Flat Def", "Basic(%)", "Heavy(%)", "Skill(%)", "Liberation(%)"]
    er_stat_names = ["Required ER", "ER Importance", "Resonance Cost"]
    substat_names = rel_val_stat_names+["ER(%)"]
    substat_avg = [8.4, 16.8, 9.0, 45.0, 9.0, 450.0, 11.35, 55.0, 9.0, 9.0, 9.0, 9.0, 9.6]
    substat_max = [10.5, 21.0, 11.6, 60.0, 11.6, 580.0, 14.7, 70.0, 11.6, 11.6, 11.6, 11.6, 12.4]
    substat_rolls = {
        "Crit Rate(%)":      [6.3, 6.9, 7.5, 8.1, 8.7, 9.3, 9.9, 10.5],
        "Crit Damage(%)":    [12.6, 13.8, 15.0, 16.2, 17.4, 18.6, 19.8, 21.0],
        "Atk(%)":            [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
        "Flat Atk":          [30.0, 40.0, 50.0, 60.0],
        "HP(%)":             [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
        "Flat HP":           [320.0, 360.0, 390.0, 430.0, 470.0, 510.0, 540.0, 580.0],
        "Def(%)":            [8.1, 9.0, 10.0, 10.9, 11.8, 12.8, 13.8, 14.7],
        "Flat Def":          [40.0, 50.0, 60.0, 70.0],
        "Basic(%)":          [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
        "Heavy(%)":          [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
        "Skill(%)":          [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
        "Liberation(%)":     [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
        "ER(%)":             [6.8, 7.6, 8.4, 9.2, 10.0, 10.8, 11.6, 12.4]
    }
    mainstat_vals={
        4: {"Crit Rate(%)": 22.0, "Crit Damage(%)": 44.0, "Atk(%)": 33.0, "HP(%)": 33.0, "Def(%)": 41.5, "Heal(%)": 0.0},
        3: {"Atk(%)": 30.0, "Element(%)": 0.0, "HP(%)": 30.0, "Def(%)": 38.0, "ER(%)": 32.0},
        1: {"Atk(%)": 18.0, "HP(%)": 22.8, "Def(%)": 18.0}
    }
    secstat_vals={4: ["Flat Atk", 150], 3: ["Flat Atk", 100], 1: ["Flat HP", 2280]}

    def __init__(self, mode: str)-> None: self.ssm = mode

    @property
    def ssm(self)-> dict: return self._ssm
    @ssm.setter
    def ssm(self, mode: str)-> None:
        if not isinstance(mode, str): raise DataMismatchError(f"invalid calculation mode type: {type(mode)}")
        ssm_dict = {}
        if mode == "O":
            for i in range(len(GameData.substat_names)): ssm_dict[GameData.substat_names[i]] = GameData.substat_max[i]
        else:
            for i in range(len(GameData.substat_names)): ssm_dict[GameData.substat_names[i]] = GameData.substat_avg[i]
        self._ssm = ssm_dict

class Character:
    data: dict[str, list] = {
        #Name:                              [[cr%, cd%, atk%, fatk, hp%, fhp, def%, fdef, ba%, ha%, skill%, liberation%], [{name: req_er}, er_imp, rc], analysis]
        "Aalto (Main-DPS)":                 [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.70, 0.0, 0.5*0.15, 0.5*0.10], [{"Default": 125.0}, 0.4, 150.0], True],
        "Aalto (Sub-DPS)":                  [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.45, 0.0, 0.5*0.25, 0.5*0.15], [{"Default": 125.0}, 0.9, 150.0], True],
        "Aemeath (Rupture)":                [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.0, 0.0, 0.5*0.85], [{"Lynae/Lupa + Mornye": 115.0, "Lynae + Shorekeeper": 120.0, "Default": 125.0}, 0.7, 125.0], True],
        "Aemeath (Fusion Burst)":           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.0, 0.0, 0.5*0.85], [{"Denia + Chisa/Lupa": 110.0, "Default": 125.0}, 0.8, 125.0], True],
        "Augusta":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.5*0.15, 0.0], [{"Iuno + Shorekeeper": 125.0, "Mortefi + Shorekeeper": 115.0, "Default": 115.0}, 0.8, 125.0], True],
        "Baizhi":                           [[0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Default": 230.0}, 1.0, 175.0], False],
        "Brant" :                           [[1.0, 1.0, 0.3, 0.2, 0.0, 0.0, 0.0, 0.0, 0.55, 0.0, 0.0, 0.05], [{"Default": 280.0}, 0.9, 175.0], True],
        "Buling":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Carlotta": 125.0, "Phrolova": 135.0, "Default": 135.0}, 1.0, 150.0], False],
        "Calcharo":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.0, 0.0, 0.5*0.55], [{"Default": 125.0}, 0.9, 125.0], True],
        "Camellya":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.75, 0.0, 0.0, 0.5*0.15], [{"Lynae + Shorekeeper": 115.0, "Default": 115.0, "Roccia + Shorekeeper": 125.0}, 0.3, 125.0], True],
        "Cantarella":                       [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.0, 0.5*0.1, 0.0], [{"Midnight Veil (Phrolova + Roccia)": 120.0, "Moonlit Clouds (Carlotta + Shorekeeper)": 140.0, "Default": 135.0}, 0.9, 125.0], True],
        "Carlotta":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85, 0.0], [{"Default": 125.0}, 0.8, 125.0], True],
        "Cartethyia":                       [[1.0, 1.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.5*0.55, 0.0, 0.5*0.15, 0.5*0.3], [{"Default": 110.0}, 1.0, 125.0], True],
        "Changli":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.65, 0.5*0.3], [{"Mono Fusion": 105.0, "Default": 120.0}, 0.8, 125.0], True],
        "Chisa":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.8], [{"With Cartethyia/Hiyuki/Zani": 115.0, "Aemeath + Denia": 110.0, "Default": 125.0}, 0.7, 125.0], True],
        "Chixia":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.5, 0.5*0.3], [{"Default": 140.0}, 0.6, 150.0], True],
        "Ciaccona":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.25, 0.0, 0.5*0.35], [{"Default": 125.0, "Low-Reqs: ": 115.0, "High-Reqs: ": 135.0}, 0.9, 125.0], True],
        "Danjin":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.25, 0.5*0.3], [{"Default": 0.0}, 0.0, 100.0], True],
        "Denia":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.9], [{"Aemeath + Lupa/Chisa": 110.0, "Default": 115.0}, 0.9, 125.0], True],
        "Encore (Hypercarry)":              [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.5, 0.0, 0.5*0.15, 0.5*0.15], [{"Easy Rotation": 130.0, "Advanced Rotation": 105.0, "Default": 125.0}, 0.9, 125.0], True],
        "Galbrena":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.0], [{"Mono Fusion": 110.0, "Default": 125.0}, 0.9, 125.0], True],
        "Hiyuki":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.5*0.85], [{"Lucilla + Chisa": 107.0, "Lynae + Chisa": 115.0, "Lynae + Shorekeeper": 125.0, "Default": 120.0}, 0.6, 125.0], True],
        "Iuno (Main-DPS)":                  [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85], [{"Default": 110.0}, 0.7, 125.0], True],
        "Iuno (Sub-DPS)":                   [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85], [{"Default": 130.0}, 0.9, 125.0], True],
        "Jianxin (Main/Sub-DPS)":           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.4, 0.0, 0.5*0.3], [{"Default": 135.0}, 0.9, 150.0], True],
        "Jingran (Signature Wp.)":          [[1.0, 1.0, 0.39, 0.27, 0.55, 0.15, 0.0, 0.0, 0.0, 0.41, 0.0, 0.0], [{"Default": 115.0, "Mono-Fusion/Rebecca": 120.0}, 1.0, 125.0], True],
        "Jingran (No Signature Wp.)":       [[1.0, 1.0, 0.46, 0.25, 0.92, 0.28, 0.0, 0.0, 0.0, 0.44, 0.0, 0.0], [{"Default": 115.0, "Mono-Fusion/Rebecca": 120.0}, 1.0, 125.0], True],
        "Jinhsi":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.5*0.15], [{"Alternate Rotation Burst": 125.0, "Default": 115.0}, 0.3, 150.0], True],
        "Jiyan":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85, 0.5*0.1, 0.0], [{"Iuno + Ciaccona": 115.0, "Default": 125.0}, 1.0, 125.0], True],
        "Lingyang":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.5*0.35, 0.5*0.1], [{"Default": 125.0}, 0.9, 125.0], True],
        "Lucy":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.9, 0.0, 0.0], [{"Default": 120.0}, 0.7, 125.0], True],
        "Lucilla (Glacio Chafe)":           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.75, 0.0, 0.5*0.15, 0.0], [{"Default": 0.0}, 0.0, 0.0], True],
        "Lucilla (Echo)":                   [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.15, 0.0, 0.5*0.15, 0.0], [{"Default": 0.0}, 0.0, 0.0], True],
        "Lumi":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.4, 0.0, 0.5*0.3, 0.5*0.3], [{"Default": 155.0}, 0.9, 125.0], True],
        "Lupa":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.15, 0.5*0.75], [{"Mono-Fusion - Brant + Changli, Galbrena + Mornye, Aemeath + Denia": 115.0, "Encore + Shorekeeper": 130.0, "Aemeath + Mornye": 120.0, "Default": 120.0}, 0.9, 125.0], True],
        "Luuk Herssen":                     [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.9, 0.0, 0.0, 0.0], [{"Sanhua + Mornye": 115.0, "Lynae + Mornye": 125.0, "Default": 125.0}, 0.7, 125.0], True],
        "Lynae":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.0, 0.0, 0.5*0.2], [{"Iuno + Ciaccona": 110.0, "Default": 125.0}, 0.9, 125.0], True],
        "Mornye":                           [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.5*0.75], [{"Default": 260.0}, 1.0, 175.0], False],
        "Mornye (Pure Support)":            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0], [{"Default": 260.0}, 1.0, 175.0], False],
        "Mortefi":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.0, 0.5*0.2, 0.5*0.7], [{"Default": 120.0}, 0.9, 125.0], True],
        "Phoebe":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.15, 0.5*0.5, 0.0, 0.5*0.15], [{"Absolution": 0.0, "Confession": 125.0, "Default": 125.0}, 1.0, 125.0], True],
        "Phrolova":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.5, 0.0], [{"Default": 0.0}, 0.0, 0], True],
        "Qingxiao":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.35, 0.0, 0.5*0.3], [{"Deina + Supp": 110.0, "Lynae + Supp": 120.0, "Ciaccona + ANY character": 105.0, "Default": 115.0}, 0.6, 125.0], True],
        "Qiuyuan":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.65, 0.0, 0.0], [{"Galbrena + Shorekeeper": 115.0, "Phrolova + Cantarella": 125.0, "Default": 125.0}, 0.9, 125.0], True],
        "Rebecca":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.0, 0.0, 0.0], [{"Default": 120.0}, 0.9, 125.0], True],
        "Roccia":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.6, 0.5*0.15, 0.0], [{"Phrolova + Cantarella": 115.0, "Camellya + Shorekeeper": 125.0, "Default": 130.0}, 0.9, 125.0], True],
        "Rover (Aero)":                     [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.5*0.2], [{"Iuno + Ciaccona": 125.0, "Cartethyia + Ciaccona": 145.0, "Default": 145.0}, 0.9, 150.0], True],
        "Rover (Havoc)":                    [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.5*0.2, 0.5*0.3], [{"Sub DPS / Phrolova + Cantarella": 140.0, "Main DPS / Lynae + Shorekeeper": 125.0, "Default": 125.0}, 0.6, 125.0], True],
        "Rover (Spectro)":                  [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.5*0.35, 0.5*0.4], [{"Default": 125.0}, 1.0, 125.0], True],
        "Sanhua":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.5*0.3, 0.5*0.3], [{"Default": 115.0}, 0.9, 100.0], True],
        "Sigrika":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Qiuyuan + Ciaccona/Phrolova": 110.0, "Qiuyuan + Shorekeeper": 120.0, "Default": 120.0}, 0.8, 100.0], True],
        "Suisui":                           [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Default": 260.0}, 1.0, 175.0], False],
        "Taoqi (sub DPS)":                  [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.25, 0.5*0.5, 0.0, 0.0, 0.5*0.5], [{"Default": 125.0}, 0.9, 125.0], True],
        "Taoqi (sup)":                      [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0], [{"Default": 175.0}, 1.0, 125.0], False],
        "The Shorekeeper":                  [[0.0, 1.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.75], [{"With Fallacy": 230.0, "Default": 230.0, "No Fallacy": 240.0}, 1.0, 175.0], False],
        "The Shorekeeper (Pure Support)":   [[0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"With Fallacy": 230.0, "Default": 230.0, "No Fallacy": 240.0}, 1.0, 175.0], False],
        "Verina":                           [[0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Default": 230.0}, 1.0, 175.0], False],
        "Xiangli Yao":                      [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.0, 0.5*0.15, 0.5*0.7], [{"Default": 120.0}, 0.9, 125.0], True],
        "Yangyang":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.5*0.15, 0.5*0.45], [{"Default": 115.0}, 0.9, 100.0], True],
        "Xuanling Yangyang":                [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.9, 0.0, 0.0], [{"Rebecca + Chisa": 110.0, "Chisa + Mornye": 120.0, "Default": 120.0}, 0.6, 125.0], True],
        "Yinlin":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.5*0.15], [{"Xiangli Yao + Shorekeeper": 125.0, "Default": 135.0}, 0.9, 125.0], True],
        "Youhu":                            [[0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Default": 165.0}, 0.9, 100.0], False],
        "Yuanwu":                           [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.5*0.5, 0.5*0.4], [{"No Liberation": 0.0, "Default": 135.0}, 0.9, 125.0], True],
        "Zani":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.65, 0.0, 0.5*0.2], [{"Default": 120.0}, 1.0, 125.0], True],
        "Zhezhi":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.0, 0.0, 0.0], [{"Empyrean Anthem": 130.0, "Default": 130.0, "Moonlit Clouds": 115.0}, 0.9, 125.0], True]
    }
    zhezhi_users = ["Carlotta", "Jinhsi", "Hiyuki", "Lingyang"]
    for char_name in data:
        if char_name not in zhezhi_users: continue
        for team_name in data[char_name][1][0]:
            if "Default" in team_name:
                try:
                    def_er = data[char_name][1][0][team_name]
                    zhe_er = adjust_req_er(def_er, data[char_name][1][2], 15)
                    if zhe_er > 100: data[char_name][1][0]["Zhezhi Outro"] = round(zhe_er, 1)
                    else: data[char_name][1][0]["Zhezhi Outro"] = 0.0
                except ZeroDivisionError: pass
                break

    def __init__(self, name: str, team: str)-> None:
        self.name = name
        self.rel_val = Character.data[self.name][0]
        self.er = team
        self.anal = Character.data[self.name][2]
        self.teams = Character.data[self.name][1][0]

    @property
    def name(self)-> str: return self._name
    @name.setter
    def name(self, name: str)-> None:
        if not isinstance(name, str): raise DataMismatchError(f"invalid character name type: {type(name)}")
        if name not in Character.data: raise DataMismatchError(f"invalid character name: {name}")
        self._name = name

    @property
    def rel_val(self)-> dict: return self._rel_val
    @rel_val.setter
    def rel_val(self, rel_val: list)-> None:
        if len(rel_val) != len(GameData.rel_val_stat_names): raise InternalLogicError(f"invalid relative value list: Expected length {len(GameData.rel_val_stat_names)}, got instead {len(rel_val)}")
        rel_val_dict = {}
        for i in range(len(rel_val)): rel_val_dict[GameData.rel_val_stat_names[i]] = rel_val[i]
        self._rel_val = rel_val_dict

    @property
    def er(self)-> dict: return self._er
    @er.setter
    def er(self, team: str)-> None:
        if not isinstance(team, str): raise DataMismatchError(f"team is not a string: {type(team)}")
        if team not in Character.data[self.name][1][0]: raise DataMismatchError(f"team not found for {self.name}: {team}")
        er_dict = {}
        er_dict[GameData.er_stat_names[0]] = Character.data[self.name][1][0][team]
        er_dict[GameData.er_stat_names[1]] = Character.data[self.name][1][1]
        er_dict[GameData.er_stat_names[2]] = Character.data[self.name][1][2]
        self._er = er_dict

    @property
    def teams(self)-> list: return self._teams
    @teams.setter
    def teams(self, teams: dict)-> None:
        if not isinstance(teams, dict): raise InternalLogicError(f"teams type is not dict: {type(teams)}")
        team_list = []
        for team in teams: team_list.append(team)
        self._teams = team_list

class Echo:
    def __init__(self, ssr: list)-> None: self.ssr = ssr

    @property
    def ssr(self)-> dict: return self._ssr
    @ssr.setter
    def ssr(self, ssr: list)-> None:
        if not (isinstance(ssr, list)) or len(ssr) != 13: raise DataMismatchError(f"Corrupted echo format/data")
        ssr_data = {}
        for i, stat_name in enumerate(GameData.substat_names): 
            try: ssr_data[stat_name] = float(ssr[i])
            except (ValueError, TypeError): raise DataMismatchError(f"couldn't convert {type(ssr[i])} to float")
        stat_count = 0
        for substat in ssr_data:
            if ssr_data[substat] != 0.0: stat_count = stat_count + 1
        if stat_count > 5: raise DataMismatchError(f"Too many sub stats: {stat_count}")
        self._ssr = ssr_data

class Build:
    def __init__(self, build_stats: list)-> None: self.build_stats = build_stats

    @property
    def build_stats(self)-> dict: return self._build_stats
    @build_stats.setter
    def build_stats(self, bs_in: list)-> None:
        if not (isinstance(bs_in, list)) or len(bs_in) != 13: raise DataMismatchError(f"Corrupted build format/data")
        bs_data = {}
        for i, stat_name in enumerate(GameData.substat_names): 
            try: bs_data[stat_name] = float(bs_in[i])
            except (ValueError, TypeError): raise DataMismatchError(f"couldn't convert {type(bs_in[i])} to float")
        self._build_stats = bs_data

def init_data(char_name: str, team_name: str, tot_er: float)-> tuple[Character, dict, GameData]: 
    char = Character(char_name, team_name)
    if char.er["Required ER"] > 100: er_net = tot_er - char.er["Required ER"]
    else: er_net = 0
    if er_net > 0 and er_net <= 3.1: er_net = 0
    if er_net > 3.1: er_net -= 3.1
    er_net = {"av": er_net, "ep": er_net}
    return char, er_net, GameData("N")

def av_er(er_net_av: float, er_ssr: float, er_med: float, er_imp: float)-> tuple[float, float]:
    if er_net_av < 0: er_av = (er_ssr / er_med) * er_imp
    else:
        er_net_av = er_net_av - er_ssr
        if er_net_av < 0:
            er_av = (-er_net_av / er_med) * er_imp
            er_net_av = 0
        else: er_av = 0
    return er_net_av, er_av

def ep_er(er_net_ep: float, er_ssr: float, er_med: float, er_imp: float)-> tuple[float, float]:
    if er_net_ep < 0:
        er_net_ep_temp = er_net_ep - er_ssr
        if er_net_ep_temp / er_med <= -1: er_ep = er_imp
        else: er_ep = ((-er_net_ep_temp) / er_med) * er_imp
    else:
        er_net_ep = er_net_ep - er_ssr
        if er_net_ep < 0:
            if er_net_ep / er_med <= -1: er_ep = er_imp
            else: er_ep = ((-er_net_ep) / er_med) * er_imp
            er_net_ep = 0
        else: er_ep = 0
    return er_net_ep, er_ep

def av_stats(echo_ssr: dict, ssm: dict, char_player: Character, er_net_av: float)-> tuple[float, float]:
    er_net_av, total_av = av_er(er_net_av, echo_ssr["ER(%)"], ssm["ER(%)"], char_player.er["ER Importance"])
    for substat in echo_ssr:
        if substat != "ER(%)": total_av = total_av + ((echo_ssr[substat] / ssm[substat]) * char_player.rel_val[substat])
    return total_av, er_net_av

def ep_stats(echo_ssr_er: float, ssm_er: float, char_player: Character, er_net_ep: float)-> tuple[float, float]:
    rel_pot_vals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    er_net_ep, rel_pot_vals[12] = ep_er(er_net_ep, echo_ssr_er, ssm_er, char_player.er["ER Importance"])
    index = 0
    for substat in char_player.rel_val:
        rel_pot_vals[index] = char_player.rel_val[substat]
        index = index + 1
        if index == 12: break
    return sum(heapq.nlargest(5, rel_pot_vals)), er_net_ep

def ep_stats_build(echo_ssr: dict, ssm: dict, char_player: Character, er_net_ep: float)-> tuple[float, float]:
    rel_pot_vals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    if er_net_ep < 0:
        if echo_ssr["ER(%)"] > 12.4:
            echo_ssr_temp = 9.6
            echo_ssr["ER(%)"] = echo_ssr["ER(%)"] - 9.6
        else:
            echo_ssr_temp = echo_ssr["ER(%)"]
            echo_ssr["ER(%)"] = 0.0
        er_net_ep_temp = er_net_ep - echo_ssr_temp
        if er_net_ep_temp / ssm["ER(%)"] <= -1: er_ep = char_player.er["ER Importance"]
        else: er_ep = ((-er_net_ep_temp) / ssm["ER(%)"]) * char_player.er["ER Importance"]
    else:
        if echo_ssr["ER(%)"] > 12.4:
            echo_ssr_temp = 9.6
            echo_ssr["ER(%)"] = echo_ssr["ER(%)"] - 9.6
        else:
            echo_ssr_temp = echo_ssr["ER(%)"]
            echo_ssr["ER(%)"] = 0.0
        er_net_ep = er_net_ep - echo_ssr_temp
        if er_net_ep < 0:
            if er_net_ep / ssm["ER(%)"] <= -1:
                er_ep = char_player.er["ER Importance"]
            else:
                er_ep = ((-er_net_ep) / ssm["ER(%)"]) * char_player.er["ER Importance"]
            er_net_ep = 0
        else: er_ep = 0
    rel_pot_vals[12] = er_ep
    index = 0
    for substat in char_player.rel_val:
        rel_pot_vals[index] = char_player.rel_val[substat]
        index = index + 1
        if index == 12: break
    return sum(heapq.nlargest(5, rel_pot_vals)), er_net_ep

def es_stats(av_total: float, ep_total: float)-> float: 
    if ep_total == 0.0: return 0.0
    else: return (av_total / ep_total) * 100

def analysis(score: float, na: bool)-> str:
    if na:
        if score >= 99: score_tier = "Godly"
        elif score >= 88: score_tier = "Extreme"
        elif score >= 77: score_tier = "High Investment"
        elif score >= 66: score_tier = "Well Built"
        elif score >= 55: score_tier = "Decent"
        elif score >= 44: score_tier = "Base Level"
        else: score_tier = "Unbuilt"
    else: score_tier = "Not Applicable"
    return score_tier

def echo_calc(char: Character, ssr: list, ssm: dict, er_net: dict)-> tuple[str, str]: 
    echo = Echo(ssr)
    if char.er["Required ER"] <= 100: echo.ssr["ER(%)"] = 0.0
    av_total, er_net["av"] = av_stats(echo.ssr, ssm, char, er_net["av"])
    ep_total, er_net["ep"] = ep_stats(echo.ssr["ER(%)"], ssm["ER(%)"], char, er_net["ep"])
    es_total = round(es_stats(av_total, ep_total), 3)
    es_tier = analysis(es_total, char.anal)
    return str(es_total), es_tier

def change_echo_order(ssr: list[list])-> list[int]:
    echo_order = []
    sanity_check = 0
    for index in range(5):
        if float(ssr[index][12]) != 0.0: echo_order.append(index)
        else: sanity_check += 1
    if len(echo_order) + sanity_check != 5: raise DataMismatchError(f"Sanity Check Failed: {echo_order} {sanity_check}")
    for index in range(5):
        if index not in echo_order: echo_order.append(index)
    if len(echo_order) != 5: raise InternalLogicError("Full Score: Corrupted data while sorting echoes. ")
    return echo_order

def full_calc(char: Character, ssr: list[list], ssm: dict, er_net: dict)-> tuple[str, str]:
    echo_order = change_echo_order(ssr)
    es_total = [0.0, 0.0, 0.0, 0.0, 0.0]
    es_tier = ["Unknown", "Unknown", "Unknown", "Unknown", "Unknown"]
    for echo_no in range(5): 
        es_to, es_ti = echo_calc(char, ssr[echo_order[echo_no]], ssm, er_net)
        es_total[echo_order[echo_no]], es_tier[echo_order[echo_no]] = float(es_to), es_ti
    bs_total=round(sum(es_total) / 5, 3)
    bs_tier=analysis(bs_total, char.anal)
    return f"{bs_total}: {es_total}", f"{bs_tier}: {es_tier}"

def init_build(char: Character, build: Build, main_stats: dict)-> None: 
    if char.rel_val["Atk(%)"] != 0 and char.rel_val["HP(%)"] == 0: 
        if main_stats["echo_cost"][1] == 4: build.build_stats["Flat HP"] = 2280 * 3
        else: build.build_stats["Flat HP"] = 2280 * 2
    elif char.rel_val["HP(%)"] != 0 and char.rel_val["Atk(%)"] == 0: 
        if main_stats["echo_cost"][1] == 4: build.build_stats["Flat Atk"] = 150 * 2
        else: build.build_stats["Flat Atk"] = 150 + 200
    elif char.rel_val["Atk(%)"] == 0 and char.rel_val["HP(%)"] == 0: 
        if main_stats["echo_cost"][1] == 4: 
            build.build_stats["Flat HP"]=2280 * 3
            build.build_stats["Flat Atk"]=150 * 2
        else: 
            build.build_stats["Flat HP"]=2280 * 2
            build.build_stats["Flat Atk"]=150 + 200

def remove_main_and_sec_stats(build: Build, main_stats: dict)-> None:
    for echo_no in range(5):
        cur_echo_cost = main_stats["echo_cost"][echo_no]
        cur_mainstat = main_stats["echo_mainstat"][echo_no]
        try: cur_mainstat_val = GameData.mainstat_vals[cur_echo_cost][cur_mainstat]
        except KeyError: raise DataMismatchError(f"echo cost ({cur_echo_cost}) doesn't have ({cur_mainstat}) as an option")
        except Exception as msg: raise InternalLogicError(f"unexpected error raised: {msg}")
        cur_secstat = GameData.secstat_vals[cur_echo_cost][0]
        cur_secstat_val = GameData.secstat_vals[cur_echo_cost][1]
        if cur_mainstat != "Element(%)" and cur_mainstat != "Heal(%)":
            build.build_stats[cur_mainstat] = build.build_stats[cur_mainstat] - cur_mainstat_val
            if build.build_stats[cur_mainstat] < -0.00000001: raise InvalidInputError("Remember that stats from Echo PRESETS are expected")
        build.build_stats[cur_secstat] = build.build_stats[cur_secstat] - cur_secstat_val
        if build.build_stats[cur_secstat] < -0.00000001: raise InvalidInputError("Remember that stats from Echo PRESETS are expected")

def build_calc(char: Character, ssr: list, ssm: dict, er_net: dict, main_stats: dict|None)-> tuple[str, str]: 
    if main_stats == None: raise InternalLogicError("data not received")
    build = Build(ssr)
    if char.er["Required ER"] < 100: build.build_stats["ER(%)"] = 0.0
    for substat in char.rel_val: 
        if char.rel_val[substat] == 0: build.build_stats[substat] = 0
    init_build(char, build, main_stats)
    remove_main_and_sec_stats(build, main_stats)
    av_total, er_net["av"] = av_stats(build.build_stats, ssm, char, er_net["av"])
    ep_total_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    for _ in range(5): ep_total_list[_], er_net["ep"] = ep_stats_build(build.build_stats, ssm, char, er_net["ep"])
    ep_total = sum(ep_total_list)
    es_total = round(es_stats(av_total, ep_total), 3)
    es_tier = analysis(es_total, char.anal)
    return str(es_total), es_tier

def main(char_name: str, team_name: str, tot_er: float, ssr: list, type_in: str, main_stats: dict|None = None)-> tuple[str, str]:
    char, er_net, ssgd = init_data(char_name, team_name, tot_er)
    if type_in == "echo": return echo_calc(char, ssr, ssgd.ssm, er_net)
    elif type_in == "full": return full_calc(char, ssr, ssgd.ssm, er_net)
    elif type_in == "build": return build_calc(char, ssr, ssgd.ssm, er_net, main_stats)
    else: raise InternalLogicError(f"Invalid calculation path: {type_in}")

if __name__ == "__main__": pass
    # for char in Character.data:
    #     def_found = False
    #     for team in Character.data[char][1][0]:
    #         if "Default" in team: def_found = True
    #     if def_found == False: raise DataMismatchError(f"Default not found for {char}")
