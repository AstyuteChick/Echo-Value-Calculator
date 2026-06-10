
import heapq

def adjust_req_er(er_req, rc, buff_val) -> float: 
    er_adj=er_req*(1-(buff_val/rc))
    if er_adj<=100: er_adj=0.0
    return er_adj

class GameData:

    rel_val_stat_names=["Crit Rate(%)", "Crit Damage(%)", "Atk(%)", "Flat Atk", "HP(%)", "Flat HP", "Def(%)", "Flat Def", "Basic(%)", "Heavy(%)", "Skill(%)", "Liberation(%)"]
    er_stat_names=["Required ER", "ER Importance", "Resonance Cost"]
    substat_names=["Crit Rate(%)", "Crit Damage(%)", "Atk(%)", "Flat Atk", "HP(%)", "Flat HP", "Def(%)", "Flat Def", "Basic(%)", "Heavy(%)", "Skill(%)", "Liberation(%)", "ER(%)"]
    substat_medians=[8.4, 16.8, 9.0, 45.0, 9.0, 450.0, 11.35, 55.0, 9.0, 9.0, 9.0, 9.0, 9.6]
    substat_max=[10.5, 21.0, 11.6, 60.0, 11.6, 580.0, 14.7, 70.0, 11.6, 11.6, 11.6, 11.6, 12.4]
    substat_rolls={"Crit Rate(%)": [6.3, 6.9, 7.5, 8.1, 8.7, 9.3, 9.9, 10.5],
                   "Crit Damage(%)": [12.6, 13.8, 15.0, 16.2, 17.4, 18.6, 19.8, 21.0],
                   "Atk(%)": [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
                   "Flat Atk": [30.0, 40.0, 50.0, 60.0],
                   "HP(%)": [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
                   "Flat HP": [320.0, 360.0, 390.0, 430.0, 470.0, 510.0, 540.0, 580.0],
                   "Def(%)": [8.1, 9.0, 10.0, 10.9, 11.8, 12.8, 13.8, 14.7],
                   "Flat Def": [40.0, 50.0, 60.0, 70.0],
                   "Basic(%)": [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
                   "Heavy(%)": [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
                   "Skill(%)": [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
                   "Liberation(%)": [6.4, 7.1, 7.9, 8.6, 9.4, 10.1, 10.9, 11.6],
                   "ER(%)": [6.8, 7.6, 8.4, 9.2, 10.0, 10.8, 11.6, 12.4]}
    mainstat_vals={4: {"Crit Rate(%)": 22.0, "Crit Damage(%)": 44.0, "Atk(%)": 33.0, "HP(%)": 33.0, "Def(%)": 41.5, "Heal(%)": 0.0},
                   3: {"Atk(%)": 30.0, "Element(%)": 0.0, "HP(%)": 30.0, "Def(%)": 38.0, "ER(%)": 32.0},
                   1: {"Atk(%)": 18.0, "HP(%)": 22.8, "Def(%)": 18.0}}
    sec_stats={4: ["Flat Atk", 150], 3: ["Flat Atk", 100], 1: ["Flat HP", 2280]}

    def __init__(self, mode: str): self.ssm=mode

    @property
    def ssm(self)-> dict: return self._ssm
    @ssm.setter
    def ssm(self, mode: str)-> None:
        ssm_dict={}
        if mode=="O":
            for i in range(13): ssm_dict[GameData.substat_names[i]]=GameData.substat_max[i]
        else:
            for i in range(13): ssm_dict[GameData.substat_names[i]]=GameData.substat_medians[i]
        self._ssm=ssm_dict

class Character:

    data: dict[str, list]={
        #Name:                              [[cr%, cd%, atk%, fatk, hp%, fhp, def%, fdef, ba%, ha%, skill%, liberation%], [{name: req_er}, imp_er, rc], analysis]
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
        "Ciaccona":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.25, 0.0, 0.5*0.35], [{"Default": 125.0}, 0.9, 125.0], True],
        "Danjin":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.25, 0.5*0.3], [{"Default": 0.0}, 0.0, 100.0], True],
        "Denia":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.9], [{"Aemeath + Lupa/Chisa": 110.0, "Luuk Herssen + Mornye": 115.0, "Default": 115.0}, 0.9, 125.0], True],
        "Encore (Hypercarry)":              [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.5, 0.0, 0.5*0.15, 0.5*0.15], [{"Easy Rotation": 130.0, "Advanced Rotation": 105.0, "Default": 125.0}, 0.9, 125.0], True],
        "Galbrena":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.0], [{"Mono Fusion": 110.0, "Default": 125.0}, 0.9, 125.0], True],
        "Hiyuki":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.5*0.85], [{"Lynae + Chisa": 115.0, "Lynae + Shorekeeper": 125.0, "Default": 120.0}, 0.6, 125.0], True],
        "Iuno (Main-DPS)":                  [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85], [{"Default": 110.0}, 0.7, 125.0], True],
        "Iuno (Sub-DPS)":                   [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85], [{"Default": 130.0}, 0.9, 125.0], True],
        "Jianxin (Main/Sub-DPS)":           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.25, 0.5*0.4, 0.0, 0.5*0.3], [{"Default": 135.0}, 0.9, 150.0], True],
        "Jinhsi":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.5*0.15], [{"Alternate Rotation Burst": 125.0, "Default": 115.0}, 0.3, 150.0], True],
        "Jiyan":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85, 0.5*0.1, 0.0], [{"Iuno + Ciaccona": 115.0, "Default": 125.0}, 1.0, 125.0], True],
        "Lingyang":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.5*0.35, 0.5*0.1], [{"Default": 125.0}, 0.9, 125.0], True],
        "Lucy":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.9, 0.0, 0.0], [{"Default": 120.0}, 0.7, 125.0], True],
        "Lumi":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.4, 0.0, 0.5*0.3, 0.5*0.3], [{"Default": 155.0}, 0.9, 125.0], True],
        "Lupa":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.15, 0.5*0.75], [{"Mono-Fusion - Brant + Changli, Galbrena + Mornye, Aemeath + Denia": 115.0, "Encore + Shorekeeper": 130.0, "Aemeath + Mornye": 120.0, "Default": 120.0}, 0.9, 125.0], True],
        "Luuk Herssen":                     [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.9, 0.0, 0.0, 0.0], [{"Sanhua + Mornye": 115.0, "Lynae + Mornye": 125.0, "Default": 125.0}, 0.7, 125.0], True],
        "Lynae":                            [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.0, 0.0, 0.5*0.2], [{"Iuno + Ciaccona": 110.0, "Default": 125.0}, 0.9, 125.0], True],
        "Mornye":                           [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.5*0.75], [{"Default": 260.0}, 1.0, 175.0], False],
        "Mornye (Pure Support)":            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0], [{"Default": 260.0}, 1.0, 175.0], False],
        "Mortefi":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.0, 0.5*0.2, 0.5*0.7], [{"Default": 120.0}, 0.9, 125.0], True],
        "Phoebe":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.15, 0.5*0.5, 0.0, 0.5*0.15], [{"Absolution": 0.0, "Confession": 125.0, "Default": 125.0}, 1.0, 125.0], True],
        "Phrolova":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.5, 0.0], [{"Default": 0.0}, 0.0, 0], True],
        "Qiuyuan":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.65, 0.0, 0.0], [{"Galbrena + Shorekeeper": 115.0, "Phrolova + Cantarella": 125.0, "Default": 125.0}, 0.9, 125.0], True],
        "Rebecca":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.0, 0.0, 0.0], [{"Default": 120.0}, 0.9, 125.0], True],
        "Roccia":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.6, 0.5*0.15, 0.0], [{"Phrolova + Cantarella": 115.0, "Camellya + Shorekeeper": 125.0, "Default": 130.0}, 0.9, 125.0], True],
        "Rover (Aero)":                     [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.5*0.2], [{"Iuno + Ciaccona": 125.0, "Cartethyia + Ciaccona": 145.0, "Default": 145.0}, 0.9, 150.0], True],
        "Rover (Havoc)":                    [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.5*0.2, 0.5*0.3], [{"Sub DPS / Phrolova + Cantarella": 140.0, "Main DPS / Lynae + Shorekeeper": 125.0, "Default": 125.0}, 0.6, 125.0], True],
        "Rover (Spectro)":                  [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.5*0.35, 0.5*0.4], [{"Default": 125.0}, 1.0, 125.0], True],
        "Sanhua":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.5*0.3, 0.5*0.3], [{"Default": 115.0}, 0.9, 100.0], True],
        "Sigrika":                          [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Qiuyuan + Ciaccona/Phrolova": 110.0, "Qiuyuan + Shorekeeper": 120.0, "Default": 120.0}, 0.8, 100.0], True],
        "Taoqi (sub DPS)":                  [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.25, 0.5*0.5, 0.0, 0.0, 0.5*0.5], [{"Default": 125.0}, 0.9, 125.0], True],
        "Taoqi (sup)":                      [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0], [{"Default": 175.0}, 1.0, 125.0], False],
        "The Shorekeeper":                  [[0.0, 1.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.75], [{"With Fallacy": 230.0, "Default": 230.0, "No Fallacy": 240.0}, 1.0, 175.0], False],
        "The Shorekeeper (Pure Support)":   [[0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"With Fallacy": 230.0, "Default": 230.0, "No Fallacy": 240.0}, 1.0, 175.0], False],
        "Verina":                           [[0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Default": 230.0}, 1.0, 175.0], False],
        "Xiangli Yao":                      [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.1, 0.0, 0.5*0.15, 0.5*0.7], [{"Default": 120.0}, 0.9, 125.0], True],
        "Yangyang":                         [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.35, 0.0, 0.5*0.15, 0.5*0.45], [{"Default": 115.0}, 0.9, 100.0], True],
        "Yinlin":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.7, 0.5*0.15], [{"Xiangli Yao + Shorekeeper": 125.0, "Default": 135.0}, 0.9, 125.0], True],
        "Youhu":                            [[0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [{"Default": 165.0}, 0.9, 100.0], False],
        "Yuanwu":                           [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.5*0.5, 0.5*0.4], [{"No Liberation": 0.0, "Default": 135.0}, 0.9, 125.0], True],
        "Zani":                             [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.65, 0.0, 0.5*0.2], [{"Default": 120.0}, 1.0, 125.0], True],
        "Zhezhi":                           [[1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.5*0.8, 0.0, 0.0, 0.0], [{"Empyrean Anthem": 130.0, "Default": 130.0, "Moonlit Clouds": 115.0}, 0.9, 125.0], True]
    }

    for char_name in data:
        if char_name not in ["Carlotta", "Jinhsi", "Hiyuki", "Lingyang"]: continue
        for team in data[char_name][1][0]:
            if "Default" in team:
                try:
                    def_er=data[char_name][1][0][team]
                    zhe_er=adjust_req_er(def_er, data[char_name][1][2], 15)
                    if zhe_er>100: data[char_name][1][0]["Zhezhi Outro"]=round(zhe_er, 1)
                    else: data[char_name][1][0]["Zhezhi Outro"]=0.0
                except ZeroDivisionError: pass
                break

    def __init__(self, name: str, team: str)-> None:
        self.name=name
        self.rv=Character.data[self.name][0]
        self.team=team
        self.er=self.team
        self.anal=Character.data[self.name][2]

    @property
    def name(self)-> str: return self._name
    @name.setter
    def name(self, name: str)-> None:
        char_found=False
        for char_name in Character.data:
            if char_name==name:
                char_found=True
                break
        if char_found!=True: raise ValueError("Unexpected Error - Character not found")
        self._name=name

    @property
    def team(self)->list: return self._team
    @team.setter
    def team(self, team_in:str)->None:
        team_stat=None
        team_stats=Character.data[self.name][1][0]
        for team in team_stats:
            if team_in == team: 
                team_stat=float(team_stats[team])
                break
        if team_stat==None: raise ValueError("Unexpected Error - Team not found")
        er_stat = [team_stat, Character.data[self.name][1][1], Character.data[self.name][1][2]]
        self._team=er_stat

    @property
    def rv(self)-> dict: return self._rv
    @rv.setter
    def rv(self, rv_list: list)-> None:
        rv_dict={}
        for index in range(12): rv_dict[GameData.rel_val_stat_names[index]]=rv_list[index]
        self._rv=rv_dict

    @property
    def er(self)-> dict: return self._er
    @er.setter
    def er(self, er_list: list)-> None:
        er_dict={}
        for index in range(3): er_dict[GameData.er_stat_names[index]]=er_list[index]
        self._er=er_dict

