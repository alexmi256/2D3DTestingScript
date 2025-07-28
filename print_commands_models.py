models = ["ZoeD_N",
          "ZoeD_K",
          "ZoeD_NK",
          "Any_S",
          "Any_B",
          "Any_L",
          "ZoeD_Any_N",
          "ZoeD_Any_K",
          "Any_V2_S",
          "Any_V2_B",
          "Any_V2_L",
          "Any_V2_N",
          "Any_V2_K",
          "Any_V2_N_S",
          "Any_V2_N_B",
          "Any_V2_N_L",
          "Any_V2_K_S",
          "Any_V2_K_B",
          "Any_V2_K_L",
          "Distill_Any_S",
          "Distill_Any_B",
          "Distill_Any_L",
          "DepthPro",
          "DepthPro_S",
          # These require videos, not images
          # "VDA_S",
          # "VDA_L",
          # "VDA_Metric",
          # "VDA_Stream_S",
          # "VDA_Stream_L"
]

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


print(f"\nrm run_commands.sh && nano run_commands.sh && chmod +x run_commands.sh\n")

print('source .venv/bin/activate')
for i, model in enumerate(models):
    convergence = 0.5
    divergence = 4.0
    foreground_scale = 0
    method = 'mlbw_l4s'
    mapper = 'div_2'
    # mapper = False
    edge_dilation = True
    depth_aa = True
    tta = True

    mapper_type = ''
    if mapper in METRIC_DIV_MAPPER:
        mapper_type = 'div'
    elif mapper in RELATIVE_MUL_MAPPER:
        mapper_type = 'mul'
    elif mapper in RELATIVE_SHIFT_MAPPER:
        mapper_type = 'shift'

    #command = f"python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model {model} --output ~/Downloads/images_cropped/sample/right_generated/{model}/"

    command = f"mkdir -p ~/Downloads/images_cropped/sample/right_generated/{model}/; echo \"Run {i+1}/{len(models)}\"; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence {convergence} --divergence {divergence} --foreground-scale {foreground_scale} --depth-model {model} --output ~/Downloads/images_cropped/sample/right_generated/{model}/"
    # python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/012600_L.png --synthetic-view right --yes --depth-model DepthPro_S --find-param {divergence,convergence,foreground-scale} --output ~/Downloads/images_cropped/sample/param_generated/DepthPro_S/
    if edge_dilation and 'Any' in model:
        command += f" --edge-dilation 2"
    if depth_aa:
        command += f" --depth-aa"
    if tta:
        command += f" --tta"
    if method:
        command += f" --method {method}"
    if mapper:
        command += f" --mapper {mapper}"
        if mapper_type:
            command += f" --mapper-type {mapper_type}"

    print(command)

print("""
cd /home/alex/PycharmProjects/nunifScripter/
deactivate
source .venv/bin/activate
python3 compare_models.py
""")
