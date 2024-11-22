# _*_ coding:utf-8 _*_

import pandas as pd
import numpy as np

# 提供文件路径（您上传的文件名）
file_path = '/mnt/data/results.csv'  # 替换为您的文件路径

# 使用 pandas 读取 CSV 文件
df = pd.read_csv(file_path)

def get_value(df, model, attack, defense):
    """
    获取特定模型、攻击和防御的 CA, ASR 和 RA 值。
    """
    row_value = df[(df['backbone'] == model) & (df['attack_name'] == attack) & (df['defense_name'] == defense)]
    if row_value.empty:
        return 'NA', 'NA', 'NA'

    # Retrieve test_acc, test_asr, and test_ra
    ca = row_value['test_acc'].iloc[0] * 100 if not pd.isna(row_value['test_acc'].iloc[0]) else 'NA'
    asr = row_value['test_asr'].iloc[0] * 100 if not pd.isna(row_value['test_asr'].iloc[0]) else 'NA'
    rc = row_value['test_ra'].iloc[0] * 100 if not pd.isna(row_value['test_ra'].iloc[0]) else 'NA'

    return round(ca, 2) if isinstance(ca, float) else ca, \
           round(asr, 2) if isinstance(asr, float) else asr, \
           round(rc, 2) if isinstance(rc, float) else rc

# 定义数据集、比例和其他参数
datasets = df['dataset'].unique()
ratios = df['ratio'].unique()
backbones = df['backbone'].unique()
attacks = df['attack_name'].unique()
defenses = df['defense_name'].unique()

# 映射模型、攻击和防御名称
models2name = {
    'preactresnet18': 'PreAct-Resnet18', 
    'vgg19': 'VGG19', 
    "efficientnet_b3": 'EfficientNet-B3',
    "mobilenet_v3_large": 'MobileNetV3-Large', 
    "densenet161": 'DenseNet-161'
}
attacks2name = {
    'badnet': 'BadNets', 
    'blended': 'Blended', 
    'lc': 'LC', 
    'sig': 'SIG', 
    'lf': 'LF', 
    'ssba': 'SSBA', 
    'inputaware': 'Input-aware', 
    'wanet': 'WaNet'
}
defenses2name = {
    'no defense': 'No defense', 
    'ft': 'FT', 
    "fp": 'FP', 
    'nad': 'NAD',
    'nc': 'NC', 
    'anp': 'ANP', 
    'ac': 'AC', 
    'spectral': 'Spectral', 
    'abl': 'ABL', 
    'dbd': 'DBD'
}

# 生成 HTML 表格
def generate_table(dataset, ratio):
    """
    生成 HTML 表格并保存为文件。
    """
    output_file = f'{dataset}_{ratio * 100: .1f}.html'

    # 表头
    head = """<div class="tab-pane fade show active" id="{}-{}" role="tabpanel" aria-labelledby="{}-{}-tab">
    <div style="overflow: auto; width: 100%;">
        <table style="overflow: auto; width: 100%;" class="table table-hover sortable performanceTableWide">
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Attack</th>
    """.format(dataset, ratio * 100, dataset, ratio * 100)

    # 添加防御方法作为表头
    for defense in defenses:
        head += f"<th>{defenses2name.get(defense, defense)} CA</th>"
        head += f"<th>{defenses2name.get(defense, defense)} ASR</th>"
        head += f"<th>{defenses2name.get(defense, defense)} RA</th>"
    head += "</tr></thead><tbody>"

    rows = ""
    # 筛选特定数据集和比例的数据
    filtered_data = df[(df['dataset'] == dataset) & (df['ratio'] == ratio)]

    for model in backbones:
        for attack in attacks:
            row = f"<tr><td>{models2name.get(model, model)}</td><td>{attacks2name.get(attack, attack)}</td>"
            for defense in defenses:
                ca, asr, rc = get_value(filtered_data, model, attack, defense)
                row += f"<td>{ca}</td><td>{asr}</td><td>{rc}</td>"
            row += "</tr>"
            rows += row

    tail = "</tbody></table></div></div>"

    # 拼接表头、行和表尾
    html_content = head + rows + tail

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated: {output_file}")

# 为所有数据集和比例生成表格
for dataset in datasets:
    for ratio in ratios:
        generate_table(dataset, ratio)
