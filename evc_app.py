
from flask import Flask, render_template, request, url_for, redirect, send_file, jsonify, send_from_directory
from werkzeug.exceptions import BadRequest
from evc_engine import GameData, Character, main
from evc_errors import InvalidInputError, DataMismatchError

evc_app=Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")

def validate_common_data(data): 
    if not isinstance(data, dict) or len(data)!=4: raise DataMismatchError("request is not a valid data dictionary")
    try: 
        if not isinstance(data["char"], str): raise DataMismatchError("character name must be a string")
        if not isinstance(data["team"], str): raise DataMismatchError("team name must be a string")
        if not isinstance(data["totEr"], (int, float)) or isinstance(data["totEr"], bool): raise DataMismatchError("total er must be a number")
        if not isinstance(echo, list): raise DataMismatchError("ssr data must be a valid list")
    except KeyError as msg: raise DataMismatchError(f"key not found: {msg}")
    if data["char"] not in Character.data: raise DataMismatchError("character name not recognized")
    if data["team"] not in Character.data[data["char"]][1][0]: raise DataMismatchError("character team not recognized")
    if data["totEr"]<100 and Character.data[data["char"]][1][0][data["team"]]>100 and Character.data[data["char"]][1][1]!=0: raise InvalidInputError("please enter character's total ER")

def validate_echo_data(echo):
    if len(echo)!=13: raise DataMismatchError(f"echo must have 13 fields, not {len(echo)}")
    for i, ssr in enumerate(echo): 
        if isinstance(ssr, bool): raise DataMismatchError("substat roll cannot be a bool (please stop messing around!)")
        try: ssr_val=float(ssr)
        except (TypeError, ValueError): raise DataMismatchError(f"couldn't covert substat roll to float: {ssr}")
        if ssr_val!=0 and ssr_val not in GameData.substat_rolls[GameData.substat_names[i]]: raise DataMismatchError(f"invalid roll value for {GameData.substat_names[i]}: {ssr_val}")
        echo[i]=ssr_val
    ssr_counter=0
    for ssr in echo: 
        if ssr!=0: ssr_counter+=1
    if ssr_counter>5: raise DataMismatchError(f"too many substats: {ssr_counter}")

def validate_build_data(preset_vals): 
    if len(preset_vals)!=13: raise DataMismatchError(f"build must have 13 fields, not {len(preset_vals)}")
    for i, ssr in enumerate(preset_vals):
        if isinstance(ssr, bool): raise DataMismatchError("preset values cannot be bools (ha you think you got me)")
        try: ssr_val=float(ssr)
        except (TypeError, ValueError): raise DataMismatchError(f"coudln't covert substat roll to float: {ssr}")
    preset_vals[i]=ssr_val

def validate_full_data(full_build):
    if len(full_build)!=5: raise DataMismatchError(f"Build must have 5 Echoes, not {len(full_build)}")
    for echo in full_build: 
        if not isinstance(echo, list): raise DataMismatchError("substat rolls must be a valid list")
        validate_echo_data(echo)

@evc_app.route("/")
def home(): return redirect(url_for("echo"))

@evc_app.route("/echo", methods=["GET"])
def echo(): return render_template("echo.html", active_page="echo", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls,
                                   canon_ulr="https://www.echovaluecalc.com/echo")

@evc_app.route("/calcEcho", methods=["POST"])
def calc_echo():
    try:
        if not request.is_json: return jsonify({"error": "Request didn't send json", "code": "unsupported_media"}), 415
        data=request.get_json()
        validate_common_data(data)
        validate_echo_data(data["ssr"])
        es, et=main(data["char"], data["team"], data["totEr"], data["ssr"], "echo")
        return jsonify({"score": es, "tier": et}), 200
    except BadRequest as msg: 
        evc_app.logger.warning(str(msg))
        return jsonify({"error": "Request body contains invalid json", "code": "invalid_json"}), 400
    except InvalidInputError as msg: return jsonify({"error": str(msg), "code": "invalid_input"}), 400
    except DataMismatchError as msg: 
        evc_app.logger.warning(str(msg))
        return (jsonify({"error": "Data doesn't match the contract", "code": "invalid_request"})), 400
    except Exception as msg: 
        evc_app.logger.exception(str(msg))
        return jsonify({"error": "Something went wrong", "code": "internal_error"}), 500

@evc_app.route("/build", methods=["GET"])
def build(): return render_template("build.html", active_page="build", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls,
                                    main_stat_data=GameData.mainstat_vals, canon_ulr="https://www.echovaluecalc.com/build")

