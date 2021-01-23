import pandas as pd
file_name = 'short.vcf'
export_file_name = 'export.vcf'

df = pd.read_csv(file_name, delimiter='\t', comment='#', index_col='ID')

def str2dict(s):
    kv_pairs = s.split(';')
    res = {}
    for kv in kv_pairs:
        _kv = kv.split('=')
        if(len(_kv))==2:
            res[_kv[0]] = _kv[1]
    return res
infos = df['INFO'].map(lambda s: str2dict(s))

AFs = infos.map(lambda x: x['AF'] if 'AF' in x else None)
df['AF'] = AFs

# read comment
comments = []
with open(file_name, mode='r') as f:
    while True:
        current_line = f.readline()
        if not current_line.startswith("##"):
            break
        comments.append(current_line)

with open(export_file_name, mode='w') as f:
    f.writelines(comments)
    df.to_csv(f, mode='a', index=False, sep='\t')
