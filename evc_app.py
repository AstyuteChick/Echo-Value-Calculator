
from flask import Flask, render_template, request, url_for, redirect, send_file, jsonify
from evc_engine import *

evc_app=Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")

@evc_app.route("/")
def home(): return redirect(url_for("echo"))

@evc_app.route("/echo", methods=["GET"])
def echo(): return render_template("echo2.html", active_page="echo", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls)

@evc_app.route("/calcEcho", methods=["POST"])
def calc_echo():
    data=request.get_json()    
    for x in range (len(data["ssr"])): data["ssr"][x]=float(data["ssr"][x])
    
    try: 
        es, et=main(data.get("char"), data.get("team"), data.get("totEr"), data.get("ssr"), "echo")
        return jsonify({"score": es, "tier": et})
    except Exception as msg: return jsonify({"score": msg, "tier": "NA"})

@evc_app.route("/build", methods=["GET"])
def build(): return render_template("build2.html", active_page="build", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls)
    # elif request.method == "POST":
    #     if request.form["change_char"]=="True": return render_template("build.html", sbs="build_b", stat_names=GameData.substat_names, char_data=Character.data, echo_score="Build Score",
    #                                                                  echo_tier="Build Tier", prev_char=request.form["char_build"], prev_er=request.form["er_tot_build"],
    #                                                                  prev_buff=request.form["buff_build"], mainstat_dict=GameData.mainstat_vals)
    #     try:
    #         if request.form["echo_setup"]=="43311":
    #             echo_costs=[4, 3, 3, 1, 1]
    #             echo_mainstats=[request.form["s1"], request.form["s2"], request.form["s3"], request.form["s4"], request.form["s5"]]
    #             es, et = main(request.form["char_build"],
    #                           request.form["buff_build"],
    #                           request.form["er_tot_build"],
    #                           [request.form["Crit Rate(%)_s"], request.form["Crit Damage(%)_s"], request.form["Atk(%)_s"], request.form["Flat Atk_s"], request.form["HP(%)_s"], request.form["Flat HP_s"],
    #                            request.form["Def(%)_s"], request.form["Flat Def_s"], request.form["Basic(%)_s"], request.form["Heavy(%)_s"], request.form["Skill(%)_s"], request.form["Liberation(%)_s"],
    #                            request.form["ER(%)_s"]],
    #                            "build",
    #                            {"echo_cost": echo_costs, "echo_mainstat": echo_mainstats})
    #         else:
    #             echo_costs=[4, 4, 1, 1, 1]
    #             echo_mainstats=[request.form["c1"], request.form["c2"], request.form["c3"], request.form["c4"], request.form["c5"]]
    #             es, et = main(request.form["char_build"],
    #                           request.form["buff_build"],
    #                           request.form["er_tot_build"],
    #                           [request.form["Crit Rate(%)_c"], request.form["Crit Damage(%)_c"], request.form["Atk(%)_c"], request.form["Flat Atk_c"], request.form["HP(%)_c"], request.form["Flat HP_c"],
    #                            request.form["Def(%)_c"], request.form["Flat Def_c"], request.form["Basic(%)_c"], request.form["Heavy(%)_c"], request.form["Skill(%)_c"], request.form["Liberation(%)_c"],
    #                            request.form["ER(%)_c"]],
    #                            "build",
    #                            {"echo_cost": echo_costs, "echo_mainstat": echo_mainstats})
    #         return render_template("build.html", sbs="build_b", stat_names=GameData.substat_names, char_data=Character.data, echo_score=es, echo_tier=et, prev_char=request.form["char_build"],
    #                                prev_er=request.form["er_tot_build"], prev_buff=request.form["buff_build"], mainstat_dict=GameData.mainstat_vals)
    #     except Exception as msg: return render_template("error.html", error_msg="Build: "+str(msg))
    # else: raise ValueError

