========== ========== ==========

  README  ver.1.0.0

========== ========== ==========

【 ソフト名 】entrance
【 製 作 者 】kawahara_r, ikezawa_y
【  種  別  】社内ツール
【 開発環境 】pycharm
【 動作環境 】windows
【バージョン】4.0.1
【最終更新日】2019-02-12
【ファイル名】rubyGenerator

---------- ----------
◇ 概要 ◇
インターフェースオーダー定義書からRubyスクリプトとbatファイルを生成します。
2019年2月時点で、「ファイル削除」のみ対象外となっています。

◇ 動作条件 ◇
HUE_API_KICK内に以下のように配置することで動作します。
HUE_API_KICK/
　├ bat/
　├ config/
　├*entrance/
　│　├ *template/
　│　└ *entrance.exe/
　├ filein/
　├ fileout/
　├ filewk/
　├ logs/
　├ result/
　├ ruby/
　└ source/


◇ デプロイ ◇
    本ツールは「pyinstaller」を使用しています。
    pyinstaller が入っていない場合は、pipコマンドにてダウンロードしてください。
        pip install pyinstaller
    entrance.py があるファイル階層にて、以下のコマンドを実行してください。
        pyinstaller entrance.py --onefile --icon="entrance_image.ico"
    上記のコマンドを実行することでdistフォルダ内にexeファイルが生成されます。
    templateフォルダは別途用意する必要があります。プロジェクトのtemplateフォルダをそのままコピーしてください。
    ・entrance.exe
    ・templateフォルダ
    この二つを上記の◇動作条件◇に合うよう配置してください。
    

◇ つかいかた ◇
　　entrance.exeをダブルクリックして起動します。
　　ファイル選択ダイアログが立ち上がるので、インターフェースオーダー定義書を選択します。
　　確認ダイアログで「OK」を押すと処理が開始されます。
　　「batフォルダ」「sourceフォルダ」以下にbatファイルとrubyスクリプトがそれぞれ出力されます。

◇ 免責 ◇
　　実行の際に確認を怠ったことにより発生した利用者の損害に関しては
　　製作者は一切責任を負いません。


◇ 転載 ◇
   転載はご自由にどうぞ。許可不要、著作権表記も不要。

◇ FAQ・既知のバグ ◇

