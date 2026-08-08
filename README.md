# Hermes Agent CTF Reversing

Hermes Agent CTF Reversing là bản mở rộng của [Hermes Agent](https://github.com/NousResearch/hermes-agent), được tối ưu cho CTF đã được cấp phép, phòng lab cục bộ và bài tập reverse engineering. Dự án giữ lại agent core của Hermes: CLI, TUI, desktop, memory, skills, subagent và terminal; đồng thời thêm một lớp CLI cho quy trình CTF có thể tái lập và lưu vết bằng chứng.

> Chỉ sử dụng dự án với CTF, lab có chủ sở hữu cho phép, hoặc mục tiêu mà bạn được ủy quyền rõ ràng. Không sử dụng các lệnh này để quét, khai thác hay can thiệp vào hệ thống ngoài phạm vi.

## Mục lục

- [Tính năng](#tính-năng)
- [Kiến trúc CTF](#kiến-trúc-ctf)
- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Khởi động nhanh](#khởi-động-nhanh)
- [Cấu hình CTFd](#cấu-hình-ctfd)
- [Quy trình phân tích](#quy-trình-phân-tích)
- [Lệnh tham chiếu](#lệnh-tham-chiếu)
- [Attack & Defense](#attack--defense)
- [Phát triển và kiểm thử](#phát-triển-và-kiểm-thử)
- [Tài liệu và giấy phép](#tài-liệu-và-giấy-phép)

## Tính năng

- **Agent đa kênh:** dùng cùng một agent qua CLI, TUI, desktop và các kênh nhắn tin mà Hermes hỗ trợ.
- **Skill `ctf-solver`:** playbook cho web, crypto, reverse engineering, pwn/binary, forensics, stego và APK reversing.
- **Workspace có cấu trúc:** tách input gốc, tệp sinh ra, ghi chú chung và trace để kết quả có thể kiểm tra lại.
- **Triage cố định:** `hermes ctf triage` chạy probe theo danh mục, lưu report JSON và cập nhật `findings.md`.
- **Benchmark cục bộ:** đo độ phủ danh mục, verifier, tính lặp lại và độ đầy đủ của bằng chứng; không đồng nhất điểm này với tỷ lệ giải được CTF bất kỳ.
- **CTFd:** pull challenge, xem score/status và submit flag qua API, với token tách khỏi cấu hình.
- **Điều phối song song:** Hermes có thể giao các hướng điều tra độc lập cho subagent, nhưng coordinator vẫn là nơi xác minh bằng chứng và submit flag.
- **Attack & Defense có kiểm soát:** bắt buộc khai báo `authorized: true`, scope cụ thể và `--live` trước khi chạy lệnh có tác động.

## Kiến trúc CTF

Tính năng CTF nằm ở CLI edge (`hermes_cli/ctf.py`), không thêm tool vào model schema được gửi trên mọi lượt chat. Cách tách này giữ prompt caching của Hermes ổn định và để người dùng có thể kiểm tra trực tiếp các lệnh có tác động bên ngoài.

```text
Hermes Agent
  |
  +-- ctf-solver skill
  |     +-- playbook theo danh mục
  |     +-- mẫu metadata và worker brief
  |
  +-- hermes ctf
        +-- init / triage / benchmark
        +-- doctor / assess
        +-- pull / score / status / submit (CTFd)
        +-- run (ctf-agent coordinator tùy chọn)
        +-- attack / ad (Attack & Defense)
```

| Thành phần | Vị trí | Vai trò |
| --- | --- | --- |
| CTF CLI | `hermes_cli/ctf.py` | CTFd, workspace, runner và Attack & Defense |
| Parser CLI | `hermes_cli/subcommands/ctf.py` | Định nghĩa `hermes ctf ...` |
| Triage | `hermes_cli/ctf_triage.py` | Probe theo danh mục và report evidence |
| Benchmark | `hermes_cli/ctf_benchmark.py` | Verifier và metric tái lập |
| Skill | `optional-skills/security/ctf-solver/` | Quy trình, playbook, template và toolbox |
| Tests | `tests/hermes_cli/test_ctf.py` | CTFd fixture, triage, benchmark và A&D |
| Ví dụ reverse | `ctf_cases/MetroApp/` | Case có artifact, trace, findings và verifier |

### Workspace contract

Mỗi challenge nên được chuẩn hóa theo cấu trúc sau:

```text
<challenge-slug>/
  metadata.yml     # Tên, danh mục, hint, kết nối, flag format
  distfiles/       # Input gốc, chỉ đọc
  workspace/       # Script, file extract, patch và artifact sinh ra
  findings.md      # Bảng thông tin chung của coordinator và worker
  traces/          # Output, trace, disassembly, bằng chứng đã chọn lọc
```

Không sửa file trong `distfiles/`. Toàn bộ script, file giải mã, binary patch, exploit draft và output lớn phải nằm trong `workspace/` hoặc `traces/`. Những thư mục challenge mặc định và state score được bỏ qua bởi Git vì có thể chứa flag, token hoặc dữ liệu thi đấu riêng tư.

## Yêu cầu

| Thành phần | Bắt buộc | Ghi chú |
| --- | --- | --- |
| Git | Có | Clone repository |
| Python 3.11-3.13 | Có | Dự án không hỗ trợ Python 3.14 |
| [uv](https://docs.astral.sh/uv/) | Có | Quản lý Python và dependency |
| Docker | Tùy chọn | Dùng cho triage cách ly và sandbox `ctf-sandbox` |
| `ctf-agent` checkout | Tùy chọn | Cần cho `hermes ctf run` theo coordinator/swarm bên ngoài |
| CTFd URL và token | Tùy chọn | Cần cho pull, score, status và submit |

Node.js chỉ cần khi phát triển TUI/Desktop hoặc các thành phần web của Hermes. Các công cụ reverse, pwn, crypto và forensics có thể dùng local hoặc trong Docker sandbox; `doctor` sẽ báo rõ capability nào đang thiếu.

## Cài đặt

Vì đây là fork có thêm CTF CLI và skill, hãy clone repository này thay vì cài Hermes Agent từ PyPI hoặc installer chung.

### Linux, macOS và WSL2

```bash
git clone https://github.com/in4SECxMinDandy/Hermes-Agent-CTF-Reversing-.git
cd Hermes-Agent-CTF-Reversing-

curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --locked --python 3.11 --extra all --extra dev

uv run hermes ctf --help
```

### Windows PowerShell

```powershell
git clone https://github.com/in4SECxMinDandy/Hermes-Agent-CTF-Reversing-.git
Set-Location Hermes-Agent-CTF-Reversing-

winget install --id astral-sh.uv -e
uv sync --locked --python 3.11 --extra all --extra dev

uv run hermes ctf --help
```

Mở một terminal mới nếu `uv` chưa có trên `PATH` sau khi cài đặt. Trong source checkout, ưu tiên `uv run hermes ...` để chắc chắn dùng đúng runtime của repository. Khi cần kích hoạt trực tiếp virtual environment trên PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
hermes ctf --help
```

### Kích hoạt skill CTF

`ctf-solver` là official optional skill, nên không được kích hoạt mặc định. Cài nó vào Hermes profile đang dùng:

```bash
uv run hermes skills install official/security/ctf-solver
```

Sau đó khởi động agent bằng `uv run hermes` và gọi `/ctf-solver` kèm yêu cầu cụ thể, ví dụ: `/ctf-solver phân tích challenge tại ~/ctf-challenges/sample`. Skill đưa vào playbook, template worker và quy tắc lưu bằng chứng trong repository này.

## Khởi động nhanh

Quy trình này hoạt động với một challenge local và không cần CTFd:

```bash
# 1. Kiểm tra capability local. Docker và ctf-agent là tùy chọn.
uv run hermes ctf doctor --json

# 2. Chuẩn hóa file hoặc thư mục challenge vào workspace.
uv run hermes ctf init ~/Downloads/challenge.zip --root ~/ctf-challenges

# 3. Chạy fixed probes. Docker được chọn tự động nếu có sẵn.
uv run hermes ctf triage ~/ctf-challenges/challenge --engine auto --network none --json

# 4. Đọc findings.md và report trong workspace/triage/, sau đó điều tra bằng agent.
uv run hermes
```

Trong agent, bắt đầu bằng dữ liệu có thể kiểm chứng: nêu rõ đường dẫn workspace, danh mục nghi ngờ, flag format và kết quả triage. Nếu challenge có `connection_info`, hãy ghi lại phản hồi đầu tiên của dịch vụ trước khi đào sâu vào tệp local.

Ví dụ prompt:

```text
/ctf-solver Đây là CTF đã được cấp phép. Hãy phân tích workspace
~/ctf-challenges/challenge, đọc metadata.yml và findings.md trước, sau đó
thực hiện một giả thuyết reverse engineering có bằng chứng. Không sửa distfiles/.
```

Khi triage bằng Docker, `--network none` là mặc định an toàn. Chỉ dùng `--network host` khi dịch vụ CTF đã được ủy quyền cần truy cập từ sandbox. Chế độ `--engine local` chạy probe trên host và không tạo network isolation; chỉ dùng nó với input local/offline hoặc khi bạn đã kiểm soát môi trường thực thi.

### Benchmark workflow

Benchmark chỉ thực thi verifier local mà bạn tin tưởng. Chạy `--execute` trên corpus riêng của bạn để kiểm tra năm danh mục: `web`, `crypto`, `reverse`, `forensics` và `binary`.

```bash
uv run hermes ctf benchmark \
  --root tests/fixtures/ctf_benchmark \
  --repeats 2 \
  --execute \
  --report ctf-benchmark-report.json \
  --json
```

Practical score là 10 điểm: độ phủ danh mục (3), verifier thành công (3), tính lặp lại (2) và artifact evidence đầy đủ (2). Đây là chỉ số đo độ ổn định của quy trình, không phải khẳng định rằng model sẽ giải được mọi đề CTF.

## Cấu hình CTFd

Đặt cấu hình hành vi trong Hermes home và chỉ đặt secret trong file `.env`:

- Linux/macOS/WSL: `~/.hermes/config.yaml` và `~/.hermes/.env`
- Windows native: `%LOCALAPPDATA%\hermes\config.yaml` và `%LOCALAPPDATA%\hermes\.env`

`config.yaml`:

```yaml
ctf:
  url: https://ctfd.example.invalid
  workspace: ~/ctf-challenges
  agent_dir: ~/src/ctf-agent
  sandbox_image: ctf-sandbox
  max_challenges: 10
  request_timeout: 30
  verify_tls: true
```

`.env`:

```text
CTFD_TOKEN=replace-with-a-secret-api-token
```

Không đưa `CTFD_TOKEN` vào `config.yaml`, commit, screenshot hoặc chat history. URL CTFd là cấu hình hành vi nên thuộc `config.yaml`; token là credential nên thuộc `.env`.

Kiểm tra cấu hình trước khi chạy thao tác live:

```bash
uv run hermes ctf doctor --network --json
uv run hermes ctf assess --network --json
```

`doctor` và `assess` báo cả các capability tùy chọn. Vì vậy kết quả partial không ngăn bạn dùng triage local; nó chỉ cho biết Docker image, CTFd hoặc external `ctf-agent` chưa sẵn sàng.

## Quy trình phân tích

### 1. Bảo toàn và triage

1. Xác nhận scope CTF/lab và flag format.
2. Chuẩn hóa challenge bằng `hermes ctf init` hoặc tạo đúng workspace contract.
3. Ghi checksum, loại file, kết nối, hint và dữ liệu ban đầu vào `findings.md`.
4. Chạy `hermes ctf triage` trước khi giao việc sâu.
5. Đọc report JSON; tool bị thiếu là thông tin về môi trường, không phải bằng chứng challenge đã hết đường.

### 2. Chọn playbook

Skill cung cấp playbook cho các hướng sau:

| Danh mục | Hướng bắt đầu |
| --- | --- |
| Web | Header, HTML/JS, route, cookie, redirect, source map và API |
| Reverse | `file`, `strings`, imports, disassembly, flag check và reimplement logic |
| Binary/Pwn | Protocol, `checksec`, ELF metadata, debugger và exploit script trong `workspace/` |
| Crypto | Xác định primitive và misuse trước khi brute force; lưu toàn bộ tham số |
| Forensics/Stego | Metadata, magic bytes, archive, image/audio/video và filesystem/memory artifact |
| APK | Static triage trước; dynamic analysis chỉ trên emulator/device disposable được cấp phép |

Xem [category playbooks](optional-skills/security/ctf-solver/references/category-playbooks.md), [sandbox toolbox](optional-skills/security/ctf-solver/references/sandbox-toolbox.md) và [APK reversing playbook](optional-skills/security/ctf-solver/references/apk-reversing-playbook.md) để có lệnh và điều kiện chi tiết.

### 3. Điều phối subagent

Chỉ tách 3-5 hướng thật sự độc lập, ví dụ service interaction, binary/reverse, crypto/encoding, forensics/stego và sanity check. Mỗi worker phải nhận metadata, scope, đường dẫn tuyệt đối và bản trích `findings.md` mới nhất. Dùng [worker brief](optional-skills/security/ctf-solver/templates/worker-brief.md) làm contract trả về:

```json
{
  "status": "flag_found | promising | blocked | exhausted",
  "flag_candidate": "",
  "evidence": [],
  "new_findings": [],
  "dead_ends": [],
  "next_best_step": ""
}
```

Coordinator cập nhật `findings.md`, loại bỏ kết quả trùng lặp và tự xác minh flag candidate. Không submit flag do worker tự báo cáo mà chưa có bằng chứng.

### 4. Kết thúc và xác minh

- Sau ba lần lặp lại cùng một lệnh mà không có phát hiện mới, đổi giả thuyết hoặc công cụ.
- Lưu lệnh, output liên quan và lý do kết luận vào `findings.md`/`traces/`.
- Nếu CTFd đã cấu hình, xác minh candidate bằng API thay vì chỉ dựa vào hình dạng chuỗi.
- Nếu chưa submit, ghi rõ `unsubmitted` và bằng chứng có đủ mạnh hay không.

## Lệnh tham chiếu

| Lệnh | Mục đích |
| --- | --- |
| `hermes ctf doctor [--network] [--json]` | Kiểm tra skill, workspace, Docker, sandbox, CTFd và coordinator |
| `hermes ctf assess [--network] [--json]` | Chấm điểm readiness 0-10 |
| `hermes ctf init <source> --root <dir>` | Chuẩn hóa file/thư mục local thành workspace |
| `hermes ctf triage <challenge> [--engine auto|docker|local]` | Chạy probe theo danh mục và lưu report |
| `hermes ctf benchmark --root <dir> [--execute]` | Đo corpus verifier local |
| `hermes ctf pull [--unsolved-only]` | Tải challenge và file từ CTFd |
| `hermes ctf score [--top N]` | Xem scoreboard CTFd |
| `hermes ctf status [--top N]` | Lấy snapshot challenge, solve và scoreboard |
| `hermes ctf submit <challenge> <flag> --yes` | Submit flag; bắt buộc xác nhận explicit |
| `hermes ctf run [--challenge <dir>]` | Gọi external `ctf-agent` coordinator nếu đã cấu hình |
| `hermes ctf attack list` | Liệt kê curated attack-tool catalog |
| `hermes ctf ad doctor|run|status <config>` | Validate, chạy hoặc xem state A&D |

Dùng `uv run hermes ctf <lệnh> --help` để xem flag đầy đủ. Các lệnh CTFd sẽ fail rõ ràng nếu `ctf.url` hoặc `CTFD_TOKEN` chưa được cấu hình.

### CTFd workflow

```bash
# Tải các challenge chưa giải vào ctf.workspace
uv run hermes ctf pull --unsolved-only --json

# Theo dõi trạng thái thi đấu
uv run hermes ctf status --top 20 --json

# Chỉ submit sau khi đã kiểm chứng giả thuyết và muốn tạo side effect
uv run hermes ctf submit "Challenge name" "FLAG{candidate}" --yes --json
```

`hermes ctf run` là integration với external `ctf-agent` checkout, được tìm qua `ctf.agent_dir`. Không có checkout này, vẫn có thể dùng Hermes-native workflow: `pull`/`init`, `triage`, `/ctf-solver`, sau đó `submit` khi được phép.

## Attack & Defense

Attack & Defense chỉ phục vụ lab/competition đã được ủy quyền. Config phải khai báo `authorized: true`, scope không rỗng, dịch vụ có tên và lệnh rõ ràng. Bắt đầu từ [template](optional-skills/security/ctf-solver/templates/attack-defense.yml):

```yaml
authorized: true
scope:
  - 127.0.0.1:31337
command_timeout: 60
allow_high_risk: false
services:
  - name: example-service
    target: 127.0.0.1:31337
    healthcheck: [python, -c, "print('healthy')"]
    patch: [python, -c, "print('authorized patch')"]
    attack: [python, -c, "print('authorized check')"]
    flag_command: [python, -c, "print('FLAG{example}')"]
    points: 100
```

Xác thực trước khi thực thi:

```bash
uv run hermes ctf ad doctor templates/attack-defense.yml
uv run hermes ctf ad run templates/attack-defense.yml
```

Lệnh thứ hai mặc định là dry run. Chạy command thật chỉ khi đã kiểm tra config và có ủy quyền:

```bash
uv run hermes ctf ad run templates/attack-defense.yml --live --watch --interval 30
uv run hermes ctf ad status templates/attack-defense.yml
```

Catalog `hermes ctf attack list` là tập nhỏ các công cụ recon/web được gọi bằng argv, không qua shell. Hermes tự chèn target từ service config, không chấp nhận target thứ hai trong `args`, không tự động cài công cụ upstream và không chạy privileged container. `sqlmap` cần `allow_high_risk: true` trong config đã được ủy quyền rõ ràng.

## Ví dụ MetroApp

`ctf_cases/MetroApp/` là một case reverse engineering đã được chuẩn hóa, gồm archive, PE đã extract, string/disassembly traces, findings và verifier. Nó minh họa cách tách evidence và kết luận; không dùng nó như CTFd target hoặc corpus benchmark tổng quát.

```powershell
# Chạy verifier của case mẫu trên Windows
.\.venv\Scripts\python.exe .\ctf_cases\MetroApp\workspace\verify_flag.py
```

Đọc [findings.md](ctf_cases/MetroApp/findings.md) để xem cách một kết luận lure được loại bỏ bằng relation ROL/XOR, charset filter và verification độc lập.

## Phát triển và kiểm thử

Chạy test CTF cố định sau khi thay đổi CLI, triage, benchmark hoặc Attack & Defense:

```bash
uv run python -m pytest tests/hermes_cli/test_ctf.py -v
```

Hoặc chạy test runner của dự án để gần với CI hơn:

```bash
scripts/run_tests.sh tests/hermes_cli/test_ctf.py
```

Test bao phủ CTFd fixture, origin guard khi tải file, submit, score/status, workspace benchmark, triage evidence, validation scope của A&D và parser CLI. Khi thêm skill hoặc sửa frontmatter, chạy thêm:

```bash
uv run python scripts/validate_skills.py --strict
```

Quy tắc đóng góp của Hermes vẫn áp dụng: giữ core toolset hẹp, đưa capability đặc thù vào CLI/skill/plugin khi có thể, không đặt credential trong source control và ưu tiên test end-to-end với `HERMES_HOME` tạm thời khi chạm vào config, filesystem hoặc network.

## Tài liệu và giấy phép

- [CTF Solver skill](optional-skills/security/ctf-solver/SKILL.md)
- [CTFd workflow](optional-skills/security/ctf-solver/references/ctfd-workflow.md)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Contributing guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

Dự án phát hành theo giấy phép [MIT](LICENSE). Hermes Agent được xây dựng bởi [Nous Research](https://nousresearch.com); phần CTF Reversing trong repository này mở rộng nó cho các workflow CTF và lab đã được cấp phép.
