# 教科書轉科普漫畫生成器 (Textbook-to-Manga Skill)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://github.com/geniefu/textbook-to-manga)

專為教育工作者、教材研發人員與自學者打造的 **Antigravity / Claude 智慧技能**。  
能將中學至高中艱澀的教科書章節（PDF 或純文字），自動轉化為富有吸引力、教學深度與幽默感兼具的直式 A4 全彩日系科普漫畫，並一站式產出獨立圖片與適合平板閱讀的 PDF 電子書！

---

## 🌟 核心特色

1. **章節知識點深度鎖定**：自動剖析課本內容，精準提煉必考概念、單位換算、實驗探究與易錯陷阱。
2. **角色設定彈性自由**：支援使用者彈性自訂動漫主角（預設為深受學生喜愛的「哆啦A夢與大雄」系列，亦可指定名偵探柯南、寶可夢或原創校園角色）。
3. **8～15 頁彈性篇幅規範**：依照知識點多寡量身規劃 3～4 格漫畫分鏡，兼顧教學完整性與閱讀節奏。
4. **提示詞加固原生繪製（Prompt Hardening & Native Rendering）**：
   * **12 字短句鐵則**：每句嚴格控制在 12 字以內口語短句（黃金 5～9 字），徹底杜絕模型因長句發散導致的缺字、漏筆畫、結巴重複與雙生氣泡。
   * **絕對空間與角色錨定**：提示詞中精確鎖定方位（如 `Upper-left for Gian`、`Lower-right for Doraemon`），確保對白氣泡指針完全吻合角色，角色台詞絕不顛倒。
   * **預留器材與氣泡安全區**：角色位於中下景、上方預留留白空間，**保證對白氣泡絕不遮擋人物表情與關鍵實驗器材**（天平、量筒、數值螢幕）。
   * **拒絕後製白塊貼補**：堅持原生一體成型，氣泡黑線框與對應指針隨圖自然生成，絕無突兀的後製方塊補丁。
5. **發行級封底設計標準**：
   * 封底包含全員同慶揮手插圖、排版精緻的「★ 核心理化重點秘笈 ★」條列整理卡與真實感 ISBN 條碼。
6. **兩段式配額容錯管理（Two-Stage Quota Resilience）**：
   * **階段一（文本先行）**：遇到 AI 繪圖模型配額限制時，完整劇本、分鏡與提示詞 100% 寫入手冊保存，並先行後製已生出的圖片。
   * **階段二（無縫續跑）**：配額重置後自動無縫接續完成剩餘頁面。
7. **發行級自動化後製（Python 內建）**：
   * 抹平 AI 產生的邊角印刷標記（如 A4、A5、21）。
   * 去除封面封底樣機的織布/木紋/立體陰影，一律修復為專業純白背景。
   * 底部中央自動排版並印刷清晰阿拉伯數字頁碼。
8. **平板專用電子書打包**：一鍵輸出最適配 iPad / Android 平板全螢幕翻頁閱讀與紙本雙面列印的高畫質向量 PDF。

---

## 📂 專案結構

```
textbook-to-manga/
├── SKILL.md                 # 核心技能規範、分鏡範本、Prompt 模板、加固規則與兩段式容錯機制
├── README.md                # 專案介紹與使用說明
├── requirements.txt         # Python 相依套件 (Pillow, numpy, etc.)
├── LICENSE                  # MIT 授權條款
├── .gitignore               # Git 忽略檔案清單
└── scripts/
    ├── postprocess_manga.py # 自動化後製修復（去雜訊、去底布、純白背景、加置中頁碼）
    └── compile_pdf.py       # 自動打包平板閱讀高畫質 PDF 電子書
```

---

## 🚀 快速安裝與使用

### 1. 安裝技能
將本專案複製至您的 Antigravity / Claude 技能目錄下：
```bash
git clone https://github.com/geniefu/textbook-to-manga.git ~/.gemini/config/skills/textbook-to-manga
```

### 2. 安裝 Python 依賴
```bash
pip install -r requirements.txt
```

### 3. 對話中調用技能
在與 Antigravity 對話時，只需輸入類似指令：
* 「請使用 `/textbook-to-manga` 將第 1 章基本測量轉成漫畫。」
* 「請把教材電子書的 1-2 章節改編成科普漫畫，以哆啦A夢和大雄為主角，每句限制在12字以內短句。」

---

## 🛠️ 內建輔助腳本手動執行

### 1. 圖片後製清洗（純白背景、除雜訊、上頁碼）
```bash
python scripts/postprocess_manga.py --folder "路徑/CH1-2"
```

### 2. 打包平板電子書 (PDF Compilation)
```bash
python scripts/compile_pdf.py --folder "路徑/CH1-2" --title "質量與密度的測量"
```

---

## 📄 授權條款
本專案採用 [MIT License](LICENSE) 授權。
