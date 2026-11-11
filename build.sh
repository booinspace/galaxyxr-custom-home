#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/Library/Android/sdk}}"
BT="$SDK/build-tools/35.0.0"
for f in "$BT/aapt2" "$BT/zipalign" "$BT/apksigner" "$SDK/platforms/android-35/android.jar"; do
    [ -f "$f" ] || { echo "Missing $f; install Android SDK Platform 35 and Build Tools 35.0.0." >&2; exit 1; }
done
for tool in python3 keytool unzip; do command -v "$tool" >/dev/null || { echo "Missing $tool" >&2; exit 1; }; done
mkdir -p build
stock="${STOCK_APK:-}"
if [ -z "$stock" ]; then
    command -v adb >/dev/null || { echo 'Install adb or set STOCK_APK to a local stock Snow APK.' >&2; exit 1; }
    stock_path=$(adb shell pm path com.google.environments.snow | tr -d '\r' | sed -n 's/^package://p' | head -n 1)
    [ -n "$stock_path" ] || { echo 'Stock Snow package not found. Set STOCK_APK to a saved stock Snow APK.' >&2; exit 1; }
    adb pull "$stock_path" build/stock.apk >/dev/null
    stock=build/stock.apk
fi
# Remove stale variants/assets, while retaining the signing key for updates.
rm -rf build/assets
python3 generate.py build/assets
unzip -p "$stock" assets/resources/snow/day/snow_day.zip > build/assets/resources/snow/day/lighting.zip
[ -s build/assets/resources/snow/day/lighting.zip ] || { echo 'Stock lighting archive missing.' >&2; exit 1; }
unzip -tq build/assets/resources/snow/day/lighting.zip
"$BT/aapt2" link -o build/unsigned.apk -I "$SDK/platforms/android-35/android.jar" --manifest AndroidManifest.xml -A build/assets -0 glb -0 zip -0 png
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk
if [ ! -f build/debug.keystore ]; then
    keytool -genkeypair -keystore build/debug.keystore -storepass android -keypass android -alias blackhome -dname 'CN=Black Home Debug' -keyalg RSA -keysize 2048 -validity 10000
fi
"$BT/apksigner" sign --ks build/debug.keystore --ks-pass pass:android --key-pass pass:android --ks-key-alias blackhome --out build/black-home.apk build/aligned.apk
"$BT/apksigner" verify --verbose build/black-home.apk
"$BT/zipalign" -c 4 build/black-home.apk
printf '\nBuilt build/black-home.apk\n'
