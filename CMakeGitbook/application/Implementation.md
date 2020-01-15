## 実装

この節では、[対処法](/application/solutions.md) の実装に関する補足事項を述べます。

** ソースファイルの整合性 **

"CMakeLists.txt" に組み込みます
 ("CMakeSettings.txt" の SPR_PROJS で定義したプロジェクトのすべてを
`add_subdirectory` します)。
"CMakeLists.txt.Dev.dist" を参照のこと。

** ビルドの最適性 **

組み込まれる Springhead Library の各プロジェクトに対して、
次のことを実施します (ここでは Base を例にします)。

cmake (configure) 実行時に作成されるオブジェクト格納ディレクトリ
 "C:/Develop/Application/*build*/Base/Base.dir" を、
オブジェクト共通格納場所
 "C/Springhead/core/src/Base/<platform>/<VS-Version>/Base.dir" への link (\*) に
すげ替えます。

オブジェクト共通格納場所は、Springhead Library の cmake (configure) 時に作成します。
各プロジェクトの "CMakeLists.txt" から execute_process で呼び出される
 "make_prconfig.py" を参照のこと。

> (\*) で作成する link は、unix では symbolic link、Windows では junction です。
これは、Windows では通常の実行権限では symblic link が作成できないためです。

> Windows では、"Base.dir" が junction なのか通常のディレクトリなのかが、
 explorer でも command prompt でも区別がつきません。
このことが、[Q&A](/application/QandA.md) の *ビルドの最適性が崩れる* の原因究明を
困難にする可能性を孕んでいます。
ここでは、オブジェクト共通格納場所には "\_target\_body\_" という名前の空ファイルを
置くことで判定の補助としています。

** プロジェクトファイルの整合性 **

アプリケーションのソリューションファイルに追加したターゲット sync が
次の処理を順に実行します。

1. もしもアプリケーション側のプロジェクトファイルの内容と Springhead Library 側の
プロジェクトファイルの内容とが異なっていたならば、
アプリケーション側のプロジェクトファイルを Springhead Library 側にコピーする。
これは、アプリケーション側でソースファイル構成を変更 (追加・削除) を行ない、
Visual Studio 上でプロジェクトファイルを保存したとき、
またはアプリケーション側で再度 cmake を実行した場合です。

1. アプリケーション側のプロジェクトファイルを Springhead Library 側のプロジェクト
ファイルへの link とする。

ターゲット sync は、アプリケーションの "CMakeLists.txt" で
 add_custom_target として作成されます。
また、このターゲットはアプリケーションのビルドにおいて
必ず最初に実行されるように依存関係が設定されます。
"CMakeLists.txt.Dev.dist" および "make\_sync.py" を参照のこと。

