# APK Reversing Playbook

Use this playbook only for an authorized CTF, local challenge, or explicitly
authorized mobile application test. The goal is to make APK analysis
repeatable for a headless agent: every stage writes evidence to the challenge
workspace and reports missing capabilities explicitly.

## Capability Tiers

The static sandbox and the Android runtime are separate:

| Tier | Capability | Required environment |
| --- | --- | --- |
| P0 | APK metadata, DEX, resources, Smali, signatures, packer detection | ctf-sandbox |
| P0 | Native library extraction and ELF analysis | ctf-sandbox |
| P1 | Java/native hooks and runtime values | ADB device or emulator plus Frida |
| P1 | UI exploration and transition graph | ADB device or emulator plus uiautomator2/DroidBot |
| P1 | Native-only ARM/JNI emulation | Java sidecar with unidbg |
| P1 | HTTPS inspection and pinning bypass | APK patching or Frida plus mitmproxy |
| P2 | Broad mobile assessment and web report | MobSF sidecar |

The static image architecture follows its deployment platform. It can inspect
ARM, ARM64, x86, and x86-64 files, but it must not execute native code
extracted from an APK. Dynamic execution belongs in a disposable Android
device/emulator.

## Project Map

These are the projects used by the runtime. The first eight are the base image
contract; the others are optional sidecars:

| Project | Use |
| --- | --- |
| https://github.com/skylot/jadx | DEX/APK to Java decompilation |
| https://github.com/iBotPeaches/Apktool | Manifest/resource decode, Smali patching, rebuild |
| https://developer.android.com/tools | ADB, AAPT2, apksigner, zipalign |
| https://github.com/androguard/androguard | APK/DEX parsing, disassembly, XREF analysis |
| https://github.com/rednaga/APKiD | Packers, protectors, obfuscators, compiler and RASP detection |
| https://frida.re/docs/android/ | Runtime instrumentation and hooks |
| https://github.com/sensepost/objection | Frida-powered runtime exploration, patching, and SSL-pinning helpers |
| https://github.com/openatx/uiautomator2 | Device UI, activity, screenshot, and session automation |
| https://github.com/ax/apk.sh | Split APK handling and Frida Gadget repackaging |
| https://github.com/niklashigi/apk-mitm | Network security config and common pinning patches |
| https://github.com/mitmproxy/android-unpinner | Rootless pinning removal and XAPK install-multiple workflow |
| https://github.com/honeynet/droidbot | UI-guided input generation and UI transition graph |
| https://github.com/zhkl0228/unidbg | ARM32/ARM64 native library and JNI emulation |
| https://github.com/google/android-emulator-container-scripts | Reproducible Android emulator container sidecar |
| https://github.com/budtmo/docker-android | Docker Android emulator with ADB and noVNC |
| https://github.com/MobSF/Mobile-Security-Framework-MobSF | Static/dynamic mobile assessment service |
| https://github.com/quark-engine/quark-engine | Rule-based Android behavior and malware analysis |

APKLab is useful for an interactive VS Code operator workflow but is not a
headless dependency. smali/baksmali should not be the primary new dependency
because its upstream repository is archived; Apktool already supplies the
normal Smali edit/rebuild path.

## Runtime Provisioning

The runtime is intentionally a sidecar. Google provides reproducible emulator
container scripts, but they require Linux Docker and KVM; Docker Desktop on
Windows/macOS does not provide the required KVM acceleration. Use a Linux host,
a WSL2/Ubuntu VM with nested virtualization, or a remote Linux runner:

    git clone https://github.com/google/android-emulator-container-scripts.git
    cd android-emulator-container-scripts
    source ./configure.sh
    emu-docker interactive --start
    adb connect localhost:5555
    adb wait-for-device

Then expose the host ADB server to the static sandbox and run
`apk-runtime-check`. For a noVNC-oriented setup, budtmo/docker-android is an
alternative, but it has the same virtualization prerequisite. Do not put the
emulator, ADB private key, or Frida server binary into the static APK image.

## First Pass

Set the input and output paths. Never modify the original under distfiles:

    APK=/challenge/distfiles/app.apk
    OUT=/challenge/workspace/apk
    mkdir -p "$OUT"
    apk-triage --apk "$APK" --out "$OUT"

Read the report before launching expensive tools:

    jq '{input,inventory,androguard,checks,next_steps}' "$OUT/apk-report.json"

The report is a triage result, not a flag. Confirm important observations in
the decompiler output and the original archive.

When a runtime sidecar is available, probe it before installing or hooking an
APK. This creates an explicit readiness result instead of silently treating a
missing emulator as a failed reverse-engineering hypothesis:

    RUNTIME_OUT="$OUT/runtime"
    apk-runtime-check --out "$RUNTIME_OUT" --package com.example.app
    jq '{status,selected_serial,device_count,frida_status}' "$RUNTIME_OUT/runtime-report.json"

## Static Branch

Run the following when the wrapper reports a missing or failed stage:

    file "$APK"
    unzip -l "$APK" | sed -n '1,160p'
    apkid -j "$APK"
    aapt dump badging "$APK"
    aapt dump permissions "$APK"
    apksigner verify --verbose "$APK"
    jadx --show-bad-code -d "$OUT/jadx-manual" "$APK"
    apktool d -f -o "$OUT/apktool-manual" "$APK"

Search both Java and Smali output. Prioritize:

1. Main activity, exported components, deep links, intent extras, and custom
   URI schemes.
2. Strings containing flag prefixes, URLs, hostnames, keys, salts, debug
   messages, and error text.
3. Comparisons against user input, cryptographic calls, native method
   declarations, reflection, DexClassLoader, and dynamically loaded assets.
