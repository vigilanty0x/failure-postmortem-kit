import argparse,hashlib,json
def build(data):
 req=("incident","impact","timeline","evidence","causes","actions");missing=[x for x in req if not data.get(x)] if isinstance(data,dict) else list(req)
 if missing:return {"ok":False,"missing":missing}
 if any(not isinstance(data[x],list) or not data[x] for x in ("timeline","evidence","causes","actions")):return {"ok":False,"missing":["non_empty_lists"]}
 if any(not isinstance(a,dict) or not all(a.get(k) for k in ("owner","due","action")) for a in data["actions"]):return {"ok":False,"missing":["action_accountability"]}
 sections=["# Postmortem: "+data["incident"],"## Impact",data["impact"],"## Timeline"]+[f"- {x}" for x in data["timeline"]]+["## Evidence"]+[f"- {x}" for x in data["evidence"]]+["## Causes"]+[f"- {x}" for x in data["causes"]]+["## Actions"]+[f"- {a['action']} — {a['owner']} — {a['due']}" for a in data["actions"]];body="\n".join(sections);return {"ok":True,"markdown":body,"sha256":hashlib.sha256(body.encode()).hexdigest()}
def probe():
 g=build({"incident":"demo","impact":"none","timeline":["t"],"evidence":["e"],"causes":["c"],"actions":[{"owner":"o","due":"later","action":"a"}]});b=build({"incident":"demo"});return {"ok":g["ok"] and not b["ok"],"incomplete_counter_proof":not b["ok"]}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("command",choices=("build","probe"));p.add_argument("--input");a=p.parse_args(argv);o=probe() if a.command=="probe" else build(json.load(open(a.input)));print(json.dumps(o,sort_keys=True));return 0 if o["ok"] else 2