@evc_app.route("/full", methods=["GET", "POST"])
def full():
    if request.method == "GET":
        prev_stats=[{"Crit Rate(%)": 0.0, "Crit Damage(%)": 0.0, "Atk(%)": 0.0, "Flat Atk": 0.0, "HP(%)": 0.0, "Flat HP": 0.0, "Def(%)": 0.0, "Flat Def": 0.0, "Basic(%)": 0.0, "Heavy(%)": 0.0,
                     "Skill(%)": 0.0, "Liberation(%)": 0.0, "ER(%)": 0.0},
                     {"Crit Rate(%)": 0.0, "Crit Damage(%)": 0.0, "Atk(%)": 0.0, "Flat Atk": 0.0, "HP(%)": 0.0, "Flat HP": 0.0, "Def(%)": 0.0, "Flat Def": 0.0, "Basic(%)": 0.0, "Heavy(%)": 0.0,
                     "Skill(%)": 0.0, "Liberation(%)": 0.0, "ER(%)": 0.0},
                     {"Crit Rate(%)": 0.0, "Crit Damage(%)": 0.0, "Atk(%)": 0.0, "Flat Atk": 0.0, "HP(%)": 0.0, "Flat HP": 0.0, "Def(%)": 0.0, "Flat Def": 0.0, "Basic(%)": 0.0, "Heavy(%)": 0.0,
                     "Skill(%)": 0.0, "Liberation(%)": 0.0, "ER(%)": 0.0},
                     {"Crit Rate(%)": 0.0, "Crit Damage(%)": 0.0, "Atk(%)": 0.0, "Flat Atk": 0.0, "HP(%)": 0.0, "Flat HP": 0.0, "Def(%)": 0.0, "Flat Def": 0.0, "Basic(%)": 0.0, "Heavy(%)": 0.0,
                     "Skill(%)": 0.0, "Liberation(%)": 0.0, "ER(%)": 0.0},
                     {"Crit Rate(%)": 0.0, "Crit Damage(%)": 0.0, "Atk(%)": 0.0, "Flat Atk": 0.0, "HP(%)": 0.0, "Flat HP": 0.0, "Def(%)": 0.0, "Flat Def": 0.0, "Basic(%)": 0.0, "Heavy(%)": 0.0,
                     "Skill(%)": 0.0, "Liberation(%)": 0.0, "ER(%)": 0.0}]
        return render_template("full.html", sbs="full_b", stat_names=GameData.substat_names, stat_rolls=GameData.substat_rolls, char_data=Character.data, echo_score="Your scores will be displayed here",
                               echo_tier="Your tiers will be shown here", prev_char="Carlotta", prev_er="100", prev_buff="None", stats=prev_stats)
    elif request.method == "POST":
        try:
            es, et = main(request.form["char_full"],
                          request.form["buff_full"],
                          request.form["er_tot_full"],
                          [[request.form["Crit Rate(%) 1"], request.form["Crit Damage(%) 1"], request.form["Atk(%) 1"], request.form["Flat Atk 1"], request.form["HP(%) 1"], request.form["Flat HP 1"],
                           request.form["Def(%) 1"], request.form["Flat Def 1"], request.form["Basic(%) 1"], request.form["Heavy(%) 1"], request.form["Skill(%) 1"], request.form["Liberation(%) 1"],
                           request.form["ER(%) 1"]],
                           [request.form["Crit Rate(%) 2"], request.form["Crit Damage(%) 2"], request.form["Atk(%) 2"], request.form["Flat Atk 2"], request.form["HP(%) 2"], request.form["Flat HP 2"],
                           request.form["Def(%) 2"], request.form["Flat Def 2"], request.form["Basic(%) 2"], request.form["Heavy(%) 2"], request.form["Skill(%) 2"], request.form["Liberation(%) 2"],
                           request.form["ER(%) 2"]],
                           [request.form["Crit Rate(%) 3"], request.form["Crit Damage(%) 3"], request.form["Atk(%) 3"], request.form["Flat Atk 3"], request.form["HP(%) 3"], request.form["Flat HP 3"],
                           request.form["Def(%) 3"], request.form["Flat Def 3"], request.form["Basic(%) 3"], request.form["Heavy(%) 3"], request.form["Skill(%) 3"], request.form["Liberation(%) 3"],
                           request.form["ER(%) 3"]],
                           [request.form["Crit Rate(%) 4"], request.form["Crit Damage(%) 4"], request.form["Atk(%) 4"], request.form["Flat Atk 4"], request.form["HP(%) 4"], request.form["Flat HP 4"],
                           request.form["Def(%) 4"], request.form["Flat Def 4"], request.form["Basic(%) 4"], request.form["Heavy(%) 4"], request.form["Skill(%) 4"], request.form["Liberation(%) 4"],
                           request.form["ER(%) 4"]],
                           [request.form["Crit Rate(%) 5"], request.form["Crit Damage(%) 5"], request.form["Atk(%) 5"], request.form["Flat Atk 5"], request.form["HP(%) 5"], request.form["Flat HP 5"],
                           request.form["Def(%) 5"], request.form["Flat Def 5"], request.form["Basic(%) 5"], request.form["Heavy(%) 5"], request.form["Skill(%) 5"], request.form["Liberation(%) 5"],
                           request.form["ER(%) 5"]]],
                           "full")
            prev_stats=[{"Crit Rate(%)": request.form["Crit Rate(%) 1"], "Crit Damage(%)": request.form["Crit Damage(%) 1"], "Atk(%)": request.form["Atk(%) 1"],
                         "Flat Atk": request.form["Flat Atk 1"], "HP(%)": request.form["HP(%) 1"], "Flat HP": request.form["Flat HP 1"], "Def(%)": request.form["Def(%) 1"],
                         "Flat Def": request.form["Flat Def 1"], "Basic(%)": request.form["Basic(%) 1"], "Heavy(%)": request.form["Heavy(%) 1"], "Skill(%)": request.form["Skill(%) 1"],
                         "Liberation(%)": request.form["Liberation(%) 1"], "ER(%)": request.form["ER(%) 1"]},
                         {"Crit Rate(%)": request.form["Crit Rate(%) 2"], "Crit Damage(%)": request.form["Crit Damage(%) 2"], "Atk(%)": request.form["Atk(%) 2"],
                         "Flat Atk": request.form["Flat Atk 2"], "HP(%)": request.form["HP(%) 2"], "Flat HP": request.form["Flat HP 2"], "Def(%)": request.form["Def(%) 2"],
                         "Flat Def": request.form["Flat Def 2"], "Basic(%)": request.form["Basic(%) 2"], "Heavy(%)": request.form["Heavy(%) 2"], "Skill(%)": request.form["Skill(%) 2"],
                         "Liberation(%)": request.form["Liberation(%) 2"], "ER(%)": request.form["ER(%) 2"]},
                         {"Crit Rate(%)": request.form["Crit Rate(%) 3"], "Crit Damage(%)": request.form["Crit Damage(%) 3"], "Atk(%)": request.form["Atk(%) 3"],
                         "Flat Atk": request.form["Flat Atk 3"], "HP(%)": request.form["HP(%) 3"], "Flat HP": request.form["Flat HP 3"], "Def(%)": request.form["Def(%) 3"],
                         "Flat Def": request.form["Flat Def 3"], "Basic(%)": request.form["Basic(%) 3"], "Heavy(%)": request.form["Heavy(%) 3"], "Skill(%)": request.form["Skill(%) 3"],
                         "Liberation(%)": request.form["Liberation(%) 3"], "ER(%)": request.form["ER(%) 3"]},
                         {"Crit Rate(%)": request.form["Crit Rate(%) 4"], "Crit Damage(%)": request.form["Crit Damage(%) 4"], "Atk(%)": request.form["Atk(%) 4"],
                         "Flat Atk": request.form["Flat Atk 4"], "HP(%)": request.form["HP(%) 4"], "Flat HP": request.form["Flat HP 4"], "Def(%)": request.form["Def(%) 4"],
                         "Flat Def": request.form["Flat Def 4"], "Basic(%)": request.form["Basic(%) 4"], "Heavy(%)": request.form["Heavy(%) 4"], "Skill(%)": request.form["Skill(%) 4"],
                         "Liberation(%)": request.form["Liberation(%) 4"], "ER(%)": request.form["ER(%) 4"]},
                         {"Crit Rate(%)": request.form["Crit Rate(%) 5"], "Crit Damage(%)": request.form["Crit Damage(%) 5"], "Atk(%)": request.form["Atk(%) 5"],
                         "Flat Atk": request.form["Flat Atk 5"], "HP(%)": request.form["HP(%) 5"], "Flat HP": request.form["Flat HP 5"], "Def(%)": request.form["Def(%) 5"],
                         "Flat Def": request.form["Flat Def 5"], "Basic(%)": request.form["Basic(%) 5"], "Heavy(%)": request.form["Heavy(%) 5"], "Skill(%)": request.form["Skill(%) 5"],
                         "Liberation(%)": request.form["Liberation(%) 5"], "ER(%)": request.form["ER(%) 5"]}]
            return render_template("full.html", sbs="full_b", stat_names=GameData.substat_names, stat_rolls=GameData.substat_rolls, char_data=Character.data, echo_score=es, echo_tier=et,
                                   prev_char=request.form["char_full"], prev_er=request.form["er_tot_full"], prev_buff=request.form["buff_full"], stats=prev_stats)
        except Exception as msg: return render_template("error.html", error_msg="Full: "+str(msg))
    else: raise ValueError