class Echo:

    def __init__(self, ssr_in: list)-> None: self.ssr=ssr_in

    @property
    def ssr(self)-> dict: return self._ssr
    @ssr.setter
    def ssr(self, ssr_in: list) -> None:
        ssr_data={}
        index=0
        for stat_name in GameData.substat_names:
            ssr_data[stat_name]=float(ssr_in[index])
            index=index+1
        if len(ssr_data)!=13: raise ValueError("Unexpected Error - Corrupted Echo Substat Data: "+str(len(ssr_data)))
        stat_count=0
        for substat in ssr_data:
            if ssr_data[substat]!=0.0: stat_count=stat_count+1
        if stat_count>5: raise ValueError("Unexpected Error - Too many sub stats: "+str(stat_count))
        self._ssr=ssr_data

class Build:

    def __init__(self, build_stats: list)-> None: self.build_stats=build_stats

    @property
    def build_stats(self)-> dict: return self._build_stats
    @build_stats.setter
    def build_stats(self, bs_in: list)-> None:
        bs_data={}
        index=0
        for stat_name in GameData.substat_names:
            bs_data[stat_name]=float(bs_in[index])
            index=index+1
        if len(bs_data)!=13: raise ValueError("Unexpected Error - Corrupted Build Substat Data: "+str(len(bs_data)))
        self._build_stats=bs_data

