# Scripts for testing 2D to 3D image generation
Data used was from live indoor 3D video keyframes and cannot be shared
Comparisons were performed using [imgcompare](https://github.com/datenhahn/imgcompare) RGB images

# TL;DR
For right image only synthetic view:
- Use `--model ZoeD_Any_N --edge-dilation --depth-aa --convergence 0.5 --divergence 4.0 --method mlbw_l4s` for almost best in class generation and performance
- Use `--model DepthPro_S --edge-dilation --depth-aa --convergence 0.5 --divergence 4.0 --method mlbw_l4s --tta` for best in class generation but 4x slower performance

# Summary
- `DepthPro_S` seems to be the best model even though it's smaller than `DepthPro`
- `DepthPro_S` is ~2x slower compared to other models while `DepthPro` is ~4x slower
- `--edge-dilation` for `Any` models doesn't matter much
- `--depth-aa` doesn't matter much
- `--tta` doesn't matter much, marginal improvement
- `--divergence` and `--convergence` do seem to make a slight difference in right frame generation
- `--foreground-scale` either does nothing or is only applicable in certain conditions
- These score likely don't mean much
  - A 5% difference between ground truth and generated may actually be a lot. gt right vs gt left difference is ~7.021% 
  - While I finetuned parameters for "right frame only" generation, `iw3` uses both frame generation by default so these fine tuned settings may be invalid with that mode which I believed may result in better generation
  - Ideally I'd be able to generate a depth map from L and R frames and compare that against iw3 generated map. This proves to be difficult in that all examples I've seen of this generate messy maps which could not be compared against the iw3 maps.
- VideoDepthAnything was not tested

# Setup
```
../images_cropped/
├── images_cropped
│   ├── left
│   └── right
└── sample
    ├── left
    ├── param_generated
    │   ├── 001000_R
....
    │   └── 107400_R
    ├── right
    ├── right_generated
    │   ├── Any_B
....
    │   └── ZoeD_NK
    └── right_generated_method
        ├── backward
        ├── forward
        ├── forward_fill
        ├── grid_sample
        ├── mlbw_l2
        ├── mlbw_l2s
        ├── mlbw_l4
        ├── mlbw_l4s
        ├── row_flow
        ├── row_flow_sym
        ├── row_flow_v2
        ├── row_flow_v3
        └── row_flow_v3_sym

```
- `images_cropped` contains ALL ground truth images sorted into `left` and `right` frames
- `sample` contains a subset of the images
  - `left` contains a subset of the left ground truth frames
  - `right` contains a subset of the right ground truth frames
  - `right_generated` contains generated right frame images sorted by models' directory
  - `param_generated` contains generated right frame images with the `--find-params` option, this one is weird because input is only one image and not a `dir`

# Scripts
## print_commands_models.py
Prints `nunif iw3.cli`  commands to generate the right sample images for all models and user set params
```sh
source .venv/bin/activate
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model ZoeD_N --output ~/Downloads/images_cropped/sample/right_generated/ZoeD_N/ --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model ZoeD_K --output ~/Downloads/images_cropped/sample/right_generated/ZoeD_K/ --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model ZoeD_NK --output ~/Downloads/images_cropped/sample/right_generated/ZoeD_NK/ --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_S --output ~/Downloads/images_cropped/sample/right_generated/Any_S/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_B --output ~/Downloads/images_cropped/sample/right_generated/Any_B/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_L --output ~/Downloads/images_cropped/sample/right_generated/Any_L/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model ZoeD_Any_N --output ~/Downloads/images_cropped/sample/right_generated/ZoeD_Any_N/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model ZoeD_Any_K --output ~/Downloads/images_cropped/sample/right_generated/ZoeD_Any_K/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_S --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_S/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_B --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_B/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_L --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_L/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_N --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_N/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_K --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_K/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_N_S --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_N_S/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_N_B --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_N_B/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_N_L --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_N_L/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_K_S --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_K_S/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_K_B --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_K_B/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Any_V2_K_L --output ~/Downloads/images_cropped/sample/right_generated/Any_V2_K_L/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Distill_Any_S --output ~/Downloads/images_cropped/sample/right_generated/Distill_Any_S/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Distill_Any_B --output ~/Downloads/images_cropped/sample/right_generated/Distill_Any_B/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model Distill_Any_L --output ~/Downloads/images_cropped/sample/right_generated/Distill_Any_L/ --edge-dilation 2 --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model DepthPro --output ~/Downloads/images_cropped/sample/right_generated/DepthPro/ --depth-aa --tta --method mlbw_l4s
python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --convergence 0.5 --divergence 4.0 --depth-model DepthPro_S --output ~/Downloads/images_cropped/sample/right_generated/DepthPro_S/ --depth-aa --tta --method mlbw_l4s
```

## print_commands_mapper.py
Prints `nunif iw3.cli`  commands to generate the right sample images for all mappers
```sh
source .venv/bin/activate
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/shift_08; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper shift_08 --output ~/Downloads/images_cropped/sample/mapper_generated/shift_08/ --mapper-type shift
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/mul_2; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper mul_2 --output ~/Downloads/images_cropped/sample/mapper_generated/mul_2/ --mapper-type mul
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/none; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper none --output ~/Downloads/images_cropped/sample/mapper_generated/none/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/shift_14; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper shift_14 --output ~/Downloads/images_cropped/sample/mapper_generated/shift_14/ --mapper-type shift
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/inv_mul_2; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper inv_mul_2 --output ~/Downloads/images_cropped/sample/mapper_generated/inv_mul_2/ --mapper-type mul
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/shift_30; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper shift_30 --output ~/Downloads/images_cropped/sample/mapper_generated/shift_30/ --mapper-type shift
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/softplus2; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper softplus2 --output ~/Downloads/images_cropped/sample/mapper_generated/softplus2/
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/shift_06; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper shift_06 --output ~/Downloads/images_cropped/sample/mapper_generated/shift_06/ --mapper-type shift
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/inv_mul_3; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper inv_mul_3 --output ~/Downloads/images_cropped/sample/mapper_generated/inv_mul_3/ --mapper-type mul
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/div_4; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper div_4 --output ~/Downloads/images_cropped/sample/mapper_generated/div_4/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/mul_3; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper mul_3 --output ~/Downloads/images_cropped/sample/mapper_generated/mul_3/ --mapper-type mul
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/div_25; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper div_25 --output ~/Downloads/images_cropped/sample/mapper_generated/div_25/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/pow2; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper pow2 --output ~/Downloads/images_cropped/sample/mapper_generated/pow2/
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/inv_mul_1; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper inv_mul_1 --output ~/Downloads/images_cropped/sample/mapper_generated/inv_mul_1/ --mapper-type mul
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/div_10; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper div_10 --output ~/Downloads/images_cropped/sample/mapper_generated/div_10/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/div_2; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper div_2 --output ~/Downloads/images_cropped/sample/mapper_generated/div_2/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/div_6; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper div_6 --output ~/Downloads/images_cropped/sample/mapper_generated/div_6/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/div_1; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper div_1 --output ~/Downloads/images_cropped/sample/mapper_generated/div_1/ --mapper-type div
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/auto; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper auto --output ~/Downloads/images_cropped/sample/mapper_generated/auto/
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/mul_1; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper mul_1 --output ~/Downloads/images_cropped/sample/mapper_generated/mul_1/ --mapper-type mul
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/shift_20; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper shift_20 --output ~/Downloads/images_cropped/sample/mapper_generated/shift_20/ --mapper-type shift
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/shift_045; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper shift_045 --output ~/Downloads/images_cropped/sample/mapper_generated/shift_045/ --mapper-type shift
mkdir -p ~/Downloads/images_cropped/sample/mapper_generated/softplus; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model Any_B --mapper softplus --output ~/Downloads/images_cropped/sample/mapper_generated/softplus/
```

## print_commands_methods.py
Prints `nunif iw3.cli`  commands to generate the right sample images for all methods
```
source .venv/bin/activate
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/backward/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method backward --output ~/Downloads/images_cropped/sample/right_generated_method/backward/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/forward/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method forward --output ~/Downloads/images_cropped/sample/right_generated_method/forward/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/forward_fill/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method forward_fill --output ~/Downloads/images_cropped/sample/right_generated_method/forward_fill/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l2/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method mlbw_l2 --output ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l2/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l4/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method mlbw_l4 --output ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l4/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l2s/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method mlbw_l2s --output ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l2s/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l4s/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method mlbw_l4s --output ~/Downloads/images_cropped/sample/right_generated_method/mlbw_l4s/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/row_flow/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method row_flow --output ~/Downloads/images_cropped/sample/right_generated_method/row_flow/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/row_flow_sym/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method row_flow_sym --output ~/Downloads/images_cropped/sample/right_generated_method/row_flow_sym/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/row_flow_v3/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method row_flow_v3 --output ~/Downloads/images_cropped/sample/right_generated_method/row_flow_v3/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/row_flow_v3_sym/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method row_flow_v3_sym --output ~/Downloads/images_cropped/sample/right_generated_method/row_flow_v3_sym/
mkdir -p ~/Downloads/images_cropped/sample/right_generated_method/row_flow_v2/; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/ --synthetic-view right --yes --depth-model ZoeD_Any_N --method row_flow_v2 --output ~/Downloads/images_cropped/sample/right_generated_method/row_flow_v2/
```

## print_commands_params.py
Prints `nunif iw3.cli` commands to generate the right sample images for a subset of images using `--find-params`
```shell
source .venv/bin/activate
mkdir -p ~/Downloads/images_cropped/sample/param_generated/005600_R; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/005600_L.png --synthetic-view right --yes --depth-model ZoeD_Any_N --find-param {divergence,convergence,foreground-scale} --output ~/Downloads/images_cropped/sample/param_generated/005600_R/
...
mkdir -p ~/Downloads/images_cropped/sample/param_generated/105500_R; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/105500_L.png --synthetic-view right --yes --depth-model ZoeD_Any_N --find-param {divergence,convergence,foreground-scale} --output ~/Downloads/images_cropped/sample/param_generated/105500_R/
```


## compare_models.py
Compares all right generated images to the ground truth and averages a score for each model

# Results
## Baseline

With 1093 images from video keyframes converted and compared with [imgcompare.image_diff_percent](https://github.com/datenhahn/imgcompare/issues)
These ran at ~9 images/second with RTX 3090 except for `DepthPro` and `DepthPro_S` which took 2.47 and 4.64
### Grayscale
| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.5582 |
| Any_V2_K_L    |  6.5    |
| Any_V2_K      |  6.5    |
| Distill_Any_L |  6.493  |
| Any_V2_K_S    |  6.4901 |
| Distill_Any_B |  6.4802 |
| Distill_Any_S |  6.4798 |
| ZoeD_NK       |  6.4751 |
| ZoeD_Any_K    |  6.4681 |
| Any_V2_L      |  6.4574 |
| Any_V2_S      |  6.4568 |
| ZoeD_K        |  6.4568 |
| Any_V2_B      |  6.4567 |
| Any_V2_N_B    |  6.445  |
| Any_V2_N      |  6.4376 |
| Any_V2_N_L    |  6.4376 |
| Any_V2_N_S    |  6.4365 |
| ZoeD_N        |  6.4152 |
| Any_S         |  6.4087 |
| Any_L         |  6.4076 |
| Any_B         |  6.4017 |
| ZoeD_Any_N    |  6.378  |
| DepthPro      |  6.3077 |
| DepthPro_S    |  6.2761 |


### RGB
Same but images were kept as RGB instead of grayscale conversion

| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.6775 |
| Any_V2_K_L    |  6.6192 |
| Any_V2_K      |  6.6192 |
| Distill_Any_L |  6.6122 |
| Any_V2_K_S    |  6.6094 |
| Distill_Any_B |  6.5992 |
| Distill_Any_S |  6.5988 |
| ZoeD_NK       |  6.594  |
| ZoeD_Any_K    |  6.587  |
| Any_V2_L      |  6.5763 |
| Any_V2_B      |  6.5757 |
| Any_V2_S      |  6.5757 |
| ZoeD_K        |  6.5753 |
| Any_V2_N_B    |  6.564  |
| Any_V2_N      |  6.5567 |
| Any_V2_N_L    |  6.5567 |
| Any_V2_N_S    |  6.5554 |
| ZoeD_N        |  6.5337 |
| Any_S         |  6.5272 |
| Any_L         |  6.5263 |
| Any_B         |  6.5204 |
| ZoeD_Any_N    |  6.4965 |
| DepthPro      |  6.4267 |
| DepthPro_S    |  6.3945 |

## Tuning Options
All of these were done with RGB mode

### --edge-dilation
Edge dilation only applicable for models with `Any` in the name
| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.6775 |
| Any_V2_K_L    |  6.6192 |
| Any_V2_K      |  6.6192 |
| Distill_Any_L |  6.6122 |
| Any_V2_K_S    |  6.6094 |
| Distill_Any_B |  6.5992 |
| Distill_Any_S |  6.5988 |
| ZoeD_NK       |  6.594  |
| ZoeD_Any_K    |  6.5884 |
| Any_V2_L      |  6.5763 |
| Any_V2_B      |  6.5757 |
| Any_V2_S      |  6.5757 |
| ZoeD_K        |  6.5753 |
| Any_V2_N_B    |  6.564  |
| Any_V2_N      |  6.5567 |
| Any_V2_N_L    |  6.5567 |
| Any_V2_N_S    |  6.5554 |
| ZoeD_N        |  6.5337 |
| Any_S         |  6.5272 |
| Any_L         |  6.5263 |
| Any_B         |  6.5204 |
| ZoeD_Any_N    |  6.4981 |
| DepthPro      |  6.4267 |
| DepthPro_S    |  6.3945 |

### --depth-aa
Edge dilation only applicable for models with `Any` in the name
| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.6775 |
| Any_V2_K_L    |  6.6192 |
| Any_V2_K      |  6.6192 |
| Distill_Any_L |  6.6122 |
| Any_V2_K_S    |  6.6094 |
| Distill_Any_B |  6.5992 |
| Distill_Any_S |  6.5988 |
| ZoeD_NK       |  6.594  |
| ZoeD_Any_K    |  6.587  |
| Any_V2_L      |  6.5789 |
| Any_V2_S      |  6.5781 |
| Any_V2_B      |  6.578  |
| ZoeD_K        |  6.5753 |
| Any_V2_N_B    |  6.564  |
| Any_V2_N      |  6.5567 |
| Any_V2_N_L    |  6.5567 |
| Any_V2_N_S    |  6.5554 |
| ZoeD_N        |  6.5337 |
| Any_S         |  6.5272 |
| Any_L         |  6.5263 |
| Any_B         |  6.5204 |
| ZoeD_Any_N    |  6.4965 |
| DepthPro      |  6.4267 |
| DepthPro_S    |  6.3945 |


### --tta
This dropped most processing by 2-3/s

| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.6729 |
| Any_V2_K_L    |  6.6178 |
| Any_V2_K      |  6.6178 |
| Any_V2_K_S    |  6.6082 |
| Distill_Any_L |  6.6078 |
| Distill_Any_S |  6.5982 |
| Distill_Any_B |  6.5977 |
| ZoeD_Any_K    |  6.5832 |
| Any_V2_L      |  6.5763 |
| Any_V2_S      |  6.5762 |
| ZoeD_NK       |  6.5753 |
| Any_V2_B      |  6.5744 |
| ZoeD_K        |  6.5729 |
| Any_V2_N_B    |  6.5622 |
| Any_V2_N      |  6.5549 |
| Any_V2_N_L    |  6.5549 |
| Any_V2_N_S    |  6.5509 |
| ZoeD_N        |  6.5328 |
| Any_S         |  6.5258 |
| Any_L         |  6.5244 |
| Any_B         |  6.518  |
| ZoeD_Any_N    |  6.4886 |
| DepthPro      |  6.4194 |
| DepthPro_S    |  6.3922 |

### --method 
I used `ZoeD_Any_N` as the model to test this with

| Method          |   Score |
|-----------------|---------|
| forward         |  6.6026 |
| backward        |  6.5096 |
| row_flow_sym    |  6.5046 |
| row_flow_v3_sym |  6.5046 |
| forward_fill    |  6.4968 |
| row_flow        |  6.4965 |
| row_flow_v3     |  6.4965 |
| mlbw_l2         |  6.4887 |
| mlbw_l2s        |  6.4886 |
| row_flow_v2     |  6.4881 |
| mlbw_l4         |  6.4876 |
| mlbw_l4s        |  6.4871 |

### --find-params
I used `ZoeD_Any_N` as the model to test this with
This generates a combination (80) of divergence, convergence, foreground-scale images just for one image
I only used a smaller sample of 110 images for this test


| Combination   |   Score |
|---------------|---------|
| d50_c7_fs3    |  8.393  |
| d50_c0_fs0    |  8.1231 |
| d40_c7_fs3    |  7.8887 |
| d50_c0_fs1    |  7.8819 |
| d50_c7_fs2    |  7.6794 |
| d40_c0_fs0    |  7.4349 |
| d50_c0_fs2    |  7.4111 |
| d30_c7_fs3    |  7.3587 |
| d40_c7_fs2    |  7.2682 |
| d40_c0_fs1    |  7.2394 |
| d50_c7_fs1    |  7.0654 |
| d50_c0_fs3    |  6.9992 |
| d20_c7_fs3    |  6.982  |
| d30_c0_fs0    |  6.9144 |
| d30_c7_fs2    |  6.9109 |
| d40_c0_fs2    |  6.9107 |
| d10_c7_fs3    |  6.8345 |
| d50_c7_fs0    |  6.8131 |
| d30_c0_fs1    |  6.7973 |
| d40_c7_fs1    |  6.7889 |
| d10_c7_fs2    |  6.7429 |
| d20_c7_fs2    |  6.7379 |
| d10_c5_fs3    |  6.7204 |
| d50_c5_fs3    |  6.7195 |
| d50_c2_fs0    |  6.6905 |
| d10_c7_fs1    |  6.6849 |
| d10_c7_fs0    |  6.6651 |
| d40_c0_fs3    |  6.664  |
| d10_c5_fs2    |  6.6512 |
| d10_c2_fs3    |  6.6468 |
| d30_c0_fs2    |  6.6217 |
| d10_c5_fs1    |  6.614  |
| d40_c7_fs0    |  6.6126 |
| d20_c0_fs0    |  6.6111 |
| d10_c0_fs3    |  6.6099 |
| d30_c7_fs1    |  6.6095 |
| d10_c5_fs0    |  6.603  |
| d40_c5_fs3    |  6.6025 |
| d10_c2_fs2    |  6.5991 |
| d20_c7_fs1    |  6.582  |
| d10_c0_fs2    |  6.5809 |
| d10_c0_fs0    |  6.5788 |
| d20_c5_fs3    |  6.5784 |
| d10_c2_fs1    |  6.5766 |
| d10_c0_fs1    |  6.5746 |
| d10_c2_fs0    |  6.5733 |
| d20_c0_fs1    |  6.5684 |
| d30_c5_fs3    |  6.5529 |
| d50_c2_fs1    |  6.534  |
| d20_c7_fs0    |  6.5256 |
| d30_c7_fs0    |  6.5101 |
| d20_c0_fs2    |  6.5033 |
| d30_c0_fs3    |  6.5023 |
| d40_c2_fs0    |  6.485  |
| d20_c0_fs3    |  6.4745 |
| d20_c2_fs3    |  6.4435 |
| d20_c5_fs2    |  6.4378 |
| d20_c2_fs0    |  6.4094 |
| d30_c2_fs0    |  6.3981 |
| d20_c2_fs1    |  6.3899 |
| d40_c2_fs1    |  6.3883 |
| d20_c2_fs2    |  6.3859 |
| d20_c5_fs1    |  6.3669 |
| d20_c5_fs0    |  6.3532 |
| d30_c2_fs1    |  6.3474 |
| d50_c2_fs2    |  6.3271 |
| d30_c5_fs2    |  6.3223 |
| d50_c5_fs2    |  6.2932 |
| d30_c2_fs3    |  6.2905 |
| d40_c5_fs2    |  6.2792 |
| d30_c2_fs2    |  6.2745 |
| d40_c2_fs2    |  6.2543 |
| d30_c5_fs1    |  6.2132 |
| d50_c2_fs3    |  6.2073 |
| d40_c2_fs3    |  6.1975 |
| d30_c5_fs0    |  6.1943 |
| d40_c5_fs1    |  6.1523 |
| d50_c5_fs1    |  6.1517 |
| d50_c5_fs0    |  6.1495 |
| d40_c5_fs0    |  6.1468 |

|   Divergence |   Score |
|--------------|---------|
|           50 |  6.9649 |
|           40 |  6.7071 |
|           10 |  6.641  |
|           30 |  6.5511 |
|           20 |  6.5219 |

|   Convergence |   Score |
|---------------|---------|
|             7 |  6.9827 |
|             0 |  6.9001 |
|             2 |  6.4209 |
|             5 |  6.4051 |

|   Foreground Scale |   Score |
|--------------------|---------|
|                  3 |  6.7833 |
|                  2 |  6.6596 |
|                  0 |  6.6396 |
|                  1 |  6.6263 |

### --mapper
Model used was `Any_B` without any fs options
| Mapper    |   Score |
|-----------|---------|
| div_1     |  7.1796 |
| softplus2 |  7.1352 |
| mul_3     |  7.071  |
| div_2     |  6.982  |
| mul_2     |  6.8231 |
| softplus  |  6.8039 |
| div_4     |  6.7987 |
| inv_mul_3 |  6.7252 |
| shift_30  |  6.7184 |
| div_6     |  6.7165 |
| pow2      |  6.6896 |
| inv_mul_2 |  6.658  |
| mul_1     |  6.643  |
| div_10    |  6.6404 |
| shift_20  |  6.6269 |
| inv_mul_1 |  6.5946 |
| div_25    |  6.5662 |
| shift_14  |  6.5623 |
| none      |  6.5204 |
| auto      |  6.5204 |
| shift_08  |  6.5032 |
| shift_045 |  6.495  |
| shift_06  |  6.493  |

With `--input X --synthetic-view right --yes --depth-model Any_B --mapper X --convergence 0.5 --divergence 4.0 --foreground-scale 0 --depth-model Any_B --mapper-type X`

| Mapper    |   Score |
|-----------|---------|
| div_1     |  7.7866 |
| softplus2 |  7.7461 |
| mul_3     |  7.6129 |
| div_2     |  7.3294 |
| mul_2     |  7.0725 |
| softplus  |  7.0277 |
| div_4     |  6.8851 |
| inv_mul_3 |  6.811  |
| pow2      |  6.688  |
| shift_30  |  6.6844 |
| div_6     |  6.6797 |
| mul_1     |  6.6286 |
| inv_mul_2 |  6.5849 |
| div_10    |  6.4978 |
| shift_20  |  6.4666 |
| inv_mul_1 |  6.3992 |
| div_25    |  6.3336 |
| shift_14  |  6.3257 |
| shift_045 |  6.2686 |
| none      |  6.2484 |
| auto      |  6.2484 |
| shift_06  |  6.2319 |
| shift_08  |  6.2259 |

With `--input X --synthetic-view right --yes --depth-model Any_B --mapper X --convergence 0.5 --divergence 5.0 --foreground-scale 1 --depth-model Any_B --mapper-type X`

| Mapper    |   Score |
|-----------|---------|
| div_1     |  8.2193 |
| softplus2 |  8.1899 |
| mul_3     |  8.0245 |
| div_2     |  7.6484 |
| mul_2     |  7.355  |
| softplus  |  7.2988 |
| div_4     |  7.0817 |
| inv_mul_3 |  6.9655 |
| pow2      |  6.8479 |
| shift_30  |  6.8178 |
| div_6     |  6.8116 |
| mul_1     |  6.7841 |
| inv_mul_2 |  6.6301 |
| div_10    |  6.5717 |
| shift_20  |  6.5312 |
| inv_mul_1 |  6.3758 |
| div_25    |  6.3575 |
| shift_14  |  6.3468 |
| shift_045 |  6.2728 |
| none      |  6.2467 |
| auto      |  6.2467 |
| shift_06  |  6.2236 |
| shift_08  |  6.2197 |

### --edge-dilation --depth-aa --convergence 0.5 --divergence 4.0
| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.5049 |
| ZoeD_Any_K    |  6.4538 |
| ZoeD_NK       |  6.4198 |
| Any_V2_K_S    |  6.4086 |
| Any_V2_K_L    |  6.3935 |
| Any_V2_K      |  6.3935 |
| Distill_Any_L |  6.3747 |
| ZoeD_K        |  6.3696 |
| Distill_Any_B |  6.3644 |
| Distill_Any_S |  6.3527 |
| Any_V2_B      |  6.3328 |
| Any_V2_L      |  6.3288 |
| Any_V2_S      |  6.3272 |
| Any_V2_N_S    |  6.2999 |
| Any_V2_N_B    |  6.2968 |
| ZoeD_N        |  6.2829 |
| Any_V2_N      |  6.2786 |
| Any_V2_N_L    |  6.2786 |
| Any_L         |  6.2562 |
| Any_S         |  6.2501 |
| Any_B         |  6.2484 |
| ZoeD_Any_N    |  6.2473 |
| DepthPro      |  6.097  |
| DepthPro_S    |  6.0856 |

### --edge-dilation --depth-aa --convergence 0.5 --divergence 4.0 --method mlbw_l4s --tta
| Model         |   Score |
|---------------|---------|
| Any_V2_K_B    |  6.494  |
| ZoeD_Any_K    |  6.4459 |
| Any_V2_K_S    |  6.4058 |
| Any_V2_K_L    |  6.3862 |
| Any_V2_K      |  6.3862 |
| ZoeD_K        |  6.365  |
| ZoeD_NK       |  6.3623 |
| Distill_Any_L |  6.359  |
| Distill_Any_B |  6.3541 |
| Distill_Any_S |  6.3426 |
| Any_V2_B      |  6.3236 |
| Any_V2_L      |  6.3204 |
| Any_V2_S      |  6.3183 |
| Any_V2_N_B    |  6.2917 |
| Any_V2_N_S    |  6.2887 |
| ZoeD_N        |  6.2768 |
| Any_V2_N      |  6.2702 |
| Any_V2_N_L    |  6.2702 |
| Any_L         |  6.2508 |
| Any_S         |  6.2469 |
| Any_B         |  6.2433 |
| ZoeD_Any_N    |  6.2358 |
| DepthPro_S    |  6.0858 |
| DepthPro      |  6.0637 |