@evc_app.route("/calcBuild", methods=["POST"])
def calc_build():
    try:
        if not request.is_json: return jsonify({"error": "Request didn't send json", "code": "unsupported_media"}), 415
        data=request.get_json()
        validate_common_data(data)
        validate_build_data(data["ssr"])
        echo_cost=data.get("echoCost")
        echo_mainstats=data.get("echoMainStats")
        es, et=main(data.get("char"), data.get("team"), data.get("totEr"), data.get("ssr"), "build", {"echo_cost": echo_cost, "echo_mainstat": echo_mainstats})
        return jsonify({"score": es, "tier": et}), 200
    except BadRequest as msg: 
        evc_app.logger.warning(str(msg))
        return jsonify({"error": "Request body contains invalid json", "code": "invalid_json"}), 400
    except InvalidInputError as msg: return jsonify({"error": str(msg), "code": "invalid_input"}), 400
    except DataMismatchError as msg: 
        evc_app.logger.warning(str(msg))
        return (jsonify({"error": "Data doesn't match the contract", "code": "invalid_request"})), 400
    except Exception as msg: 
        evc_app.logger.exception(str(msg))
        return jsonify({"error": "Something went wrong", "code": "internal_error"}), 500

@evc_app.route("/full", methods=["GET"])
def full(): return render_template("full.html", active_page="full", char_data=Character.data, prev_char="Aemeath", echo_data=GameData.substat_names, substat_rolls=GameData.substat_rolls,
                                   canon_ulr="https://www.echovaluecalc.com/full")

@evc_app.route("/calcFull", methods=["POST"])
def calc_full():
    try:
        if not request.is_json: return jsonify({"error": "Request didn't send json", "code": "unsupported_media"}), 415
        data=request.get_json()
        validate_common_data(data)
        validate_full_data(data["ssr"])
        es, et=main(data.get("char"), data.get("team"), data.get("totEr"), data.get("ssr"), "full")
        return jsonify({"score": es, "tier": et}), 200
    except BadRequest as msg: 
        evc_app.logger.warning(str(msg))
        return jsonify({"error": "Request body contains invalid json", "code": "invalid_json"}), 400
    except InvalidInputError as msg: return jsonify({"error": str(msg), "code": "invalid_input"}), 400
    except DataMismatchError as msg: 
        evc_app.logger.warning(str(msg))
        return (jsonify({"error": "Data doesn't match the contract", "code": "invalid_request"})), 400
    except Exception as msg: 
        evc_app.logger.exception(str(msg))
        return jsonify({"error": "Something went wrong", "code": "internal_error"}), 500

@evc_app.route("/instruct")
def instruct():
    return render_template("instruct.html", active_page="inst", canon_ulr="https://www.echovaluecalc.com/instruct")

@evc_app.route("/logs")
def logs():
    return render_template("logs.html", active_page="logs", canon_ulr="https://www.echovaluecalc.com/logs")

@evc_app.route("/reports")
def reports():
    return render_template("reports.html", active_page="reps", canon_ulr="https://www.echovaluecalc.com/reports")

@evc_app.route("/about")
def about():
    return render_template("about.html", active_page="abt", canon_ulr="https://www.echovaluecalc.com/about")

@evc_app.route("/articles")
def contents():
    return render_template("contents.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/articles")

@evc_app.route("/goals")
def goals():
    return render_template("goals.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/goals")

@evc_app.route("/assumptions")
def assumptions():
    return render_template("assumptions.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/assumptions")

@evc_app.route("/cd")
def cd():
    return render_template("cd.html", active_page="arts", char_data=Character.data, canon_ulr="https://www.echovaluecalc.com/cd")

@evc_app.route("/clg")
def clg():
    return render_template("clg.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/clg")

@evc_app.route("/co")
def co():
    return render_template("co.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/co")

@evc_app.route("/av")
def av():
    return render_template("av.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/av")

@evc_app.route("/pv")
def pv():
    return render_template("pv.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/pv")

@evc_app.route("/esbs")
def esbs():
    return render_template("esbs.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/esbs")

@evc_app.route("/er")
def er():
    return render_template("er.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/er")

@evc_app.route("/cre")
def cre():
    return render_template("cre.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/cre")

@evc_app.route("/rc")
def rc():
    return render_template("rc.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/rc")

@evc_app.route("/sc")
def sc():
    return render_template("sc.html", active_page="arts", canon_ulr="https://www.echovaluecalc.com/sc")

@evc_app.route("/privacy")
def privacy():
    return render_template("privacy.html", active_page="noVal", canon_ulr="https://www.echovaluecalc.com/privacy")

@evc_app.route("/terms")
def terms():
    return render_template("terms.html", active_page="noVal", canon_ulr="https://www.echovaluecalc.com/terms")

@evc_app.route("/ads.txt")
def ads_txt():
    return redirect("https://srv.adstxtmanager.com/79141/echovaluecalc.com", code=301)

@evc_app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")

@evc_app.route("/robots.txt")
def robots(): 
    static_folder=evc_app.static_folder
    assert static_folder is not None
    return send_from_directory(static_folder, "robots.txt", mimetype="text/plain")

if __name__ == "__main__": evc_app.run(debug=True)
