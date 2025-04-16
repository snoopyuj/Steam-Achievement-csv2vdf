> _Author: bwaynesu_  
> _Created: April 16, 2025_  
> _Tags: Python, Steam, CSV, VDF_  

# Steam 成就在地化 CSV 轉 VDF 工具

[English](README.md)

此工具專門用於將 CSV 格式檔案轉換成 Steam 成就在地化所需的 Valve 資料格式（VDF）。協助遊戲開發者管理和更新多國語言的成就翻譯。

<img width="400" src="./Preview//01.png">

## 特色

- 支援任意數量和種類的語言（不限於範例中的四種）
- 將 CSV 檔案轉換為 Steam 成就 VDF 格式
- 自動識別 CSV 檔案標頭和語言欄位
- 支援有無 BOM 的 UTF-8 編碼
- 更新翻譯時保留原有 VDF 檔案結構
- 顯示詳細處理進度和統計資訊
- 可指定輸出檔名以避免覆蓋原始檔案

## 使用方式

### 使用步驟

1. **從 Steamworks 下載 VDF 檔案**
   - 登入您的 Steamworks 開發者帳號
   - 進入您的遊戲頁面，在「編輯商店頁面」選單中找到「成就」
   - 下載現有的成就本地化 VDF 檔案（通常命名為 `xxx_loc_all.vdf`）

2. **依據範本製作 CSV 檔案**
   - 使用 Excel 或其他表格軟體建立 CSV 檔案
   - 第一行必須包含標頭：`ID` 和您需要的語言名稱（例如：`ID,english,schinese,tchinese,japanese,german,french`）
   - 語言名稱必須與 VDF 檔案中的語言區塊名稱相符（通常為小寫）
   - 填入所有成就 ID 與對應的多語言翻譯
   - 儲存為 UTF-8 編碼的 CSV 檔案

3. **執行 Python 程式**
   - 將 VDF 檔案和 CSV 檔案放在同一目錄下
   - 開啟命令提示字元
   - 執行以下指令：`python csv_to_vdf.py 您的CSV檔案.csv 您的VDF檔案.vdf 輸出檔案.vdf`
   - 確認輸出檔案內容無誤後，將其上傳回 Steamworks

### 基本用法

```bash
python csv_to_vdf.py
```

這將使用預設的檔案名稱：
- 輸入 CSV：`Localization.csv`
- 輸入 VDF：`loc_all.vdf`
- 輸出 VDF：`loc_all_update.vdf`

### 指定檔案路徑

```bash
python csv_to_vdf.py input_csv_file.csv input_vdf_file.vdf output_vdf_file.vdf
```

範例：
```bash
python csv_to_vdf.py .\Localization.csv .\loc_all.vdf .\loc_all_update.vdf
```

## CSV 檔案格式

CSV 檔案應包含：
- 包含 "ID" 欄位和語言名稱的標頭列（如 english、schinese、tchinese、japanese）
- 每一列包含成就 ID 及其在不同語言中的翻譯
- ID 欄位通常包含如 "NEW_ACHIEVEMENT_1_0_NAME" 的識別碼

範例：
```
ID,english,schinese,tchinese,japanese
NEW_ACHIEVEMENT_1_0_NAME,First Blood,首杀,首殺,ファーストキル！
NEW_ACHIEVEMENT_1_0_DESC,Defeat 1 enemy in total,累积击败1个敌人,累積擊敗1個敵人,1体の敵を倒す
```

## VDF 檔案格式

VDF 檔案是 Valve 的本地化格式，包含多個語言區塊，每個區塊都有一個包含所有成就 ID 和翻譯文字的 Tokens 段落。

範例：
```
"lang"
{
	"english"
	{
		"Tokens"
		{
			"NEW_ACHIEVEMENT_1_0_NAME"	""
			"NEW_ACHIEVEMENT_1_0_DESC"	""
		}
	}
	"schinese"
	{
		"Tokens"
		{
			"NEW_ACHIEVEMENT_1_0_NAME"	""
			"NEW_ACHIEVEMENT_1_0_DESC"	""
		}
	}
	"tchinese"
	{
		"Tokens"
		{
			"NEW_ACHIEVEMENT_1_0_NAME"	""
			"NEW_ACHIEVEMENT_1_0_DESC"	""
		}
	}
	"japanese"
	{
		"Tokens"
		{
			"NEW_ACHIEVEMENT_1_0_NAME"	""
			"NEW_ACHIEVEMENT_1_0_DESC"	""
		}
	}
}
```

## 注意事項

1. CSV 檔案應以 UTF-8 編碼（可帶有或不帶有 BOM）
2. 程式會保留 VDF 檔案的原始結構，只更新翻譯內容
3. 如果在 VDF 檔案中找不到 CSV 檔案中的某個 ID，程式會顯示警告訊息
4. CSV 中的項目順序不需要與 VDF 相符（例如，不需要將所有 NAME 項目列在所有 DESC 項目之前）

## 客製化設定

要進一步調整程式功能，您可以修改 `csv_to_vdf.py` 檔案：

- 增強錯誤處理：例如在 VDF 中找不到項目時自動新增