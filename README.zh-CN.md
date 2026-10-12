# LumaMosaic · 光影织境

**让照片生长成三个视觉世界。**

LumaMosaic 是一个把一张或多张参考照片转化为三套成品壁纸的 Agent Skill：

1. **原图跟色**：忠实保留照片的主色、光线、环境和情绪。
2. **智能延展**：从照片中真实存在的颜色、形状、材质或光影继续生长新场景。
3. **大胆创新**：保留主体辨识度，重新选择更有新意的艺术方向。

适用于宠物、人物、产品、汽车、美食、建筑和旅行照片。第三版会根据主体与照片证据选择风格，不会把每次任务都做成赛博朋克、粉紫星空或月亮云朵。

[English](README.md)

## 安装

```bash
npx skills add fledgling-david/luma-mosaic
```

也可以把整个 `luma-mosaic` 文件夹复制到本机 Skills 目录，然后重启 Agent 宿主。

## 使用

上传照片后可以直接说：

> 使用 $luma-mosaic，把这些照片做成三张 16:9 电脑壁纸。主体必须还是同一个，左侧给桌面图标留出干净区域。

Skill 会先分析主体的固定特征、照片配色、光线、情绪、每张照片适合承担的构图角色，以及桌面安全区，再生成三个差异明确的位图成品。用户若指定单一模式，也可以只生成该方向。

## 辅助工具

不运行 Python 工具也能使用本 Skill；以下工具用于提高分析与验收的一致性。

```bash
python -m pip install -r requirements.txt

# 提取多张照片的加权色板
python scripts/analyze_palette.py photo-1.jpg photo-2.jpg --output palette.json

# 生成三版结构化设计计划
python scripts/plan_wallpapers.py --subject "棕灰虎斑猫" --mood "安静温暖" \
  --palette-file palette.json --output plan.json

# 检查尺寸、比例和近似重复
python scripts/validate_images.py output-01.png output-02.png output-03.png --ratio 16:9
```

## 核心原则

- 保留人物五官、宠物花纹、产品结构等身份锚点。
- 三版必须在场景逻辑、配色或构图上真正不同，而不是只换滤镜。
- 图像边缘、阴影、比例、颗粒与光源要统一，避免明显贴图感。
- 默认输出三张独立成品，不用“只给提示词”代替用户要的壁纸。
- 除非用户指定，不添加文字、水印、边框或签名。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## 说明

LumaMosaic 负责分析、生成策略和成品质检。实际出图仍需要宿主提供支持参考图的图像生成或编辑能力，最终主体还原度也会受所用模型和参考照片质量影响。

项目不包含上传或遥测代码；照片如何处理由宿主工具决定。

## 许可证

MIT