def av_er(er_net_av: float, er_ssr: float, er_med: float, er_imp: float)-> tuple[float, float]:
    if er_net_av<0: er_av=(er_ssr/er_med)*er_imp
    else:
        er_net_av=er_net_av-er_ssr
        if er_net_av<0:
            er_av=(-er_net_av/er_med)*er_imp
            er_net_av=0
        else: er_av=0
    return er_net_av, er_av

def ep_er(er_net_ep: float, er_ssr: float, er_med: float, er_imp: float)-> tuple[float, float]:
    if er_net_ep<0:
        er_net_ep_temp=er_net_ep-er_ssr
        if er_net_ep_temp/er_med<=-1: er_ep=er_imp
        else: er_ep=((-er_net_ep_temp)/er_med)*er_imp
    else:
        er_net_ep=er_net_ep-er_ssr
        if er_net_ep<0:
            if er_net_ep/er_med<=-1: er_ep=er_imp
            else: er_ep=((-er_net_ep)/er_med)*er_imp
            er_net_ep=0
        else: er_ep=0
    return er_net_ep, er_ep

def av_stats(echo_ssr: dict, ssm: dict, char_player: Character, er_net_av: float)-> tuple[float, float]:
    er_net_av, total_av=av_er(er_net_av, echo_ssr["ER(%)"], ssm["ER(%)"], char_player.er["ER Importance"])
    for substat in echo_ssr:
        if substat!="ER(%)": total_av=total_av+((echo_ssr[substat]/ssm[substat])*char_player.rv[substat])
    return total_av, er_net_av