4. Shared preferences, SQLite databases, assets, raw resources, and embedded
   certificates.
5. classes2.dex and later DEX files, split_config APKs, and every lib ABI.

Use Androguard when a programmatic answer is more reliable than grep:

    android-python - <<'PY'
    from androguard.core.apk import APK
    apk = APK("/challenge/distfiles/app.apk")
    print("package:", apk.get_package())
    print("activities:", apk.get_activities())
    print("permissions:", apk.get_permissions())
    print("dex_count:", len(apk.get_all_dex()))
    PY

## Native Branch

Extracted native libraries are evidence, not executables:

    find "$OUT/native" -type f -name '*.so' -print
    file "$OUT"/native/lib/*/*.so
    readelf -hW "$OUT"/native/lib/*/*.so
    readelf -Ws "$OUT"/native/lib/*/*.so | sed -n '1,220p'
    strings -n 6 "$OUT"/native/lib/*/*.so | tee "$OUT/native-strings.txt"

Use r2, objdump, capstone, angr, or Ghidra-compatible tooling on the library
matching the device ABI. Look for JNI exports, RegisterNatives, anti-debug
checks, string decryption, integrity checks, and the native implementation of
Java methods. A decompiler failure is not evidence that the code is absent.

## Packer and Obfuscation Branch

If APKiD identifies a protector or the decompiler is nearly empty:

- Record the APKiD JSON and the first loading component in findings.md.
- Inspect lib/*, Application.onCreate, multidex loading, reflection, and
  DexClassLoader before trusting class names.
- Compare DEX counts and file sizes before and after launching the app.
- Prefer runtime observation of decrypted classes and arguments over repeated
  decompiler retries.
- Delegate a separate worker to native loading and anti-analysis while another
  worker maps the Java entry points.

Do not claim a bypass from a static string alone. Require a hook trace,
reproducible patched behavior, or a flag check reached at runtime.

## Rebuild and Signing

Only rebuild a copy under workspace:

    apktool b "$OUT/apktool" -o "$OUT/unsigned.apk"
    zipalign -f -p 4 "$OUT/unsigned.apk" "$OUT/aligned.apk"
    apksigner sign --ks "$OUT/debug.keystore" --out "$OUT/patched.apk" "$OUT/aligned.apk"
    apksigner verify --verbose "$OUT/patched.apk"

Generate a disposable keystore if the challenge requires repackaging. Preserve
the original signer information in the report. An install failure can be
caused by signature mismatch, split APK requirements, ABI mismatch, or a
min/target SDK constraint; record which one was tested.

For split APKs or app bundles, prefer apk.sh for normalization and rebuilding.
Do not merge split files by hand unless the tool reports an unsupported format.

## Dynamic Branch

Dynamic analysis requires an explicitly provisioned device or emulator:

The ADB server must be reachable from the Docker network. A localhost-only host
server will not be reachable through Docker Desktop; in an isolated lab, start a
dedicated server with `adb -a nodaemon server`, or point `ADB_SERVER_SOCKET` at a
separate ADB sidecar. Do not expose port 5037 outside the lab network.

    export ADB_SERVER_SOCKET="tcp:host.docker.internal:5037"
    adb-host devices -l
    adb-host install -r "$OUT/patched.apk"
    frida-ps -U
    frida -U -f com.example.app -l "$OUT/hooks.js" --no-pause

The Frida server must match the device ABI and be started on the device. A
rooted disposable device is the simplest mode; Frida Gadget can be injected
into a repackaged APK when root is unavailable. Keep hooks narrow and write
stdout/stacks to workspace/dynamic/.

For UI exploration:

    uiautomator2 --serial "$SERIAL" current
    uiautomator2 --serial "$SERIAL" screenshot "$OUT/screen.png"
    droidbot -a "$OUT/patched.apk" -o "$OUT/droidbot"
    objection -g com.example.app start

DroidBot is not a substitute for reasoning. Use its UI graph to identify
hidden screens, intent paths, and inputs that need targeted Frida hooks.

For network inspection, use apk-mitm or android-unpinner for common Java-side
certificate pinning. If the app pins in native code or the patch breaks the
package, use Frida runtime hooks or a dedicated unpinning script instead.

When the target logic is isolated in a native library and a full emulator is
unavailable, use a small unidbg Java sidecar to load the matching ABI, call
JNI_OnLoad, and invoke the suspected export with controlled inputs. Record the
library hash, ABI, resolver/API level, arguments, return value, and trace in
workspace/apk/native-runtime/.

## Artifact Contract

The parent coordinator should require these artifacts before accepting a
worker result:

    {
      "status": "flag_found | promising | blocked | exhausted",
      "flag_candidate": "",
      "evidence": ["report path", "command and relevant output"],
      "new_findings": ["package", "entry point", "check or hook reached"],
      "dead_ends": ["tool and reason"],
      "next_best_step": ""
    }

APK-specific evidence must include:

- SHA-256 and original input path.
- DEX count, native ABI list, package name, and signer result.
- APKiD output or an explicit unavailable status.
- Exact decompiler command and output directory.
- For runtime claims: device ABI/API, package/activity, hook script, and
  captured trace.

## Failure Rules

- Missing JADX or Apktool: use the other decompiler and inspect raw DEX/ZIP
  structure; mark the missing tool in apk-report.json.
- Missing Androguard: continue with JADX/Apktool and aapt output; do not invent
  XREF or manifest facts.
- Missing ADB/emulator: complete static analysis, then mark dynamic as blocked.
- Frida attach failure: check process name, spawn vs attach mode, ABI, SELinux,
  and server version before changing hooks.
- Three repeated commands with no new evidence require a new branch, such as
  native extraction, split normalization, or dynamic observation.
