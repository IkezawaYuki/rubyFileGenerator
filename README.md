========== ========== ==========

  README  ver.1.0.0

========== ========== ==========

【 ソフト名 】entrance<br>
【 製 作 者 】kawahara_r, ikezawa_y<br>
【  種  別  】社内ツール<br>
【 開発環境 】pycharm<br>
【 動作環境 】windows<br>
【バージョン】4.0.1<br>
【最終更新日】2019-02-12<br>
【ファイル名】rubyGenerator<br>
<br>
---------- ----------
◇ 概要 ◇<br>
インターフェースオーダー定義書からRubyスクリプトとbatファイルを生成します。<br>
2019年2月時点で、「ファイル削除」のみ対象外となっています。<br>
<br>
◇ 動作条件 ◇<br>
HUE_API_KICK内に以下のように配置することで動作します。<br>
HUE_API_KICK/ <br>
　├ bat/ <br>
　├ config/<br>
　├*entrance/<br>
　│　├ *template/<br>
　│　└ *entrance.exe/<br>
　├ filein/<br>
　├ fileout/<br>
　├ filewk/<br>
　├ logs/<br>
　├ result/<br>
　├ ruby/<br>
　└ source/<br>

<br>
◇ デプロイ ◇<br>
    本ツールは「pyinstaller」を使用しています。
    pyinstaller が入っていない場合は、pipコマンドにてダウンロードしてください。<br>
        pip install pyinstaller<br>
    entrance.py があるファイル階層にて、以下のコマンドを実行してください。<br>
        pyinstaller entrance.py --onefile --icon="entrance_image.ico"<br>
    上記のコマンドを実行することでdistフォルダ内にexeファイルが生成されます。<br>
    templateフォルダは別途用意する必要があります。プロジェクトのtemplateフォルダをそのままコピーしてください。<br>
    ・entrance.exe<br>
    ・templateフォルダ<br>
    この二つを上記の◇動作条件◇に合うよう配置してください。<br>
    
<br>
◇ つかいかた ◇<br>
　　entrance.exeをダブルクリックして起動します。<br>
　　ファイル選択ダイアログが立ち上がるので、インターフェースオーダー定義書を選択します。<br>
　　確認ダイアログで「OK」を押すと処理が開始されます。<br>
　　「batフォルダ」「sourceフォルダ」以下にbatファイルとrubyスクリプトがそれぞれ出力されます。<br>
<br>
◇ 免責 ◇<br>
　　実行の際に確認を怠ったことにより発生した利用者の損害に関しては<br>
　　製作者は一切責任を負いません。<br>

<br>
◇ 転載 ◇<br>
   転載はご自由にどうぞ。許可不要、著作権表記も不要。<br>

◇ FAQ・既知のバグ ◇<br>
<br>
