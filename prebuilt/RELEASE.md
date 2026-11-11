A black, unlit Home Space environment for Samsung Galaxy XR. No root required.

This is the original signed APK built and installed on 11 November 2026. The owner confirmed it worked after removing the stock Snow environment for user 0 and restarting Home. Other firmware is unverified.

## Install

Download `black-home.apk` and `SHA256SUMS` below. Verify on macOS with `shasum -a 256 -c SHA256SUMS`, then run:

```sh
adb install -r black-home.apk
```

Select **Black Home** under **Settings → Home environment**. If it does not appear, follow the [README](https://github.com/booinspace/galaxyxr-custom-home#readme) for the Snow slot workaround and restore commands. There is no app screen to open.

Recovery: `adb uninstall boo.puppy.blackhome`. Restore Snow if removed: `adb shell cmd package install-existing --user 0 com.google.environments.snow`.

## Contents and validation

- Package: `boo.puppy.blackhome`, versionName `1.0`, versionCode `1`.
- Generated black GLB/thumbnails plus a stock Snow lighting archive from the owner's headset; vendor assets remain their owners' work. No DEX code.
- Original APK signature verified; generated assets matched source; ZIP integrity and uncompressed binary assets checked. The committed build recipe was also rebuilt successfully and passed signature, alignment and asset checks.
- The APK uses a local debug signing certificate. Fresh source builds generate a different key; uninstall before switching between differently signed builds. Private signing keys are not published.
- SHA-256: `04139ef45081276cf2c6be797e649c0352fb777e6b1a7a66c0ccfa05c1e6ace4`.
- Signing certificate SHA-256: `05f7a5215a624ac0f120cea9ff4f06c6c7c83ceeb8e4c69ef6370dfcc57d11cd`.

Experimental community format: a failed model load can silently retain the previous scene. System windows, borders and safety overlays can remain visible.

Build/install instructions, recovery details and credits to u/nazga's community guide and the related Galaxy XR repositories are in the README.
