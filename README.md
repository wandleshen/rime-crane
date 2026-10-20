# 凇鹤拼音

![demo](./others/demo_crane.webp)

整合了雾凇拼音和小鹤双拼/音形方案的拼音输入法，简称「凇鹤拼音」。

- 雾凇：功能齐全，词库体验良好，长期更新修订。
- 凇鹤：去除了雾凇中的其他双拼方案，增加了对鹤形的支持，对接官方的小鹤音形。
- tiger-code 分支中现可使用虎码了。

[Rime 配置：雾凇拼音 | 长期维护的简体词库](https://github.com/iDvel/rime-ice) 是本方案全拼/双拼部分的基础方案和词库方案。

[小鹤双拼/音形](https://www.flypy.com/) 是以双手均衡性最优、强弱指分布最合理、跨排别扭组合频率最低为追求的双拼设计方案。其音形码以易学、单字重码率适度、整体效率持平四码类方案为设计目的。

[RIME | 中州韵输入法引擎](https://rime.im/) 是一个跨平台的输入法算法框架，这里是 Rime 的一个配置仓库。

用户需要[下载各平台对应的 Rime 发行版](https://rime.im/download/)，并将此配置应用到配置目录。

详细介绍：[Rime 配置：雾凇拼音](https://dvel.me/posts/rime-ice/)


## 基本套路

- 简体 | 全拼 | 小鹤双拼 | 小鹤音形 | 微软双拼音形
- [雾凇部分全部功能](https://github.com/iDvel/rime-ice#%E5%9F%BA%E6%9C%AC%E5%A5%97%E8%B7%AF)
- 凇鹤 - 小鹤音形主要功能：
    - 首选词（必选）
    - 通过分号次选字词上屏
    - 随心码调整特殊的码位
    - 分号键引导的快符（不支持成对符号光标移动到中间）
    - 一简词
    - 表外字，主要是粤语词汇
    - 全码词
    - `O` 符号引导（默认关闭）
    - 全码字（默认关闭，出简不全）
    - 用户码表
    - 简码提示，如熟悉可以关闭
    - 二重简码（默认关闭，10.9k 之后由一简词代替，可以根据情况开关）
    - 左 `Shift` 键用做输入法内的〔中/英〕切换，右 `Shift` 键保留系统（可通过 Karabiner 等工具实现输入法切换）
    - \` 万能码，作为任意码的补全
    - 通过 Lua 脚本实现了部分直通车功能
    - `Tab` 键编码清屏
    - `Enter` 键编码上屏
    - `Shift + 空格` 进行〔中/半角〕切换
    - `Ctrl + .` 进行〔中/英标点〕切换
    - `Ctrl + j` 进行〔简/繁〕切换

### 支持的快符

![](others/fast-symbols.png)

<!--
http://www.keyboard-layout-editor.com/#/
[{t:"#ff0000"},"Q\n：“","W\n？","E\n（","R\n）","T\n@","Y\n《","U\n》",{c:"#7d7d7d",t:"#000000"},"I",{c:"#cccccc",t:"#ff0000"},"O\n「」","P\n『』"],
[{x:0.25},"A\n！","S\n……","D\n、","F\n重复","G\n·","H\n《》","J\n“”","K\n（）","L\n〔〕",{c:"#ffabab"},":\n;"],
[{x:0.75,c:"#cccccc"},"Z\n“","X\n→","C\n”","V\n——","B\n_",{c:"#7d7d7d",t:"#000000"},"N","M"]
 -->

### 支持的直通车功能

|编码|Windows功能|macOS功能|
|-|-|-|
|oav|打开安装目录|打开安装目录|
|ocm|打开CMD|打开Terminal|
|odn|打开我的电脑|打开Finder|
|oec|打开Excel|打开Excel|
|ogj|打开用户配置目录|打开用户配置目录|
|oht|打开画图工具|-|
|ojs|打开计算器|打开计算器|
|owd|打开Word|打开Word|

|编码|功能|
|-|-|
|ojf|〔简/繁〕切换|

## 词库说明（更新至官方清风版 v1.26.9c）

本方案码表已全面切换至**官方小鹤音形清风便携版（WindInput）**官方挂接源，实现无损保序同步：
- **词汇扩充**：主码表首选字词扩充至 68,572 条（净增 1 万多条官方新词）。
- **官方调频同步**：同步最新调频字（如 `la` 拉、`lom` 骆）与最新快符键位规范（`;p` 单书名号 `〈〉`）。
- **词库模式对齐**：支持官方熟手模式、常规模式与初学模式，可在 `xhup.dict.yaml` 中按需开启/关闭。

```yaml
# 小鹤音形的主码表：文件 "xhup.dict.yaml"，其中按需加载的码表分别如下：
# --- 用户优先层 ---
- "xhup_dicts/xhup.user.top"          # 用户置顶码表：可以按需自行添加置顶词汇
- "xhup_dicts/xhup.user"              # 用户自用词库

# --- ① 熟手模式基础库（默认启用）---
- "xhup_dicts/xhup.primary"           # -0- 首选字词（68,572条，官方原生自然序）
- "xhup_dicts/xhup.secondary"         # 1.1 次选字词（分类词库：次选）
- "xhup_dicts/xhup.whimsicality"      # 1.1 随心码（分类词库：随心）
- "xhup_dicts/xhup.off-table"         # 2.2 表外字（分类词库：表外）
- "xhup_dicts/xhup.single.code"       # 2.1 一简词（一简次选，26个单字/词）
- "xhup_dicts/xhup.fast.symbols"      # 1.2 快符（分号引导符号）

# --- ② 常规模式扩展（已有简码的全码词，可按需开启）---
- "xhup_dicts/xhup.full.code.words"   # 2.3 全码词（约500条）

# --- ③ 初学模式扩展（全码字与生僻字，默认关闭，初学可开启）---
# - "xhup_dicts/xhup.full.code.chars"   # 全码字（已有简码，全码有其他字词，约1650条）
# - "xhup_dicts/xhup.rare.chars"        # 生僻字（约500条）

# --- 可选附加库 ---
# - "xhup_dicts/xhup.secondary.simple"  # 二简次选（66个单字，备选）
# - "xhup_dicts/xhup.symbols"           # 符号与部首字根
# - "xhup_dicts/xhup.emoji"             # 斜杠引导表情
# - "xhup_dicts/xhup.ok"                # ok引导两分/三分拆字拼字库（8.8万条）
```

> 注：维护人员或自动化 Agent 请参阅 [AGENTS.md](./AGENTS.md) 了解官方清风便携版码表逆向同步工作流与测试规范。

## 微软双拼音形

方案 ID：`mspy_xh`，菜单名称：**微软双拼音形**。支持微软双拼整句输入，并保留小鹤形码精确选字、简码、同音字候选、中英混输、分号快符、重复上屏、简繁切换和通配反查。使用空格或数字手动确认候选，每页显示 9 项。

完整复制仓库配置后重新部署，按 `F4` 或 `Ctrl + 反引号` 选择该方案。`default.yaml` 已包含此方案；如果你的 `default.custom.yaml` 覆盖了 `schema_list`，请在自己的列表中加入 `schema: mspy_xh`。

### 编码与操作

| 编码（空格或数字确认） | 结果 |
| --- | --- |
| `hknz` | 好 |
| `q;fo` | 青 |
| `ojfn` | 按 |
| `nihk` | 你好 |
| `urfa` | 输入法 |
| `xhyx` | 小鹤音形 |

- 单字全码：微软双拼两码 + 原小鹤形码两码；例如“好”的形码仍为 `nz`。
- 二字词：每字各取双拼两码；三字词：前两字各取首码、末字取双拼两码；四字及以上：前三字和末字各取首码。
- 零声母统一用 `o`：`an → oj`、`ai → ol`、`er → or`；`ing` 用 `;`，`ü` 用 `y`，`ue/ve` 用 `t`。
- **分号是编码键，数字 `1`～`9` 选择候选，空格确认首选。**例如 `ojui` 的首选是“按时”、次选是“暗示”。四码后继续输入仍保留在编辑区；长句可以连续输入微软双拼，最后统一确认，英文也不会被提前截断。
- 快符保留原键位：`;p` 后按空格输入 `〈〉`，`;f` 后确认候选可重复上一次上屏内容。
- 反引号是单码通配符，例如 `` q;f` `` 可以反查“青”，候选注释显示对应的微软音形编码。
- `Tab` 清空编码，`Enter` 上屏原始编码，`Ctrl+j` 切换简繁，`Ctrl+.` 切换中英标点。

### 词库与转换规则

`mspy_xh.dict.yaml` 挂载 `mspy_xh_dicts/` 下的派生词库，保留源表分层及层内候选顺序，**默认启用单字全码和生僻字形码扩展**。额外二简次选可在入口中按需开启。原小鹤方案及 `xhup_dicts/` 数据保持独立。

一简字词保留原键位；普通二简和首码缩写中的零声母改为 `o`；二字三简按“首字双拼 + 次字首码”转换。随心词的形码尾键保持不变。“鹤 `eh`”“偶尔 `eo`”“什么 `sm`”“桃李争妍 `tlzy`”“为什么 `wsme`”等官方特殊编码，以及中英混合词、网址等固定键位原样保留。官方特殊音节 `om/on/og/hm` 也保留原编码。

转换以源码标明的读音为准，不重新猜测多音字；拼音字表缺少对应读音时使用完整音节映射，并在命令输出中列出。原有同码音形候选保留源表顺序，英文和基本区双拼候选作为独立翻译器参与排序。`o` 是常用零声母编码区，不挂载原方案的 `o` 前缀系统直通车。

### 双拼候选与中英混输

输入完整双拼两码即可从同音字中选择，追加形码可进一步筛选；同时保留原有音形码的前缀补全。候选较多时使用 `-`、`=` 或 Page Up、Page Down 翻页。

| 输入 | 候选示例 |
| --- | --- |
| `q;` | 请、轻、清、青、情、庆、晴、倾、卿…… |
| `q;f` | 青、靘、郬，以及情分、清风等同前缀词 |
| `q;fo` | 首选青，后续可有拼音翻译器的其他解释 |
| `like` | 立刻、like、liked、likes……；按 `2` 选择英文 like |
| `apple` | apple、apples、applet…… |
| `Bvj` / `Upj` | B站 / U盘 |

英文词库复用 `melt_eng`，以独立的 `mspy_xh_english` prism 应用微软双拼符号派生，避免影响原小鹤双拼方案。中英混合词使用 `en_dicts/cn_en_mspy.txt`。大小写沿用仓库的 `autocap_filter` 规则；词库没有的英文可直接输入后按 Enter 上屏原始字母。空格确认候选会被消耗，需要实际空格时再输入空格；不自动添加中英文排版空格。

### 微软双拼整句输入

每个字输入微软双拼两码，连续输入多个音节，由雾凇词库分词组句，最后按空格确认。也可以用单引号手动分隔音节。

| 连续输入 | 已验证的首选 |
| --- | --- |
| `nihkuijx` | 你好世界 |
| `ni'hk'ui'jx` | 你好世界 |
| `wojntmxdqubzj;` | 我今天想去北京 |
| `wovgzluiyswzrrudpn` | 我正在使用微软双拼 |
| `q;bhwouuruvejuhw` | 请帮我输入这句话 |
| `ojqrdiyi` | 安全第一 |
| `lyseiux;` | 绿色出行 |

整句翻译器使用 `rime_ice` 词库和独立的 `mspy_xh_sentence` prism；其 416 个拼音音节映射与音形生成器一致。原有一简、两码同音字、音形精确候选和英文优先级保留；整句候选置于其后，避免短码和英文被无关的中文拼接抢占。

长句按双拼音节连打，不是把多个四码音形码拼在一起；需要形码精确选字时，先确认该字词，再继续输入。中英交替输入也按句或词确认，例如先确认“你好世界”，再输入并确认 `apple`。整句词频学习保存在设备本地的 `mspy_xh_sentence.userdb`，与其他方案分开；默认候选会随词库和个人学习变化，不保证所有句子始终首选正确。

### CJK 基本区覆盖

独立的 `mspy_xh_pinyin.dict.yaml` 从现有中文字表生成基本区的两码微软双拼候选，按中文字频排序、保留多音字，并去除同字同码重复项。

| 范围或输入路径 | 字数 |
| --- | ---: |
| CJK 统一汉字基本区 U+4E00–U+9FFF | 20,992 |
| 现有字表有读音，可用两码双拼选字 | 20,874 |
| 现有字表无读音，使用 Unicode 输入 | 118 |

已有形码的字继续支持追加形码；其余字不编造形码，可从双拼同音候选中选择。例如 `da` 可以翻页选“龘”，`b;` 可以选“靐”。Unicode 路径输入大写 `U` 加十六进制码点后按空格，如 `U4E65` → “乥”、`U9FFF` → “鿿”。已在鼠须管中逐字验证基本区全部 20,992 个码点的 Unicode 输入与上屏；字形是否能正常显示仍取决于目标设备字体。

生成器会打印无读音码点列表。这里覆盖的是 CJK 汉字基本区，不是把整个 BMP U+0000–U+FFFF 当作汉字表。

### 日语用汉字补充

默认挂载独立的 `mspy_xh.japanese` 补充层，新增 14 个日语常见字形。源表为 `xhup_dicts/xhup.japanese.dict.yaml`，由本项目按小鹤首末取形规则手工补码；读音沿用 `cn_dicts/41448.dict.yaml` 的中文字表标注，不使用日语音读、训读或罗马字。

| 字 | 字表读音 | 输入（包含必要的数字选字） |
| --- | --- | --- |
| 栃 | li | `limw2` |
| 峠 | qia | `qwex` |
| 辻 | shi | `uizu2` |
| 榊 | shen | `ufmu` |
| 働 | dong | `dsrl` |
| 笹 | ti | `tivu` |
| 塀 | ping | `p;tk` |
| 槻 | gui | `gvme` |
| 樫 | jian | `jmmt` |
| 椛 | hua | `hwmb3` |
| 畠 | tian | `tmbt` |
| 駅 | yi | `yimn2` |
| 鴫 | tian | `tmtn` |
| 鱈 | xue | `xtae2` |

补充层排在基础词库后，保留已有字词的候选优先级。例如 `limw` 首选仍为“粝”，按 `2` 选择“栃”。表内数字按默认词库配置验证；自定义词库改变候选顺序时，以候选栏为准。已有的“畑、凪、込、雫”等继续使用原表外字层。

继续补字时编辑源表，按小鹤双拼写入前两码、形码写入后两码，再运行下方生成命令；生成器会转换为微软双拼并同步通配反查。此补充层是按需整理的字形集合，不是完整的日本常用汉字或人名用汉字表。

### 更新派生数据

更新官方小鹤源表后，在仓库根目录运行（Python 3.8+，仅标准库，无网络依赖）：

```bash
python3 others/script/generate_mspy_xh.py
python3 others/script/generate_mspy_xh.py --check
python3 -m unittest discover -s others/script -p test_generate_mspy_xh.py -v
```

生成器更新 12 层微软音形词库、基本区双拼字表、默认活动字表的通配反查词典，以及独立的 `opencc/mspy_xh_short_hints.*` 简码提示；提示只引用默认活动词库中实际存在的简码。源词库和原小鹤提示不被覆盖。生成后重新部署 Rime。

### 迁移本方案到其他设备

目标设备需安装包含 librime-lua 的 Rime 前端，保留以下文件的相对目录结构并重新部署：

- 根目录的 `mspy_xh*.schema.yaml`、`mspy_xh.dict.yaml`、`mspy_xh_reverse.dict.yaml`、`mspy_xh_pinyin.dict.yaml`。
- 完整 `mspy_xh_dicts/`，以及 `xhup_dicts/xhup.fast.symbols.dict.yaml`。
- `melt_eng.schema.yaml`、`melt_eng.dict.yaml`，以及 `en_dicts/en.dict.yaml`、`en_dicts/en_ext.dict.yaml`、`en_dicts/cn_en_mspy.txt`。
- `rime_ice.dict.yaml` 和完整 `cn_dicts/`，用于微软双拼整句分词与组句。首次部署需要编译较大的词库。
- `opencc/mspy_xh_short_hints.json`、`opencc/mspy_xh_short_hints.txt`。
- `lua/unicode.lua`、`lua/autocap_filter.lua`。

方案菜单只需加入 `mspy_xh`，其他 `mspy_xh_*` 是自动编译的隐藏依赖。目标设备使用自己的默认配置及 OpenCC 数据，不复制本机的 `build/` 或 `installation.yaml`；普通使用不需要 Python 或 Go。移动端键盘需提供可以发送分号的按键，以输入 `ing`。

## 安装与部署

建议初次安装前备份原先配置，并清空输入法用户配置目录。

### 方式一：下载 Zip 压缩包（推荐，跨平台最稳妥）

1. **下载完整配置包**：
   - **直接下载**：[预打包安装包 rime-crane.zip（推荐）](https://github.com/kchen0x/rime-crane/releases/latest/download/rime-crane.zip)
   - **备用下载**：[GitHub 仓库主分支 ZIP 源码包](https://github.com/kchen0x/rime-crane/archive/refs/heads/main.zip)
   将压缩包内的全部文件及子文件夹（包含 `cn_dicts/`、`en_dicts/`、`xhup_dicts/`、`lua/`、`opencc/` 以及各类 `*.yaml` 方案配置）完整复制并粘贴到各平台对应的 Rime 用户配置目录下：
   * **Windows（小狼毫 Weasel）**：
     `%APPDATA%\Rime`（快捷操作：按 `Win + R` 键输入 `%APPDATA%\Rime` 回车，或从开始菜单点击打开【小狼毫】用户文件夹）
   * **macOS（鼠须管 Squirrel）**：
     `~/Library/Rime`（快捷操作：点击状态栏输入法图标 ›【用户设定...】）
   * **Linux（Fcitx5-Rime）**：
     `~/.local/share/fcitx5/rime`
   * **Linux（iBus-Rime）**：
     `~/.config/ibus/rime`
3. **重新部署**：
   在系统状态栏或开始菜单中点击 **【重新部署】（Deploy）**，稍等数秒构建完成即可开始使用。

---

### 方式二：Git 克隆 / 软链接（开发者与日常更新推荐）

适合熟悉终端命令、希望后续通过 `git pull` 一键同步更新的用户：

* **macOS（软链接方式）**：
  ```bash
  # 克隆到本地任意目录（例如 ~/Code/rime-crane）
  git clone https://github.com/kchen0x/rime-crane.git ~/Code/rime-crane
  # 创建软链接至 Rime 用户目录
  rm -rf ~/Library/Rime && ln -sif ~/Code/rime-crane ~/Library/Rime
  ```
  *后续更新只需进入该仓库目录执行 `git pull` 并点击重新部署。*

* **Windows（Git 克隆方式）**：
  在 Git Bash 中直接将仓库克隆到用户配置目录：
  ```bash
  git clone https://github.com/kchen0x/rime-crane.git "$APPDATA/Rime"
  ```
  *后续更新进入 `%APPDATA%\Rime` 执行 `git pull` 即可。*

## 进阶配置：小鹤音形 5 码起联想英文单词

小鹤音形原生为**四码定长、顶字上屏**。若你在日常使用中有高频输入英文单词的需求，习惯手动按空格上屏，且不想频繁按 Shift 切换中英文或使用引导前缀：

本项目提供了配套的 Lua 滤镜组件 `lua/xhup/english_len_filter.lua`，可实现**超过 4 码后自动由雾凇英文词库（`melt_eng`）接管并联想英文长词**，同时保证 4 码以内中文候选绝对纯净：

* **1~4 码**：严格屏蔽外部英文候选，中文候选 100% 纯净（例如输入 `like` 仅出中文词「立刻」，输入 `appl` 空码时不提前跳出英文）；
* **≥ 5 码**：音形中文码表自动断码，由雾凇英文词库瞬间接管，流畅联想补全长单词（例如输入 `apple`、`computer`、`application`）；
* **1~4 字母短英文**：日常输入诸如 `git`、`app`、`cpu` 等短词时，打完直接按回车（`Enter`）即可将原始字母直接上屏。

### 开启方式

在你的 Rime 用户配置目录下新建或修改 `xhup.custom.yaml`（模板参见 `xhup.custom.template.yaml`），写入以下内容：

```yaml
patch:
  # 1. 放开最大编码长度，关闭自动顶屏与空码清屏
  speller/max_code_length: 32
  speller/auto_select: false
  speller/auto_clear: none

  # 2. 挂载雾凇英文词库依赖与翻译器
  schema/dependencies/+:
    - melt_eng
  engine/translators/+:
    - table_translator@melt_eng

  # 3. 启用长度过滤滤镜（输入 1~4 码不展示英文，5 码起放行）
  engine/filters/@before 3: lua_filter@*xhup/english_len_filter

  # 4. 配置英文词库联想补全与权重压制
  melt_eng:
    dictionary: melt_eng
    enable_completion: true
    enable_sentence: false
    enable_user_dict: false
    initial_quality: -2
```

保存后，在系统状态栏重新部署（Deploy）Rime 即可生效。
