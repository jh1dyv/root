## Q&A

前項 ([ビルドの準備](/application/Preparation.md)) に従って作成したアプリケーション
に関する Q&A 集です。
以下 Springehead Library の Base プロジェクトを例にとって説明しますが、
他のプロジェクト (Collision, Foundation, ...) についても同様です。

> unix 上で Springhead Library とアプリケーションの並行開発を行なうことはないと
思われますので、ここでは Windows 上で Visual Studio を使う場合について説明します。

----
** ソリューションファイルに新しいターゲットがある **

** ALL_BUILD **

これは CMake が自動的に作成するターゲットで、make all に相当するものとされています。
ただし Visual Studio 上では ALL_BUILD の依存関係の設定が不正確で、
このターゲットをビルドしても正しい結果は得られないようです。
**このターゲットは無視してください**

** sync **

これはプロジェクトファイルの整合性を保つために作られたターゲットで、
他のターゲットをビルドすれば自動的にこのターゲットが最初に実行されます。
** このターゲットに対して何らかのアクションを起こす必要はありません。 **

----
** ディレクトリが作成できないエラーが発生する **

Springehad Library をビルドすると、ソースツリー上に
*"C:/Springhead/core/src/Base/x64/15.0/Base.dir"*
というディレクトリが作成されます ( *x64*, *15.0* の部分は環境により異なります)。

アプリケーションの cmake をした後で上記のディレクトリを削除すると、
以降のビルドで
*“エラー MSB3191 ディレクトリ "Base.dir/Debug/" を作成できません”*
などというエラーが発生します。

また、Springhead Library 側で cmake (configure) を実行していないと
上記のディレクトリが作成されていないため、同じエラーが発生します。

**このような状態を解消するためには、アプリケーション側または Springhead Library 側
で再度 cmake を実行する必要があります。**

----
** ビルドの最適性が崩れる **

アプリケーション側で *"C:/Develop/Application/*build*/Base.Base.dir"* などを削除すると、
ビルド時に Visual Studio が *build* 下に "Base.dir" を自動的に作成してしまうために
ビルドの最適性が崩れてしまいます。

> 無駄なビルドが発生するだけで、ビルド自体は正常に行なえます。<br>
“ビルドの最適性”については [問題点](/application/Problems.md) を参照してください。

**このような状態を解消するためには、アプリケーション側または Springhead Library 側
で再度 cmake を実行する必要があります。**

----
** sync configuration でファイルオープンエラーが発生する **

Springhead Library 側で "*build*/Base" 下にあるプロジェクトファイル "Base.vcxproj" を
削除すると、sync ターゲット実行で link 先のファイルが見つからずに

```
1>sync configuration with C:/Springhead/core/src
　　：
1>Error : file open error : "Base/Base.vcxproj"
1>Traceback (most recent call last):
1>  File "C:/Springhead/core/src/cmake_sync.py", line 332, in <module>
1>    spr_org_guids = collect_vcx_guid(spr_blddir, projs)
1>  File "C:/Springhead/core/src/cmake_sync.py", line 134, in collect_vcx_guid
1>    guids[proj] = guid.popleft()
```
のようなエラーが発生します。

**この状態を解消するためには、Springhead Library 側で再度 cmake を実行する
必要があります (アプリケーション側では駄目)。**

