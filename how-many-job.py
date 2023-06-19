import json
with open ('all_jobs_HH.RU.json', encoding='utf-8') as f:
    data = json.load(f)
print(len(data))