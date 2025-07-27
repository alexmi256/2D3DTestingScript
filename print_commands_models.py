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

print('source .venv/bin/activate')
for model in models:
    convergence = 0.5
    divergence = 4.0
    foreground_scale = 0
    method = 'mlbw_l4s'
    mapper = None
    edge_dilation = True
    depth_aa = True
    tta = True

    #command = f"python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model {model} --output ~/Downloads/images_cropped/sample/right_generated/{model}/"

    command = f"python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence {convergence} --divergence {divergence} --foreground-scale {foreground_scale} --depth-model {model} --output ~/Downloads/images_cropped/sample/right_generated/{model}/"
    # python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/012600_L.png --synthetic-view right --yes --depth-model DepthPro_S --find-param {divergence,convergence,foreground-scale} --output ~/Downloads/images_cropped/sample/param_generated/DepthPro_S/
    if edge_dilation and 'Any' in model:
        command += f" --edge-dilation 2"
    if depth_aa:
        command += f" --depth-aa"
    if tta:
        command += f" --tta"
    if method:
        command += f" --method {method}"

    print(command)

print(f"\nmkdir {' '.join(models)}")
print(f"\nrm run_commands.sh && nano run_commands.sh && chmod +x run_commands.sh")