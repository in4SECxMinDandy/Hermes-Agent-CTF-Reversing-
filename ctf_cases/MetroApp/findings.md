# MetroApp findings

## Scope and preservation

- Input: `C:/Users/haqua/Downloads/MetroApp.zip`
- Original SHA-256: `77393c6de346f97f69d7e2eaa2d88d6b42fa28c1119b75ef13a300ba2e3b33fe`
- Original size: 1,069,376 bytes
- Archive test: `unzip -t` passed for all 14 entries.
- Original archive was not modified; analysis copy is under `distfiles/`.

## Triage

- Outer archive contains a Windows 8 Metro/AppX package.
- Nested package: `MetroApp/MetroApp_1.0.0.5_Win32.appx`.
- Extracted executable: `workspace/appx/MetroApp.exe`, PE32 x86 GUI.
- Executable SHA-256: `b95d2054ec243a4cb6bf78ec38e7d8eede41f0a707f10990c5fb9bf732b644dc`.
- `MainPage.xaml` has one input `TextBox` named `PasswordInput` and an OK button.

## Corrected flag analysis

The earlier `MERONG` conclusion was false. `MERONG` is a lure literal; finding it and an adjacent comparison call does not prove that it is the final accepted input. The old verifier has been corrected to model the full character loop and its terminating NUL condition.

The decisive relation is:

```text
next = ROL8(current, current & 7) XOR key[i & 7]
```

The first eight key bytes are embedded at VA `0x4307a8`:

```text
77 AD 07 02 A5 00 29 99
```

Starting from each permitted initial character and following the relation until `0x00` produces exactly:

```text
Cm
D34DF4C3
```

`Cm` is rejected because the lowercase `m` violates the permitted uppercase-letter/digit character set. The only valid flag is therefore:

```text
D34DF4C3
```

Independent corroboration: https://blog.ugonfor.kr/44

## Corrected verification

Ran `python workspace/verify_flag.py` against the extracted executable. It verifies the embedded key, ROL/XOR opcode evidence, both NUL-terminated candidates, and the charset filter; it reports `D34DF4C3` as the sole valid candidate.

No flag was submitted remotely.
