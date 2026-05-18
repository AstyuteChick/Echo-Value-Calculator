
from flask import Flask, render_template, request, url_for, redirect, send_file, jsonify
from evc_engine import *

evc_app=Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")

@evc_app.route("/")
def home(): return redirect(url_for("echo"))

@evc_app.route("/echo", methods=["GET"])
def echo(): return render_template("echo.html", active_page="echo", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls)

@evc_app.route("/calcEcho", methods=["POST"])
def calc_echo():
    data=request.get_json()    
    for x in range (len(data["ssr"])): data["ssr"][x]=float(data["ssr"][x])
    
    try: 
        es, et=main(data.get("char"), data.get("team"), data.get("totEr"), data.get("ssr"), "echo")
        return jsonify({"score": es, "tier": et})
    except Exception as msg: return jsonify({"score": msg, "tier": "NA"})

@evc_app.route("/build", methods=["GET"])
def build(): return render_template("build.html", active_page="build", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls, 
                                    main_stat_data=GameData.mainstat_vals)

@evc_app.route("/calcBuild", methods=["POST"])
def calc_build():
    data=request.get_json()
    try: 
        echo_cost=data.get("echoCost")
        echo_mainstats=data.get("echoMainStats")
        es, et=main(data.get("char"), data.get("team"), data.get("totEr"), data.get("ssr"), "build", {"echo_cost": echo_cost, "echo_mainstat": echo_mainstats})
        return jsonify({"score": es, "tier": et})
    except Exception as msg: return jsonify({"score": msg, "tier": "NA"})

@evc_app.route("/full", methods=["GET"])
def full(): return render_template("full.html", active_page="full", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls)

@evc_app.route("/calcFull", methods=["POST"])
def calc_full():
    data=request.get_json()
    try: 
        es, et=main(data.get("char"), data.get("team"), data.get("totEr"), data.get("ssr"), "full")
        return jsonify({"score": es, "tier": et})
    except Exception as msg: return jsonify({"score": msg, "tier": "NA"})

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
