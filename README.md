# サイトURL
https://nlp-python-flask.herokuapp.com

# 注意点
テキストを入力してAnalyzeボタンを押すとInternal Server Errorが出力される場合があります。その場合は何回かページを更新すれば正しく表示されます。

# 使用技術
フロントエンド: HTML/Bootstrap  
Webフレームワーク: Flask(Python)  
ライブラリ: Spacy, Displacy, NLTK, Sklearn, googletrans, flask, werkzeug, etc.  
データベース: SQLite3. Column=[email, username, passward(hash), total_volume] total_volume=調べた文章に含まれる単語数の合計  
デプロイ: Heroku  

# 機能
データベース: 登録、登録内容変更、ログイン、パスワードリセット、ログアウト、単語数更新  
自然言語処理: エンティティー解析、感情分析(全体+文章ごと)、翻訳、単語数表示  

# 使用法
1. Register, Login: ナビゲーションバーのRegisterをクリックしてEmail, Username, passwardを入力して登録(emailは架空のもので良い)。ボタンを押すとログイン画面に推移するのでログイン  
2. NLP: テキストフォームのところに解析したい文章を入力し、Analyzeをクリック  
3. 結果表示: (注意点に留意)正しく表示されたら終了。
4. Account: ナビゲーションバーのAccountをクリックすると、それまでで調べた文章に含まれる単語数の合計と、email, username情報が見れる。登録内容はここで変更可能  
