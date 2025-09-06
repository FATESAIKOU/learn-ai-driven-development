# Agentinput Readme

本專案旨在建立一個大語言模型專用的程式設計專用的基底。

主要功能如下：
1. 根據需求執行程式碼開發
2. 開發過程中自主調整目前的上下文 並輸出上下文

## 專案結構

主要結構如下
```
.
├── 01.agentContextV1
|   ├── prompt # 開發時實際要進行的流程指示 ai agent 不可以更改
|   ├── memory # 開發過程中 ai agent 可以調整的上下文, ai agenet 自行創建
|   └── action # 開發過程中針對使用者的回饋 ai agent 自行創建的可執行動作與方式
├── 02.tasks
```

※ 各資料夾內都會存在 agentinput-* 的檔案，讀取時請每次都參考並理解裡面的內容
※ 檔案結構以及 agentinput-* 的檔案內容都不可變，其他你可以自由調整
※ 針對各專案專用的 prompt/memory/action 知識你可以輸出在 02.tasks/<專案名稱>/memory 內
※ 所有你產生的檔案避免使用 agentinput-* 的檔案名稱，以免覆蓋

## 開發方式

0. 我會指定你要開發 02.tasks 的某一個專案
1. 參考 01.agentContextV1 資料夾內的說明
2. 參考 02.tasks 內的對應專案資料夾
3. 開發
    3-a. 你可以自由調整 01.agentContextV1 資料夾內的內容
    3-b. 實現專案 測試 要求 review...等