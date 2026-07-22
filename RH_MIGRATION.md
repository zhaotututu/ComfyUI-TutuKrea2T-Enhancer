# RunningHub 安装与工作流迁移清单

## 目标工作流

- 名称：`KREA2 TURBO 图图最强文生图工作流（提示词增强 + Krea2T 双增强）`
- RH 工作流 ID：`2072516698963537921`
- 公开地址：https://www.runninghub.cn/post/2072516698963537921/

本清单只针对这个工作流，不涉及“标准 KREA2 TURBO”等其他工作流。

## 交给 RH 的安装信息

- Git 仓库：`https://github.com/zhaotututu/ComfyUI-TutuKrea2T-Enhancer.git`
- 安装目录：`ComfyUI/custom_nodes/ComfyUI-TutuKrea2T-Enhancer`
- 节点类型：`TutuKrea2TEnhancer`
- 显示名称：`Tutu Krea2T Enhancer`
- 额外 Python 依赖：无
- 可与原节点并存：是
- 需要重启 ComfyUI：是

建议 RH 暂时保留原 `ComfyUI-Krea2T-Enhancer`，不要覆盖或删除，以便立即回滚。

## 需要替换的线上节点

| 节点 ID | 当前节点类型 | 当前标题 | 替换后节点类型 | 建议标题 |
|---:|---|---|---|---|
| 109 | `ComfyUI-Krea2T-Enhancer` | `Krea2T Enhancer - C 单开` | `TutuKrea2TEnhancer` | `Tutu Krea2T Enhancer - C 单开` |
| 17 | `ComfyUI-Krea2T-Enhancer` | `Krea2T Enhancer - D 双增强` | `TutuKrea2TEnhancer` | `Tutu Krea2T Enhancer - D 双增强` |

新旧节点的输入、输出及控件顺序一致。替换时保留：

- `enabled`、`strength`、`debug` 当前值；
- 节点 109 的现有输入链接 `50` 和输出链接 `53`；
- 节点 17 的现有输入链接 `7` 和输出链接 `29`；
- 所有节点位置、尺寸、分组和工作流其他内容。

工作流 JSON 中必须同步更新：

1. `workflowContent` 内节点 109、17 的 `type`；
2. `promptContent` 内节点 109、17 的 `class_type`；
3. 重新生成的 `promptContent`，不能只改画布 JSON；
4. 工作流最终保存配置和发布版本内容。

## 上线顺序

1. 将节点仓库发布到固定 Git 地址并创建首个版本标签。
2. RH 在测试环境安装节点并重启 ComfyUI。
3. 确认 `/object_info` 能返回 `TutuKrea2TEnhancer`。
4. 复制目标工作流作为私有测试副本。
5. 只在副本中替换节点 109、17，并保留全部连接和参数。
6. 调用 RH `/api/workflow/check`，确认依赖、节点类型和模型均通过。
7. 分别执行 C 单开、D 双增强；A/B 绕过分支也各做一次冒烟检查。
8. 确认无位置参数报错、四条分支均能出图后，再更新正式线上工作流。
9. 重新读取线上 `workflowContent` 和 `promptContent`，核对两个节点类型及所有链接。
10. 从公开页面实际发起一次任务，确认访客运行路径也已使用新节点。

## 验收标准

- 不再出现：`takes from 4 to 6 positional arguments but 7 were given`。
- C 单开、D 双增强都能进入采样并正常产出图片。
- A/B 绕过分支的行为和替换前一致。
- 新旧 ComfyUI Krea2 调用签名均通过节点仓库回归测试。
- 线上画布内容、执行提示词内容和公开运行版本三处一致。

## 回滚

如果 RH 环境出现未覆盖的问题：

1. 不卸载新节点；
2. 将正式工作流恢复到替换前保存版本；
3. 确认节点 109、17 的类型恢复为 `ComfyUI-Krea2T-Enhancer`；
4. 保留失败任务 ID、完整日志和 RH 当前 ComfyUI commit，回到仓库修复并增加对应回归测试。
