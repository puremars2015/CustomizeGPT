# 開始前的需知

1. venv如果用copy的,會很容易造成錯誤,因為venv產生的時候會跟當時的路徑有關,如果copy到新的位置,就會出錯

# 安裝flask

1. 安裝虛擬環境
```
python -m venv .venv
```
2. 重開terminal 看到有切到venv,再開始操作

如果沒有,可以直接執行
```
.venv\Scripts\activate
```
3. 安裝flask 套件
```
pip install flask
```
4. 安裝requests
```
pip install requests
```
# 網頁,js的控制

1. app.py
提供API串接跟資料存儲

2. index.html
控制畫面

- 不含css的畫面

- ![不含css的畫面會像](https://github.com/puremars2015/CustomizeGPT/blob/main/source/%E4%B8%8D%E5%90%ABcss%E5%8A%9F%E8%83%BD%E7%95%AB%E9%9D%A2.png)

- 注意 html上的id, 只能有一個,超過會容易出錯



# call api 

1. 畫面call自己的後端api

2. 後端去call gemini的api或chatgpt的api

# 組裝成一個客製版的chatgpt的效果


