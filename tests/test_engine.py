
import pytest
from evc_engine import adjust_req_er, GameData, Character, analysis, Echo, main
from evc_errors import DataMismatchError, InternalLogicError

@pytest.fixture
def valid_avg_dict(): return {
    "Crit Rate(%)": 8.4, 
    "Crit Damage(%)": 16.8, 
    "Atk(%)": 9.0, 
    "Flat Atk": 45.0, 
    "HP(%)": 9.0, 
    "Flat HP": 450.0, 
    "Def(%)": 11.35, 
    "Flat Def": 55.0, 
    "Basic(%)": 9.0, 
    "Heavy(%)": 9.0, 
    "Skill(%)": 9.0, 
    "Liberation(%)": 9.0, 
    "ER(%)": 9.6, 
}

@pytest.fixture
def valid_max_dict(): return {
    "Crit Rate(%)": 10.5, 
    "Crit Damage(%)": 21.0, 
    "Atk(%)": 11.6, 
    "Flat Atk": 60.0, 
    "HP(%)": 11.6, 
    "Flat HP": 580.0, 
    "Def(%)": 14.7, 
    "Flat Def": 70.0, 
    "Basic(%)": 11.6, 
    "Heavy(%)": 11.6, 
    "Skill(%)": 11.5, 
    "Liberation(%)": 11.6, 
    "ER(%)": 12.4, 
}

@pytest.fixture
def valid_echo_ssr_list(): return [8.1, 16.2, 0.0, 0.0, 9.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

@pytest.mark.parametrize("er_req, rc, buff_val, expected_result", [
    (200, 150, 75, 0.0), 
    (199.9, 150, 75, 0.0), 
    (202, 150, 75, 101)
])
def test_adjust_req_er(er_req, rc, buff_val, expected_result): assert adjust_req_er(er_req, rc, buff_val)==expected_result

@pytest.mark.parametrize("mode, ex_pot_list", [
    ("o", valid_avg_dict), 
    ("O", valid_max_dict), 
    ("a", valid_avg_dict), 
    ("", valid_avg_dict)
])
def test_game_data_substat_pot(mode, ex_pot_list): assert GameData(mode).ssm==ex_pot_list

@pytest.mark.parametrize("mode", [[], None, True, 0, 1, {}])
def test_invalid_game_mode(mode): 
    with pytest.raises(DataMismatchError): GameData(mode)

@pytest.mark.parametrize("char, team, rel_val", [
    ("Carlotta", "Default", [1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5*0.85, 0.0])
])
def test_char_rel_val(char, team, rel_val):
    rel_val_dict=Character(char, team).rel_val
    for ind, name in enumerate(rel_val_dict): assert rel_val_dict[name]==rel_val[ind]

@pytest.mark.parametrize("rel_val", [[0.0]*12, [0.0]*14])
def test_invalid_rel_val(rel_val):
    with pytest.raises(InternalLogicError): Character("Carlotta","Default").rel_val=rel_val

@pytest.mark.parametrize("char, team_in", [
    ("Carlotta", "Zhezhi Outro"), 
    ("Aemeath", "Default")
])
def test_char_teams(char, team_in): assert team_in in Character(char, "Default").teams

@pytest.mark.parametrize("ssr", [[0.0]*12, [0.0]*14])
def test_echo_rejects_wrong_length(ssr):
    with pytest.raises(DataMismatchError): Echo(ssr)

def test_echo_accepts_correct_length(valid_echo_ssr_list):
    result=Echo(valid_echo_ssr_list)
    assert result.ssr=={"Crit Rate(%)": 8.1, "Crit Damage(%)": 16.2, "Atk(%)": 0.0, "Flat Atk": 0.0, "HP(%)": 9.6, "Flat HP": 0.0, "Def(%)": 0.0, "Flat Def": 0.0, 
                        "Basic(%)": 0.0, "Heavy(%)": 0.0, "Skill(%)": 0.0, "Liberation(%)": 0.0, "ER(%)": 0.0}

def test_echo_six_stats():
    with pytest.raises(DataMismatchError): Echo([8.1, 16.2, 0.0, 0.0, 9.6, 0.0, 0.0, 0.0, 9.6, 0.0, 0.0, 9.6, 10.0])

def test_echo_invalid_substat(valid_echo_ssr_list):
    valid_echo_ssr_list[0]="aa"
    with pytest.raises(DataMismatchError): Echo(valid_echo_ssr_list)

def test_analysis_at_false(): assert analysis(66.000, False)=="Not Applicable"

@pytest.mark.parametrize("score, expected_tier", [
    (43.999, "Unbuilt"), 
    (44.000, "Base Level"), 
    (54.999, "Base Level"), 
    (55.000, "Decent"), 
    (65.999, "Decent"), 
    (66.000, "Well Built"), 
    (76.999, "Well Built"), 
    (77.000, "High Investment"), 
    (87.999, "High Investment"), 
    (88.000, "Extreme"), 
    (98.999, "Extreme"), 
    (99.000, "Godly")    
])
def test_analysis_boundaries(score, expected_tier): assert analysis(score, True)==expected_tier

def test_main_zero_potential():
    assert main("Suisui", "Default", "260", [0.0] * 13, "echo") == ("0.0", "Not Applicable")