def ep_stats(echo_ssr: dict, ssm: dict, char_player: Character, er_net_ep: float)-> tuple[float, float]:
    rel_pot_vals=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    er_net_ep, rel_pot_vals[12]=ep_er(er_net_ep, echo_ssr["ER(%)"], ssm["ER(%)"], char_player.er["ER Importance"])
    index=0
    for substat in char_player.rv:
        rel_pot_vals[index]=char_player.rv[substat]
        index=index+1
        if index==12: break
    return sum(heapq.nlargest(5, rel_pot_vals)), er_net_ep

def ep_stats_build(echo_ssr: dict, ssm: dict, char_player: Character, er_net_ep: float)-> tuple[float, float]:
    rel_pot_vals=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    if er_net_ep<0:
        if echo_ssr["ER(%)"]>12.4:
            echo_ssr_temp=9.6
            echo_ssr["ER(%)"]=echo_ssr["ER(%)"]-9.6
        else:
            echo_ssr_temp=echo_ssr["ER(%)"]
            echo_ssr["ER(%)"]=0.0
        er_net_ep_temp=er_net_ep-echo_ssr_temp
        if er_net_ep_temp/ssm["ER(%)"]<=-1: er_ep=char_player.er["ER Importance"]
        else: er_ep=((-er_net_ep_temp)/ssm["ER(%)"])*char_player.er["ER Importance"]
    else:
        if echo_ssr["ER(%)"]>12.4:
            echo_ssr_temp=9.6
            echo_ssr["ER(%)"]=echo_ssr["ER(%)"]-9.6
        else:
            echo_ssr_temp=echo_ssr["ER(%)"]
            echo_ssr["ER(%)"]=0.0
        er_net_ep=er_net_ep-echo_ssr_temp
        if er_net_ep<0:
            if er_net_ep/ssm["ER(%)"]<=-1:
                er_ep=char_player.er["ER Importance"]
            else:
                er_ep=((-er_net_ep)/ssm["ER(%)"])*char_player.er["ER Importance"]
            er_net_ep=0
        else: er_ep=0
    rel_pot_vals[12]=er_ep
    index=0
    for substat in char_player.rv:
        rel_pot_vals[index]=char_player.rv[substat]
        index=index+1
        if index==12: break
    return sum(heapq.nlargest(5, rel_pot_vals)), er_net_ep

