methods = [
    # "grid_sample",
    "backward",
    "forward",
    "forward_fill",
    "mlbw_l2",
    "mlbw_l4",
    "mlbw_l2s",
    "mlbw_l4s",
    "row_flow",
    "row_flow_sym",
    "row_flow_v3",
    "row_flow_v3_sym",
    "row_flow_v2"
]

print('source .venv/bin/activate')
for i, method in enumerate(methods):
    model = 'ZoeD_Any_N'
    convergence = 0.2
    divergence = 1.0
    foreground_scale = 0
    edge_dilation = False
    depth_aa = False
    tta = False

    command = f"mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/{method}/; echo \"Run {i+1}/{len(methods)}\"; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model {model} --method {method} --output ~/Downloads/images_cropped/sample/right_generated_method/{method}/"
    if edge_dilation and 'Any' in model:
        command += f" --edge-dilation 2"
    if depth_aa:
        command += f" --depth-aa"
    if tta:
        command += f" --tta"

    print(command)

print(f"\nmkdir {' '.join(methods)}")
print(f"\nrm run_commands.sh && nano run_commands.sh && chmod +x run_commands.sh")
