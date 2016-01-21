## 概要

DBのschemeからモデル駆動で、Flask appを生成する。  
生成されるappは、堅く軽量で、規模に問わず開発者を制約しない汎用性・拡張性の高い設計にする。（したい。）

## 設計思想

プログラムが書くべきコードはプログラムが書く。恣意的な判断が必要なところだけ人間が書く。  
（ビルダに知能を載せるところまではやらない。）  

このビルダでは、以下の2点に開発者が注力できるようにする。  
* データモデリング
* データ層とユーザ層をつなぐプログラムの分類・設計・実装

具体的には、DBの設計と、Model-Service層の構築が相当する。  
他の部分はできるだけ自動生成できるようにする。

## 仕様

DB設計を入力として、appのパッケージやデータ層を主としたソースコードを生成する。ファイルによっては、update/rewriteもする。  


/builder/app_recipe.py に、app のビルド情報やモデルの参照先を記述し、以下のコマンドを入力することで app の書き出し/更新を行う。

```
python src/run.py init
```

書き出されるソースの詳細は、[生成対象](#生成対象)を参照。  

以下、生成されるパッケージの概念仕様。

* Model / Table  
SQL-Alchemyのテーブル定義。自動生成/更新される。

* Model / DAO  
各単一のテーブルに対する処理が記述される。ベースファイルが1度だけ生成される。

* Model / Service  
複数のテーブルにまたがるデータの操作や、外部APIとの連携、データの整形などを担当する。  
データ層とユーザ層の隔たりは、この層の設計によって吸収される。したがって、ビルダはこの層の分類や継承関係を制約しない。  
ベースファイルが1度だけ生成される。

* Controller  
各ルーティング、入力チェック、Service層を利用したレスポンスの生成を担当する。
ベースファイルが1度だけ生成される。

各概念を呼び出す関係は、以下のようになる。

```
Controller use Service
Service use DAO, Table
DAO use Table
```

## 生成対象

[+] で記されるファイルが、ビルダによって生成されるファイルで、[rewrite]が付加されているファイルは更新も行われる。  
モデルの変更があった場合はビルダを起動して更新し、DAOやService層の変更が必要な箇所だけ開発者が実装する。

```
- run.py
+ app.wsgi
+ webconfig.py
+ webconfig_local.py
+ webconfig_master.py
- classes
  + __init__.py
  + controller
    + __init__.py [rewrite]
    + [each_controller].py
  + model
    + __init__.py [rewrite]
    + _settings.py
    + dao
      + __init__.py [rewrite]
      + [each_dao].py
    + service
      + __init__.py [rewrite]
      + [each_service].py
    + table
      + __init__.py [rewrite]
      + [each_table].py [rewrite]
```

## Required

ビルダの入力やコードの生成には、Flask自身に必要なSQL-AlchemyとJinja2を利用する。

```
pip install Flask
pip install SQLAlchemy
pip install mysql-python
```

## Practice

[Required](#required)のパッケージが入っているかを確認する。

練習用の app のプロジェクトディレクトリを作成し、app_builder の src ディレクトリ以下をコピーする。  
以下のようなディレクトリで作業を進める。
```
TestApp/src/classes
```

/builder/app_recipe.py を編集し、app で使いたいDBのschemeを以下のように指定する。  
パスワードはビルダを run するときに聞かれるので、ここには記述しない。

```
# /builder/app_recipe.py

DB_DEV_USER = 'user'
# such DB_DEV_PASS should not be in this file. pass-input will be required in app-build.
DB_DEV_HOST = 'localhost'
DB_DEV_SCHEME = 'scheme_name'
```

テスト用に、Controller と Service の設定も記述しておく。

```
# /builder/app_recipe.py

controllers_recipe = [ { 'name': 'public' } ]

model_services_recipe = [ 'test' ]
```

この段階で git などにコミットしておくと、ビルダが書き出したソースの差分を確認しやすい。  
以下のコマンドで、ビルダを起動する。

```
python src/run.py init
```

設定に問題がなければ、パッケージやソースファイルが生成されている。  
上記の記述と同様であれば、controller/public_c.py が生成されているので、以下のように書き換えてみる。

```
# /controller/public_c.py
...

@public_bp.route('/', methods=['GET', 'POST'])
def public_index():
    
    return render_template('index.html')
```

今度は、app を起動してみる。

```
python src/run.py
```

動作確認できたら、Service層を実装してControllerから呼び出せば、一通りの実装の流れを確認したことになる。  
app を別環境で動かしたり、wsgi を通す際は、app_recipe の DB_MASTER_XXX, ON_MASTER_XXX, などの変数を設定すればよい。

## ToDo

* Column-Typeの対応を増やす
* DAOのコード生成をもう少しやってあげる
* ログ集計のサポート
* S3, Redis統合のレシピを増やす
* rewrite-ignore 機能

## できたらやりたい

* joinクエリの自動生成・自動最適化
* Pyramid版
* 知能載っけて、ばーんどかーんやったー