@evc_app.route("/instruct")
def instruct():
    return render_template("instruct.html", sbs="inst_b")

@evc_app.route("/logs")
def logs():
    return render_template("logs.html", sbs="logs_b")

@evc_app.route("/reports")
def reports():
    return render_template("reports.html", sbs="reports_b")

@evc_app.route("/about")
def about():
    return render_template("about.html", sbs="about_b")

@evc_app.route("/articles")
def contents():
    return render_template("contents.html", sbs="articles_b")

@evc_app.route("/goals")
def goals():
    return render_template("goals.html", sbs="articles_b")

@evc_app.route("/assumptions")
def assumptions():
    return render_template("assumptions.html", sbs="articles_b")

@evc_app.route("/cd")
def cd():
    return render_template("cd.html", sbs="articles_b", char_data=Character.data)

@evc_app.route("/clg")
def clg():
    return render_template("clg.html", sbs="articles_b")

@evc_app.route("/co")
def co():
    return render_template("co.html", sbs="articles_b")

@evc_app.route("/av")
def av():
    return render_template("av.html", sbs="articles_b")

@evc_app.route("/pv")
def pv():
    return render_template("pv.html", sbs="articles_b")

@evc_app.route("/esbs")
def esbs():
    return render_template("esbs.html", sbs="articles_b")

@evc_app.route("/er")
def er():
    return render_template("er.html", sbs="articles_b")

@evc_app.route("/cre")
def cre():
    return render_template("cre.html", sbs="articles_b")

@evc_app.route("/rc")
def rc():
    return render_template("rc.html", sbs="articles_b")

@evc_app.route("/sc")
def sc():
    return render_template("sc.html", sbs="articles_b")

@evc_app.route("/privacy")
def privacy():
    return render_template("privacy.html", sbs="privacy_b")

@evc_app.route("/terms")
def terms():
    return render_template("terms.html", sbs="terms_b")

@evc_app.route("/ads.txt")
def ads_txt():
    return redirect("https://srv.adstxtmanager.com/79141/echovaluecalc.com", code=301)

@evc_app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")


if __name__ == "__main__": evc_app.run(debug=True)
