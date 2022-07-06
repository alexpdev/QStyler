import json

a = json.load(open("data.json"))


data = {}




def get_data(a, widget):
    props = []
    controls = []
    for row in a:
        if "prop" in row:
            if widget in row["options"]:
                props.append(row["prop"])
        if "control" in row:
            if widget in row["widgets"]:
                controls.append(row["control"])
    return {"props": props, "controls": controls}

def compile(a):
    seq = []
    for row in a:
        if "name" in row:
            widget = row["name"][0]
            info = get_data(a, widget)
            for item in row["controls"]:
                if item not in info["controls"] and "Customizing" not in item:
                    info["controls"].append(item)
            seq.append({widget: info})
    return seq

seq = compile(a)

print(seq)
json.dump(seq,open("data2.json","tw"), indent=4)
