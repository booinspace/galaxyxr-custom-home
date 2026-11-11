# Black Home for Samsung Galaxy XR

A minimal black Home Space environment: an unlit, double-sided black cube around the viewer, with black thumbnails. No root required. The APK contains assets and discovery metadata, with no executable app code or app screen.

**Status:** built, signature-checked and installed on a Galaxy XR on 11 November 2026. The owner reported it working after removing the stock Snow package for user 0 and restarting Home. Compatibility with other firmware and headsets is unverified. This is an experimental community format, not an official Samsung SDK.

## Install the released APK

1. Download `black-home.apk` and `SHA256SUMS` from [Releases](https://github.com/booinspace/galaxyxr-custom-home/releases). On macOS, check the download with `shasum -a 256 -c SHA256SUMS` in the download folder.
2. Enable Developer options and USB debugging on the Galaxy XR, connect it to your computer and authorize the debugging prompt. Install Android SDK Platform Tools so `adb` is on your PATH.
3. Confirm `adb devices` shows your headset as `device`, then install:

   ```sh
   adb install -r black-home.apk
   ```

4. Open **Settings → Home environment** on the headset and select **Black Home**, then **day** if offered. There is no app icon to launch.

### If Black Home does not appear

This environment uses the launcher's recognized `snow` identifier. The stock Snow environment can take that slot. The following removes Snow **for user 0 only**; its system APK remains available for restoration. Run this only if you want Black Home to replace that slot:

```sh
adb shell pm uninstall --user 0 com.google.environments.snow
adb shell am force-stop com.samsung.android.app.xr.home
adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME
```

Reopen the environment picker and select Black Home. These steps resolved discovery on the owner's headset. They assume the normal primary Android user is user 0.

### Restore Snow / remove Black Home

```sh
adb shell cmd package install-existing --user 0 com.google.environments.snow
adb uninstall boo.puppy.blackhome
```

If selecting the environment causes repeated Home crashes, keep ADB connected and run `adb uninstall boo.puppy.blackhome`, then restore Snow as above. Select a stock environment again if needed.

## Build on macOS

Prerequisites:

- Python 3, a JDK providing `java` and `keytool`, and `unzip`.
- Android SDK **Platform 35** and **Build Tools 35.0.0**. Install through Android Studio's SDK Manager, or an existing `sdkmanager`:

  ```sh
  sdkmanager "platforms;android-35" "build-tools;35.0.0" "platform-tools"
  ```

- Set `ANDROID_HOME` to the SDK directory if it is not `~/Library/Android/sdk`.
- A connected, authorized headset with stock `com.google.environments.snow` available, or a saved copy of that stock APK. With multiple ADB devices, set `ANDROID_SERIAL` to the intended headset's serial.

```sh
git clone https://github.com/booinspace/galaxyxr-custom-home.git
cd galaxyxr-custom-home
./build.sh
python3 test_assets.py build/black-home.apk
adb install -r build/black-home.apk
```

The script generates the GLB, PNG thumbnails and XML, pulls the stock Snow APK read-only, extracts its day lighting ZIP, packages uncompressed binary assets, aligns the APK and signs/verifies it. It does not install anything or change headset settings. Output: `build/black-home.apk`.

To build without a connected headset, provide an absolute path to a stock Snow APK previously pulled from your own device:

```sh
STOCK_APK=/absolute/path/to/stock-snow.apk ./build.sh
```

Save that APK **before** removing Snow for user 0; afterwards `pm path` may not find it. The script deliberately stops if the stock package or expected lighting archive is missing. No stock APK or signing key is committed to this repository.

### Signing and updates

The first build creates `build/debug.keystore` (alias `blackhome`, password `android`). Preserve it privately for subsequent updates; rebuilding with another key cannot update an installed package. This is a personal-testing key, not a production signing setup.

The downloadable v1.0.0 APK is the original signed build installed during development, not a newly signed replacement. Fresh clones generate a different key and will generally produce different APK bytes. If Android reports `INSTALL_FAILED_UPDATE_INCOMPATIBLE` when switching from the release to your own build, uninstall `boo.puppy.blackhome` first, then install your build. Do not publish your private keystore. The build recipe is repeatable with the same stock input and tools; byte-for-byte reproducibility of signed APKs is not claimed.

## Package layout

```text
AndroidManifest.xml                                  boo.puppy.blackhome; vst.3d.environment=true
assets/environment_list.xml                          catalogue; name=snow
assets/resources/snow/environment_information_jxr.xml descriptor; single day variant
assets/resources/snow/day/black.glb                   generated unlit black cube
assets/resources/snow/day/black.png                   generated black thumbnail
assets/resources/snow/day/lighting.zip                stock snow_day.zip lighting archive
assets/resources/snow/thumbnail/snow_thumb.png         generated picker thumbnail
```

`generate.py` uses only Python's standard library. The manifest declares `hasCode=false`, min SDK 26 and target SDK 34. Platform 35 supplies the build-time framework. The descriptor omits the stock `auto` variant: the community guide reports that a variant without a model can crash-loop Home.

Run `python3 test_assets.py` without an SDK or headset to check generated XML references, GLB structure/material/geometry, and black PNG pixels/CRCs. An optional APK argument additionally checks asset parity, ZIP integrity, uncompressed binary assets and absence of DEX code. `build.sh` runs Android signature and alignment checks.

## Limits

Check the actual scene by switching from a visibly different stock environment and looking in all directions. The community guide reports silent fallback to the previous environment when a model cannot load, so a black thumbnail alone is not proof of success. Windows, borders and safety overlays can remain visible. This project does not establish that display pixels are electrically off, hide window borders or supply fullscreen behavior to apps.

## Credits and provenance

- **u/nazga — [Adding custom home environments](https://www.reddit.com/r/Galaxy_XR/comments/1w90k6v/adding_custom_home_environments/):** the primary implementation guide for APK discovery, accepted environment identifiers, slot collisions, asset layout, unlit materials and recovery. Launcher behavior is reported community research, not a stable public API.
- **[BlueScorpioVR/galaxyxr-modules](https://github.com/BlueScorpioVR/galaxyxr-modules):** related Galaxy XR customization work consulted in the original investigation. Its rooted window modules are separate from this environment; no module code is copied or required here.
- **[compdoge/gxr-ghostlock](https://github.com/compdoge/gxr-ghostlock):** consulted during separate root/window-customization research in the original session. It is not the source of Black Home, and no code or binaries from it are used here. Black Home requires no rooting tool.
- **Google / Samsung stock Galaxy XR Snow environment:** catalogue and JXR descriptor structure were inspected on the owner's headset. The build extracts `assets/resources/snow/day/snow_day.zip` from that package for lighting. The released APK includes that stock lighting archive; those vendor assets remain their owners' work. The full stock APK is excluded from source control.
- **[Khronos glTF](https://github.com/KhronosGroup/glTF)** defines GLB and `KHR_materials_unlit`; **[Android SDK tools](https://developer.android.com/tools)** provide ADB, packaging, alignment and signing. These are format/tool references, not copied project implementations.

The black geometry, thumbnails and build scripts were created for this project. This project is not affiliated with or endorsed by Samsung, Google or the credited community developers.
