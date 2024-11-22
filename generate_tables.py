
# _*_ coding:utf-8 _*_

import pandas as pd

import numbers

import numpy as np

def get_value(df, model,attack,defense):
    df = df.replace('TBD',np.nan)
    row_value = df[(df['Attack'] == model) & (df['Model'] == attack)]
    loc = row_value.index.tolist()
    asr = row_value.loc[loc, '{} asr'.format(defense)]
    ca = row_value.loc[loc, '{} ca'.format(defense)]
    rc =row_value.loc[loc, '{} rc'.format(defense)]


    if pd.isna(ca.item()):
        ca='NA'
    else:
        ca=round(float(ca.item())*100,2)
    

    if pd.isna(asr.item()):         
        asr='NA'     
    else:         
        asr=round(float(asr.item())*100,2)

    if pd.isna(rc.item()):         
        rc='NA'     
    else:         
        rc=round(float(rc.item())*100,2)
    
    return ca,asr,rc

   

path='tables/results.csv'
datasets=['GTSRB','CIFAR100','tiny']
pratios=['10%','5%','1%','0.5%','0.1%']

all_backbones = ['preactresnet18', 'vgg19', "efficientnet_b3", "mobilenet_v3_large", "densenet161"]
all_attacks = ['badnet', 'blended', 'lc','sig','lf' ,'ssba', 'inputaware','wanet']
all_defenses = ['no defense', 'ft','fp','nad', 'nc','anp', 'ac', 'spectral','abl','dbd']

models2name={'preactresnet18':'PreAct-Resnet18','vgg19':'VGG19','efficientnet_b3':'EfficientNet-B3',"mobilenet_v3_large":'MobileNetV3-Large',"densenet161":'DenseNet-161'}
attacks2name = {'badnet':'BadNets', 'blended':'Blended','lc':'LC','sig':'SIG', 'lf':'LF', 'ssba':'SSBA', 'inputaware':'Input-aware', 'wanet':'WaNet'}
defenses2name = {'no defense':'No defense', 'ft':'FT',"fp": 'FP', 'nad':'NAD','nc':'NC','anp':'ANP','ac':'AC', 'spectral':'Spectral', 'abl':'ABL', 'dbd':'DBD'}

def generate_table(dataset,pratio):

    output_file=f'tables/{dataset}_{pratio}.txt'

    with open('tables\head.txt','r',encoding='UTF-8') as f:
        head=f.read()

    with open('tables\\tail.txt','r',encoding='UTF-8') as f:
        tail=f.read()

    with open(output_file,'w+') as f:
        f.write(head)

    sheet_name=f'{dataset}-{pratio}'
    df= pd.read_excel(path, sheet_name=sheet_name)


    for model in all_backbones:
        for attack in all_attacks:
            with open(output_file,'a') as f:
                f.write('<tr>')
            item=f'<td>{models2name[model]}</td> <td>{attacks2name[attack]}</td>'
            for defense in all_defenses:
                cacc,asr,racc=get_value(df, model,attack,defense)
                item+=f'<td>{cacc}</td>'
                item+=f'<td>{asr}</td>'
                item+=f'<td>{racc}</td>'
            item=item+'</tr>'
            with open(output_file,'a') as f:
                f.write(item)

    with open(output_file,'a') as f:
        f.write(tail) 


    print(f'{dataset}, {pratio} success')    
            

for dataset in datasets:
    for pratio in pratios:
        generate_table(dataset,pratio)