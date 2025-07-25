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
## print_commands.py
Prints the commands to generate the right sample images for all models with nunif iw3.cli

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
Foreground Scale doesn't appear to do anything despite listed as supported by `ZoeD_Any_N` 


| Combination   |   Score |
|---------------|---------|
| d50_c0_fs2    |  8.1231 |
| d50_c0_fs0    |  8.1231 |
| d50_c0_fs3    |  8.1231 |
| d50_c0_fs1    |  8.1231 |
| d40_c0_fs0    |  7.4349 |
| d40_c0_fs1    |  7.4349 |
| d40_c0_fs2    |  7.4349 |
| d40_c0_fs3    |  7.4349 |
| d30_c0_fs1    |  6.9144 |
| d30_c0_fs0    |  6.9144 |
| d30_c0_fs2    |  6.9144 |
| d30_c0_fs3    |  6.9144 |
| d50_c7_fs2    |  6.8131 |
| d50_c7_fs0    |  6.8131 |
| d50_c7_fs1    |  6.8131 |
| d50_c7_fs3    |  6.8131 |
| d50_c2_fs3    |  6.6905 |
| d50_c2_fs0    |  6.6905 |
| d50_c2_fs1    |  6.6905 |
| d50_c2_fs2    |  6.6905 |
| d10_c7_fs3    |  6.6651 |
| d10_c7_fs2    |  6.6651 |
| d10_c7_fs1    |  6.6651 |
| d10_c7_fs0    |  6.6651 |
| d40_c7_fs3    |  6.6126 |
| d40_c7_fs1    |  6.6126 |
| d40_c7_fs2    |  6.6126 |
| d40_c7_fs0    |  6.6126 |
| d20_c0_fs0    |  6.6111 |
| d20_c0_fs3    |  6.6111 |
| d20_c0_fs1    |  6.6111 |
| d20_c0_fs2    |  6.6111 |
| d10_c5_fs2    |  6.603  |
| d10_c5_fs1    |  6.603  |
| d10_c5_fs3    |  6.603  |
| d10_c5_fs0    |  6.603  |
| d10_c0_fs2    |  6.5788 |
| d10_c0_fs3    |  6.5788 |
| d10_c0_fs1    |  6.5788 |
| d10_c0_fs0    |  6.5788 |
| d10_c2_fs1    |  6.5733 |
| d10_c2_fs3    |  6.5733 |
| d10_c2_fs2    |  6.5733 |
| d10_c2_fs0    |  6.5733 |
| d20_c7_fs3    |  6.5256 |
| d20_c7_fs0    |  6.5256 |
| d20_c7_fs1    |  6.5256 |
| d20_c7_fs2    |  6.5256 |
| d30_c7_fs1    |  6.5101 |
| d30_c7_fs0    |  6.5101 |
| d30_c7_fs3    |  6.5101 |
| d30_c7_fs2    |  6.5101 |
| d40_c2_fs1    |  6.485  |
| d40_c2_fs0    |  6.485  |
| d40_c2_fs2    |  6.485  |
| d40_c2_fs3    |  6.485  |
| d20_c2_fs2    |  6.4094 |
| d20_c2_fs3    |  6.4094 |
| d20_c2_fs1    |  6.4094 |
| d20_c2_fs0    |  6.4094 |
| d30_c2_fs3    |  6.3981 |
| d30_c2_fs2    |  6.3981 |
| d30_c2_fs0    |  6.3981 |
| d30_c2_fs1    |  6.3981 |
| d20_c5_fs0    |  6.3532 |
| d20_c5_fs3    |  6.3532 |
| d20_c5_fs2    |  6.3532 |
| d20_c5_fs1    |  6.3532 |
| d30_c5_fs2    |  6.1943 |
| d30_c5_fs3    |  6.1943 |
| d30_c5_fs0    |  6.1943 |
| d30_c5_fs1    |  6.1943 |
| d50_c5_fs1    |  6.1495 |
| d50_c5_fs2    |  6.1495 |
| d50_c5_fs0    |  6.1495 |
| d50_c5_fs3    |  6.1495 |
| d40_c5_fs0    |  6.1468 |
| d40_c5_fs2    |  6.1468 |
| d40_c5_fs3    |  6.1468 |
| d40_c5_fs1    |  6.1468 |

|   Divergence |   Score |
|--------------|---------|
|           50 |  6.9441 |
|           40 |  6.6698 |
|           10 |  6.6051 |
|           30 |  6.5042 |
|           20 |  6.4748 |

|   Convergence |   Score |
|---------------|---------|
|             0 |  7.1325 |
|             7 |  6.6253 |
|             2 |  6.5113 |
|             5 |  6.2894 |

|   Foreground Scale |   Score |
|--------------------|---------|
|                  0 |  6.6396 |
|                  3 |  6.6396 |
|                  1 |  6.6396 |
|                  2 |  6.6396 |

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