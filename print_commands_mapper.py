# https://github.com/nagadomi/nunif/blob/master/iw3/mapper.py#L147C1-L164C101
METRIC_DIV_MAPPER = [
    "none",
    "div_25",
    "div_10",
    "div_6",
    "div_4",
    "div_2",
    "div_1",
]
RELATIVE_MUL_MAPPER = [
    "inv_mul_3",
    "inv_mul_2",
    "inv_mul_1",
    "none",
    "mul_1",
    "mul_2",
    "mul_3",
]
RELATIVE_SHIFT_MAPPER = [
    "shift_045",
    "shift_06",
    "shift_08",
    "none",
    "shift_14",
    "shift_20",
    "shift_30",
]

LEGACY_MAPPER = [
    "pow2",
    "softplus",
    "softplus2"
]
MAPPER_ALL = ["auto"] + list(dict.fromkeys(LEGACY_MAPPER + RELATIVE_MUL_MAPPER + METRIC_DIV_MAPPER))

print(f"\nrm run_commands.sh && nano run_commands.sh && chmod +x run_commands.sh\n")
print('source .venv/bin/activate')
for mapper in list(set(MAPPER_ALL + RELATIVE_SHIFT_MAPPER)):
    model = 'Any_B'
    convergence = 0.5
    divergence = 4.0
    foreground_scale = 0
    edge_dilation = False
    depth_aa = False
    tta = False

    mapper_type = ''
    if mapper in METRIC_DIV_MAPPER:
        mapper_type = 'div'
    elif mapper in RELATIVE_MUL_MAPPER:
        mapper_type = 'mul'
    elif mapper in RELATIVE_SHIFT_MAPPER:
        mapper_type = 'shift'

    command = f"mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/{mapper}; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model {model} --mapper {mapper} --output ~/Downloads/images_cropped/sample/mapper_generated/{mapper}/ --convergence {convergence} --divergence {divergence} --foreground-scale {foreground_scale} --depth-model {model}"
    if mapper_type:
        command += f" --mapper-type {mapper_type}"
    if edge_dilation and 'Any' in model:
        command += f" --edge-dilation 2"
    if depth_aa:
        command += f" --depth-aa"
    if tta:
        command += f" --tta"

    print(command)


print("""
cd /home/alex/PycharmProjects/nunifScripter/
deactivate
source .venv/bin/activate
python3 compare_mapper.py
""")
