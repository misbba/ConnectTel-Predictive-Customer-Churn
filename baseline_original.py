from pathlib import Path
import csv,json,math
BASE=Path(__file__).resolve().parent
def load(name):
 with (BASE/'data'/name).open(newline='') as f:return list(csv.DictReader(f))
def save(name,rows):
 with (BASE/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

rows=load('customers.csv');train=[r for r in rows if r['split']=='train'];base=(sum(int(r['churn_30d']) for r in train)+1)/(len(train)+2);probs={}
for c in {r['contract'] for r in rows}:
 g=[r for r in train if r['contract']==c];probs[c]=(sum(int(r['churn_30d']) for r in g)+5*base)/(len(g)+5)
pred=[dict(customer_id=r['customer_id'],churn_probability=probs[r['contract']]) for r in rows];save('predictions.csv',pred);metrics={}
for split in ['validation','test']:
 g=[r for r in rows if r['split']==split];metrics[split]={'n':len(g),'churn_count':sum(int(r['churn_30d']) for r in g),'brier_score':sum((probs[r['contract']]-int(r['churn_30d']))**2 for r in g)/len(g)}
(BASE/'metrics.json').write_text(json.dumps(metrics,indent=2));print('Saved predictions.csv and metrics.json')
