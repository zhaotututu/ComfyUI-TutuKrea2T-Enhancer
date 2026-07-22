# ComfyUI-TutuKrea2T-Enhancer

面向 RunningHub / ComfyUI 的 Krea2 Turbo 提示词遵循增强节点。它基于
[`capitan01R/ComfyUI-Krea2T-Enhancer`](https://github.com/capitan01R/ComfyUI-Krea2T-Enhancer)
的 MIT 许可代码维护，保留原增强算法，只独立维护兼容性、测试和发布节奏。

## 为什么需要这个版本

2026-07 的 ComfyUI Krea2 模型调用新增了 `ref_latents` 位置参数。原节点使用固定参数签名，
会在采样开始前报错：

```text
krea2t_enhancer_wrapper() takes from 4 to 6 positional arguments but 7 were given
```

本节点的包装器接收并原样透传 ComfyUI 的完整参数列表，因此同时兼容：

- 旧调用：`x, timesteps, context, attention_mask, transformer_options`
- 新调用：`x, timesteps, context, attention_mask, ref_latents, transformer_options`
- 后续在模型调用尾部继续增加的位置参数

## 节点信息

| 项目 | 值 |
|---|---|
| 节点类型 | `TutuKrea2TEnhancer` |
| 显示名称 | `Tutu Krea2T Enhancer` |
| 分类 | `conditioning/krea2` |
| 输入 | `model`, `enabled`, `strength`, `debug` |
| 输出 | `MODEL` |

节点类型、配置键和包装器键均与原节点不同，可以和原节点同时安装，不会互相覆盖。

## 安装

将本仓库克隆到 ComfyUI 的 `custom_nodes` 目录，然后重启 ComfyUI：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/zhaotututu/ComfyUI-TutuKrea2T-Enhancer.git
```

除 ComfyUI 和 Krea2 正常运行所需环境外，不需要新增 Python 依赖。

更新节点：

```bash
cd ComfyUI/custom_nodes/ComfyUI-TutuKrea2T-Enhancer
git pull --ff-only
```

## 使用和迁移

连接方式：

```text
Load Diffusion Model -> Tutu Krea2T Enhancer -> KSampler
```

从原节点迁移时，逐个替换为 `Tutu Krea2T Enhancer`，并保持以下参数不变：

- `enabled`
- `strength`
- `debug`
- 上游 `MODEL` 输入和下游 `MODEL` 输出连接

## 维护原则

- 保持原节点的增强算法和参数语义，不加入与兼容性无关的功能。
- 对 ComfyUI 旧、新 Krea2 调用签名同时做回归测试。
- RH 安装新版本后先在副本工作流验证，再替换线上正式工作流。

## 许可证与署名

本项目使用 MIT License。原始代码版权归 `capitan01R` 所有；Tutu 维护版本的改动、
来源版本和范围记录在 [NOTICE.md](NOTICE.md) 中。
