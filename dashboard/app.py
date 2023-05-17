from flask import Flask, jsonify, request
from flask import render_template
import csv
import os

app = Flask(__name__)
labels = []
values = []
final_scores = []
location_data = {}
path = "/home/david/Documents/Projects/traffic/dashboard"


@app.route("/")
def get_chart_page():
    global labels, values, final_scores
    labels = []
    values = []
    final_scores = []

    with open(os.path.join(path, "scores.csv")) as f:
        csvfile = csv.DictReader(f)
        for line in csvfile:
            final_scores.append(
                [
                    float(line["Latitude"]),
                    float(line["Longitude"]),
                    float(line["Incident_Score"]) * 1000,
                ]
            )
            location_data[line["Location_ID"]] = (
                float(line["Latitude"]),
                float(line["Longitude"]),
                float(line["Incident_Score"]) * 1000,
            )
    sorted_scores = sorted(final_scores, key=lambda x: x[2], reverse=True)
    for line in sorted_scores:
        lon, lat, scr = line
        labels.append([lon, lat])
        values.append(scr)
    return render_template("index.html", values=values, labels=labels)


@app.route("/refreshData")
def refresh_graph_data():
    global labels, values
    return jsonify(sLabel=labels, sData=values)


@app.route("/updateData", methods=["POST"])
def update_data():
    global location_data, final_scores, labels, values
    if not request.form:
        return "error", 400

    received_labels = request.form["label"][1:-1].split(", ")
    received_values = request.form["data"][1:-1].split(", ")

    for i, label in enumerate(received_labels):
        for score in final_scores:
            if label[1:-1] != "":
                if (
                    score[0] == location_data[label[1:-1]][0]
                    and score[1] == location_data[label[1:-1]][1]
                ):
                    score[2] = location_data[label[1:-1]][2] + float(received_values[i])

    labels = []
    values = []

    sorted_scores = sorted(final_scores, key=lambda x: x[2], reverse=True)
    for line in sorted_scores:
        lon, lat, scr = line
        labels.append([lon, lat])
        values.append(scr)

    return "success", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