def es_stats(av_total: float, ep_total: float)-> float: return (av_total/ep_total)*100

def analysis(score: float, na: bool) -> str:

    if na:
        if score>=99: score_tier="Godly"
        elif score>=88: score_tier="Extreme"
        elif score>=77: score_tier="High Investment"
        elif score>=66: score_tier="Well Built"
        elif score>=55: score_tier="Decent"
        elif score>=44: score_tier="Base Level"
        else: score_tier="Unbuilt"
    else: score_tier="Not Applicable"

    return score_tier

def main(char: str, team: str, tot_er: str, ssr: list, type_in: str,
         main_stats: dict={"echo_cost": [0, 0, 0, 0, 0], "echo_mainstat": ["", "", "", "", ""]}) -> tuple[str, str]:

    char_player=Character(char, team)

    if char_player.er["Required ER"]!=0 and char_player.er["Required ER"]>100:
        er_build=float(tot_er)
        er_net=er_build-char_player.er["Required ER"]
    else: er_net=0
    if er_net>0 and er_net<=3.1: er_net=0
    if er_net>3.1: er_net-=3.1
    er_net_av=er_net
    er_net_ep=er_net

    calc_mode="N"
    ssgd=GameData(calc_mode)

    if type_in=="echo":

        echo_player=Echo(ssr)
        if char_player.er["Required ER"]<100: echo_player.ssr["ER(%)"]=0.0

        av_total, er_net_av=av_stats(echo_player.ssr, ssgd.ssm, char_player, er_net_av)
        ep_total, er_net_ep=ep_stats(echo_player.ssr, ssgd.ssm, char_player, er_net_ep)
        es_total=round(es_stats(av_total, ep_total), 3)
        es_tier=analysis(es_total, char_player.anal)

        return str(es_total), es_tier

    elif type_in=="full":

        echo_order=[]
        sanity_check=0
        for index in range(5):
            if float(ssr[index][12])!=0.0: echo_order.append(index)
            else: sanity_check+=1
        if len(echo_order)+sanity_check!=5: raise ValueError("Unexpted Error - Sanity Check Failed: "+str(echo_order)+str(sanity_check))
        for index in range(5):
            if index in echo_order: continue
            else: echo_order.append(index)
        if len(echo_order)!=5: raise ValueError("Impossible Error - What The Fuk???")

        es_total=[0.0, 0.0, 0.0, 0.0, 0.0]
        es_tier=["Unknown", "Unknown", "Unknown", "Unknown", "Unknown"]

        for echo_no in range(5):

            echo_player=Echo(ssr[echo_order[echo_no]])
            if char_player.er["Required ER"]<100: echo_player.ssr["ER(%)"]=0.0

            av_total, er_net_av=av_stats(echo_player.ssr, ssgd.ssm, char_player, er_net_av)
            ep_total, er_net_ep=ep_stats(echo_player.ssr, ssgd.ssm, char_player, er_net_ep)
            es_total[echo_order[echo_no]]=round(es_stats(av_total, ep_total), 3)
            es_tier[echo_order[echo_no]]=analysis(es_total[echo_order[echo_no]], char_player.anal)

        bs_total=round(sum(es_total)/5, 3)
        bs_tier=analysis(bs_total, char_player.anal)

        return str(bs_total)+": "+str(es_total), str(bs_tier)+": "+str(es_tier)

    elif type_in=="build":

        build_player=Build(ssr)
        if char_player.er["Required ER"]<100: build_player.build_stats["ER(%)"]=0.0

        for substat in char_player.rv:
            if char_player.rv[substat]==0.0: build_player.build_stats[substat]=0.0
        if char_player.rv["Atk(%)"]!=0.0 and char_player.rv["Flat HP"]==0.0:
            if main_stats["echo_cost"][1]==4: build_player.build_stats["Flat HP"]=2280*3+1
            else: build_player.build_stats["Flat HP"]=2280*2+1
        elif char_player.rv["HP(%)"]!=0.0 and char_player.rv["Flat Atk"]==0.0:
            if main_stats["echo_cost"][1]==4: build_player.build_stats["Flat Atk"]=150*2+1
            else: build_player.build_stats["Flat Atk"]=150+200
        elif char_player.rv["Flat HP"]==0.0 and char_player.rv["Flat Atk"]==0.0:
            if main_stats["echo_cost"][1]==4:
                build_player.build_stats["Flat HP"]=2280*3+1
                build_player.build_stats["Flat Atk"]=150*2+1
            else:
                build_player.build_stats["Flat HP"]=2280*2
                build_player.build_stats["Flat Atk"]=150+200

        for echo_num in range(5):
            cur_echo_cost=main_stats["echo_cost"][echo_num]
            cur_echo_stat=main_stats["echo_mainstat"][echo_num]
            cur_mainstat_val=GameData.mainstat_vals[cur_echo_cost][cur_echo_stat]
            cur_secstat=GameData.sec_stats[cur_echo_cost][0]
            cur_secstat_val=GameData.sec_stats[cur_echo_cost][1]
            if cur_echo_stat!="Element(%)" and cur_echo_stat!="Heal(%)":
                build_player.build_stats[cur_echo_stat]=build_player.build_stats[cur_echo_stat]-cur_mainstat_val
                if build_player.build_stats[cur_echo_stat]<-0.00000001: raise ValueError("Data Error - Character stats were entered incorrectly. Remember that stats from Echo PRESETS are expected. Please try again. ")
            build_player.build_stats[cur_secstat]=build_player.build_stats[cur_secstat]-cur_secstat_val
            if build_player.build_stats[cur_secstat]<-0.00000001: raise ValueError("Data Error - Character stats were entered incorrectly - Remember that stats from Echo PRESETS are expected. Please try again. ")

        av_total, er_net_av=av_stats(build_player.build_stats, ssgd.ssm, char_player, er_net_av)
        ep_total_list=[0.0, 0.0, 0.0, 0.0, 0.0]
        for _ in range(5): ep_total_list[_], er_net_ep=ep_stats_build(build_player.build_stats, ssgd.ssm, char_player, er_net_ep)

        ep_total=sum(ep_total_list)
        es_total=round(es_stats(av_total, ep_total), 3)
        es_tier=analysis(es_total, char_player.anal)

        return str(es_total), es_tier

    else: return "Error: ", "Type not specified"

if __name__=="__main__":
    for char in Character.data:
        def_found=False
        for team in Character.data[char][1][0]:
            if "Default" in team: def_found=True
        if def_found==False: raise ValueError(f"Unexpected Error - Default not found for {char}")
        