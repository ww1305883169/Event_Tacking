# 历史埋点方案语料 · 样本 1

> 来源：history_file.xlsx（原始文件被脚本覆盖损坏，本行为用户手工粘贴的真实数据）
> 录入时间：2026-09-21

## 原始行数据（6 列结构）

| 列名 | 值 |
|---|---|
| 指标名 | 【场景选择页迭代】模式选择入口 |
| 指标描述 | 入口点击uv/pv<br>入口曝光uv/pv |
| 事件 | http://ping.migu.cn/apex/#/ameta/add-event/4518 畅听播放器/按钮 曝光和点击都要报 参数： triggerType 曝光"1"，点击"2" buttonTitle 写死 "模式入口"， resType 当前畅听播放器内容的资源类型，（歌曲："2"，MV:"D"，直播:"liveroom"，演唱会："2022"） resId 当前畅听播放器内容的id resName 资源名称 type 传1 畅听，2 全屏 sectionTitle 写死 "模式入口" musicMode 当前模式的ID （默认传"default"） |
| 端 | Android、IOS、鸿蒙 |
| 触发类型 | 点击、曝光 |
| 截图说明 | =DISPIMG("ID_4EAA2A9469CA498C9ECE5398374F318D",1)（嵌入式截图，需人工查看） |

## 结构化解析

```yaml
sample_id: sample-001
source: history_file.xlsx
feature_name: 【场景选择页迭代】模式选择入口
metric_name: 模式选择入口
requirement_desc:
  - 入口点击uv/pv
  - 入口曝光uv/pv
event_config:
  platform_url: http://ping.migu.cn/apex/#/ameta/add-event/4518
  page_or_component: 畅听播放器/按钮
  report_both: 曝光和点击都要报
  params:
    - name: triggerType
      rule: 曝光"1"，点击"2"
    - name: buttonTitle
      rule: 写死 "模式入口"
    - name: resType
      rule: 当前畅听播放器内容的资源类型
      enum:
        歌曲: "2"
        MV: "D"
        直播: "liveroom"
        演唱会: "2022"
    - name: resId
      rule: 当前畅听播放器内容的id
    - name: resName
      rule: 资源名称
    - name: type
      rule: 传1 畅听，2 全屏
      enum:
        畅听: "1"
        全屏: "2"
    - name: sectionTitle
      rule: 写死 "模式入口"
    - name: musicMode
      rule: 当前模式的ID
      default: "default"
platforms: [Android, IOS, 鸿蒙]
trigger_types: [点击, 曝光]
screenshot_ref: ID_4EAA2A9469CA498C9ECE5398374F318D
```

## 从本样本提炼的规范（v0.1）

### R1 指标名
- 格式：`【功能/项目名】+ 具体入口/模块名`
- 用全角方括号【】标记所属迭代/功能

### R2 指标描述
- 格式：`名词短语 + uv/pv`，多个指标换行分隔
- uv/pv 是核心计量口径（点击类和曝光类分别统计）

### R3 事件列（信息密度最高）
固定语法顺序：
1. 平台事件配置链接（ping.migu.cn/apex 埋点管理平台）
2. `页面/组件` 定位（如 `畅听播放器/按钮`）
3. 上报要求（如 `曝光和点击都要报`）
4. `参数：` 关键字引出参数列表
5. 每个参数：`参数名 + 赋值规则`，可选枚举映射 `（键:"值"，...）`

### R4 参数赋值规则类型
- **写死型**：`写死 "字面量"`（buttonTitle、sectionTitle）
- **枚举型**：`（歌曲:"2"，MV:"D"）`——中文键映射到上报值
- **动态取值型**：`当前页面上内容的id`（resId、resName）
- **默认值型**：`默认传"default"`（musicMode）

### R5 端
- 多端并列用顿号：`Android、IOS、鸿蒙`
- 注意 "IOS" 是团队习惯写法（非标准 iOS）

### R6 触发类型
- 与事件列的"曝光和点击都要报"对应，顿号分隔

### R7 截图说明
- 用 WPS `=DISPIMG()` 公式嵌入截图，agent 无法读取，需单独维护图片引用 ID 表
