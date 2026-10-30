set shell := ["bash", "-euc"]
set positional-arguments

# コマンド一覧
default:
    @"{{just_executable()}}" --list

python := env('PYTHON', 'python3')

# 現在のvendorソースからwheelを作成
build:
    {{quote(python)}} -m pip wheel --no-deps --wheel-dir dist .

# vendorの共有ライブラリを開発テスト用にビルド
build-native:
    cargo build --locked --release -p mejiro-native --manifest-path vendor/mejiro-engine/Cargo.toml --target-dir build/just-native

# PYTHONでPlover依存関係を導入済みのPythonを指定可能
test *args: build-native
    MEJIRO_ENGINE_LIBRARY="$PWD/build/just-native/release/libmejiro_native.so" {{quote(python)}} -m unittest discover -s tests "$@"

# プラグインの通常テスト
check: test

# 隣のEngineの現在の作業ツリーをvendorへ同期（build/testは自動実行しない）
sync source='../Mejiro_Engine':
    {{quote(python)}} "$1/tools/sync_plover_engine.py" "$PWD"
