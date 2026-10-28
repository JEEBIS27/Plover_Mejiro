# Rustエンジンとの接続

Plover版は Mejiro_Engine の Rust コアで変換します。Pythonの役割は辞書検索、Ploverの確定履歴への状態保存、キー出力、マクロの出力記録です。
母音・例外かな・活用・助詞・ローマ字/JIS変換はRust側だけで管理します。

## インストール

Windows 64bitではDLL同梱のwheelを配布します。利用者側のRust/Cargo、Visual Studio Build Toolsは不要です。

1. [READMEの導入法](../README.md#導入法installation)に従い、配布された `*-py3-none-win_amd64.whl` をPloverの `plover_console.exe -s plover_plugins install --upgrade` でインストールして再起動します。
2. Configure → Pluginsで `mejiro_engine` 拡張を有効にします。
3. SystemでMejiroを選択します。既存の `mejiro.py` 辞書はそのまま使えます。
4. 過去の `mejiro_commands.json` をコピーして独自管理している場合は、標準コマンドをRust側で扱うためそのコピーを無効にします。配布する同名JSONは空です。

拡張が無効なら、日本語変換を黙ってPythonへ戻さず、拡張を有効にするようエラーで案内します。

## wheelのビルド・配布

`.github/workflows/wheels.yml` はWindows x64上でRustエンジンをビルドし、DLL同梱wheelを生成します。Pythonのバージョンに依存しないctypes接続なので、wheelのタグは `py3-none-win_amd64` です。

- 手動配布: GitHubのActions → Windows wheel → Run workflowで配布元のブランチを選びます。成功した実行のArtifactsから `mejiro-windows-x64-wheel` をダウンロードし、ZIPを展開して中の `.whl` を渡します。
- リリース配布: `setup.cfg` のバージョンと一致するタグ（例: `v2.8.1`）のGitHub Releaseを公開すると、自動ビルド・検証後にwheelがAssetsへ追加されます。このワークフローを含むコミットにタグを付けてください。過去に公開済みのReleaseには自動で追加されません。
- Pull RequestでもWindows上のビルドとwheelの検証を実行します。

検証はwheel内のDLLを確認したうえで、一時ディレクトリへwheelをソースビルドなしでインストールし、同梱DLLのロード・ABI確認・`KI-` → `き` の変換を実行します。Plover GUIや実機での入力確認は別途必要です。

## ソースからのインストール（開発者向け）

Rust 1.88以上とCargo、対応するCリンカーが必要です。WindowsではMSVCおよびWindows SDKを含むVisual Studio Build Toolsが必要です。Plugin Managerの「GIT」もこのソースビルドに該当します。

## エンジンの編集・同期

編集元は Mejiro_Engine です。ここの `vendor/mejiro-engine` はビルド用の生成コピーなので直接編集しません。

```sh
cd /path/to/Mejiro_Engine
python tools/sync_plover_engine.py ../Plover_Mejiro
cd ../Plover_Mejiro
python -m pip wheel --no-deps .
```

生成されたwheelをPloverのPython環境へインストールし、Ploverを再起動します。
同梱ソースからCargoがライブラリをビルドし、wheel内の `Mejiro/_native/` に格納します。
必要な変更はRustの1か所だけで、Pythonの定義表を更新する必要はありません。

開発時は `MEJIRO_ENGINE_SOURCE=/path/to/Mejiro_Engine` を指定してwheelをビルドできます。
ソースからのテストでは `MEJIRO_ENGINE_LIBRARY=/path/to/Mejiro_Engine/target/debug/libmejiro_native.so` を指定できます。
macOSではdylib、WindowsではDLLを指定します。

## 辞書照会と確定出力

辞書検索はRustの純粋なプレビューで入力の妥当性だけ確認し、状態を変更しません。
有効な入力は未解決のマーカーを返します。拡張が確定出力の直前に直前の履歴スナップショットをRustへ渡し、出力と次の状態を取得します。
取り消しや複数ストロークのユーザー辞書による置換では、Plover自身の履歴に従って状態も復元されます。
記録・再生するマクロは解決済みのPlover出力を保存するため、助詞を再判定しません。

旧Pythonルールのファイルはソースチェックアウトで移行比較用に残していますが、実行経路から参照せずwheelにも含めません。
