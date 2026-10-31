<#
    AI Investigation Note Quality Assistant - automatic launcher.

    Invoked by START-ASSISTANT.bat (double-click). It does everything needed:
      1. finds Python (or offers to install it);
      2. creates the isolated .venv environment and installs the packages;
      3. asks for the API key ON EVERY START - keys are never reused from
         disk, so a shared or inherited folder can never silently run on
         someone else's credential. The entered key is verified against
         Anthropic with a free authenticated call (models list - no tokens
         are billed) when Anthropic is reachable, written to
         03 Demo\.streamlit\secrets.toml only so the application process
         can read it, and that file is removed again when the application
         stops (best effort - an abruptly closed window can leave it, but
         it is overwritten and never reused at the next start).
         Deliberate exception: with Anthropic unreachable, a
         plausible-looking key (sk-ant-*) is accepted UNVERIFIED with a
         visible warning;
      4. starts the application and opens the browser.

    -PrepareShare (used by PREPARE-TO-SHARE.bat) instead removes your personal
    key and the local environment so the folder can be handed to someone else.

    The key is entered hidden, is never shown on screen, is never written
    anywhere except secrets.toml (which git ignores), and never appears in an
    error message.

    This file is kept ASCII-only on purpose: it has to survive being read by
    Windows PowerShell 5.1 on machines with any system codepage.

    -CheckOnly verifies everything but does not start the application.
#>
[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [switch]$PrepareShare
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
# -LiteralPath everywhere: a folder name containing [brackets] would
# otherwise be treated as a wildcard pattern and break every path check.
Set-Location -LiteralPath $ProjectRoot

# Counted so a -CheckOnly run can summarize honestly instead of printing
# "all checks passed" under warnings.
$script:ProblemCount = 0

# Set by Test-PythonCommand when a working Python 3 was found but rejected
# for being older than 3.10, so the "not found" messages can name the real
# problem instead of claiming Python is missing.
$script:TooOldPythonSeen = $null

$VenvPython = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$SecretsDir = Join-Path $ProjectRoot '03 Demo\.streamlit'
$SecretsFile = Join-Path $SecretsDir 'secrets.toml'
$PlaceHolder = 'PASTE-YOUR-OWN-KEY-HERE'

function Write-Step { param([string]$Text) Write-Host "`n>>> $Text" -ForegroundColor Cyan }
function Write-Ok { param([string]$Text) Write-Host "    [OK] $Text" -ForegroundColor Green }
function Write-Info { param([string]$Text) Write-Host "    $Text" -ForegroundColor Gray }
function Write-Problem {
    param([string]$Text)
    $script:ProblemCount++
    Write-Host "`n[!] $Text" -ForegroundColor Yellow
}

function Wait-CloseKey {
    # Pause so a double-clicked window stays readable - but never hang an
    # automated caller whose stdin is redirected.
    if (-not [Console]::IsInputRedirected) {
        Read-Host 'Press Enter to close this window' | Out-Null
    }
}

# Accepted affirmative answers. "da" is written from character codes rather
# than literally, so this file stays pure ASCII and cannot be corrupted by a
# machine whose system codepage is not UTF-8.
$YesAnswers = @('y', 'yes', 'da', ([string]([char]0x0434) + [char]0x0430))

function Test-Affirmative {
    param([string]$Answer)
    if (-not $Answer) { return $false }
    return ($YesAnswers -contains $Answer.Trim().ToLower())
}

# ---------------------------------------------------------------------------
# -PrepareShare: make the folder safe to hand to someone else.
# Removes the personal API key, the local environment and machine-local
# caches. The recipient double-clicks START-ASSISTANT.bat and everything is
# rebuilt for them, including being asked for THEIR OWN key.
# ---------------------------------------------------------------------------
if ($PrepareShare) {
    Write-Host ''
    Write-Host '===============================================================' -ForegroundColor White
    Write-Host '   Preparing this folder for sharing' -ForegroundColor White
    Write-Host '===============================================================' -ForegroundColor White
    Write-Info "Project folder: $ProjectRoot"

    if (Test-Path -LiteralPath $SecretsFile) {
        try {
            Remove-Item -LiteralPath $SecretsFile -Force -ErrorAction Stop
            Write-Ok 'Removed your API key file (03 Demo\.streamlit\secrets.toml).'
        } catch {
            Write-Problem 'COULD NOT remove your API key file (03 Demo\.streamlit\secrets.toml) - it is probably held right now by antivirus or a sync tool (OneDrive/Dropbox). YOUR KEY IS STILL IN THE FOLDER. Wait a few seconds and run PREPARE-TO-SHARE again. Do NOT share the folder until this succeeds.'
            Wait-CloseKey
            exit 1
        }
    } else {
        Write-Info 'No API key file found - nothing to remove there.'
    }

    $venvDir = Join-Path $ProjectRoot '.venv'
    if (Test-Path -LiteralPath $venvDir) {
        try {
            Remove-Item -LiteralPath $venvDir -Recurse -Force -ErrorAction Stop
            Write-Ok 'Removed the .venv folder (it is large, machine-specific, and rebuilt automatically on the next start).'
        } catch {
            Write-Problem 'Could not remove the .venv folder - it is probably in use. Close every launcher/terminal window of this project, then run PREPARE-TO-SHARE again.'
            Wait-CloseKey
            exit 1
        }
    } else {
        Write-Info 'No .venv folder found - nothing to remove there.'
    }

    $localSettings = Join-Path $ProjectRoot '.claude\settings.local.json'
    if (Test-Path -LiteralPath $localSettings) {
        Remove-Item -LiteralPath $localSettings -Force -ErrorAction SilentlyContinue
        Write-Ok 'Removed .claude\settings.local.json (machine-local tool settings).'
    }

    foreach ($cache in @('.pytest_cache', '.pytest-tmp',
                         '03 Demo\__pycache__', 'tests\__pycache__')) {
        $cachePath = Join-Path $ProjectRoot $cache
        if (Test-Path -LiteralPath $cachePath) {
            Remove-Item -LiteralPath $cachePath -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    if (Test-Path -LiteralPath (Join-Path $ProjectRoot '.git')) {
        Write-Problem 'Checked but NOT removed: this folder contains a hidden ".git" folder (version-control history). It carries the author name/e-mail configured inside it and older versions of edited files. If you send the folder as a plain copy, delete the hidden ".git" folder IN THE COPY you send - it is left untouched here because it is your own working history.'
    }

    Write-Host ''
    Write-Ok 'Done. Review any [!] note above; the folder is otherwise safe to give to someone else.'
    Write-Info 'The recipient just double-clicks START-ASSISTANT.bat - it rebuilds'
    Write-Info 'everything and asks them for their own API key.'
    Write-Host ''
    Wait-CloseKey
    exit 0
}

function Stop-WithMessage {
    param([string]$Text)
    Write-Host ''
    Write-Host '===============================================================' -ForegroundColor Red
    Write-Host " $Text" -ForegroundColor Red
    Write-Host '===============================================================' -ForegroundColor Red
    Write-Host ''
    Write-Host 'Step-by-step manual instructions: START-HERE-EN.md (English)'
    Write-Host 'or START-HERE-BG.md (Bulgarian), in the project folder.'
    Write-Host ''
    if (-not $CheckOnly) {
        Wait-CloseKey
    }
    exit 1
}

function Show-Introduction {
    <# Product introduction for a normal interactive start. Skipped in
       -CheckOnly (must stay non-interactive) and never reached by
       -PrepareShare (that mode exits earlier). Facts below are sourced
       from the project's evidence records - do not embellish them.
       All lines are ASCII and kept under 76 columns. #>
    $B = 'White'; $H = 'Cyan'; $D = 'Gray'
    Write-Host ''
    Write-Host '  =========================================================================' -ForegroundColor $B
    Write-Host '     AI INVESTIGATION NOTE QUALITY ASSISTANT' -ForegroundColor $B
    Write-Host '     Local portfolio / research MVP' -ForegroundColor $D
    Write-Host '  =========================================================================' -ForegroundColor $B
    Write-Host ''
    Write-Host '  WHAT IT DOES' -ForegroundColor $H
    Write-Host '    A second set of eyes before an investigation note is submitted.'
    Write-Host '    It reviews the quality, clarity, completeness and reasoning of the'
    Write-Host '    written note: whether the documented findings support the conclusion,'
    Write-Host '    what material gaps or contradictions remain, and which focused'
    Write-Host '    questions would close them - built from the facts provided.'
    Write-Host ''
    Write-Host '    It reviews the documentation and reasoning - not the customer,'
    Write-Host '    account, risk outcome, analyst, or the investigation decision.'
    Write-Host '    All decisions remain with the human user.' -ForegroundColor $B
    Write-Host ''
    Write-Host '  HOW IT WAS BUILT' -ForegroundColor $H
    Write-Host '    The assistant follows a version-controlled behavioural specification,'
    Write-Host '    Assistant Contract v0.8: evidence-first reading, material-gap rules,'
    Write-Host '    proportional feedback, uncertainty handling, a no-invention boundary,'
    Write-Host '    and a strictly advisory role.'
    Write-Host ''
    Write-Host '    The demo is a local Streamlit application with separated parts: the'
    Write-Host '    interface, contract loading and integrity verification, request and'
    Write-Host '    domain logic, provider error handling, bilingual interface text, and'
    Write-Host '    an optional experimental gating filter. Every start verifies the'
    Write-Host '    pinned contract against its locked SHA-256 reference and fails'
    Write-Host '    closed if it cannot be verified.'
    Write-Host ''
    Write-Host '    For analysis it sends the supplied note, scenario context and the'
    Write-Host '    pinned contract to Claude Haiku 4.5 through the Anthropic API.'
    Write-Host '    This project did NOT train or fine-tune Claude.' -ForegroundColor $B
    Write-Host ''
    Write-Host '  DATA AND TESTING' -ForegroundColor $H
    Write-Host '    All notes, cases and rule descriptions bundled with this shared demo'
    Write-Host '    are human-authored synthetic material. No raw customer data, real'
    Write-Host '    case identifiers, employer material or API credentials are included'
    Write-Host '    in the shared demo.'
    Write-Host ''
    Write-Host '    The application passes 90 offline engineering tests using a mocked'
    Write-Host '    Anthropic client (contract integrity, request construction, input'
    Write-Host '    limits, secret handling, safe errors, gating mechanics, interface'
    Write-Host '    paths). Engineering tests show the application works as implemented;'
    Write-Host '    they do NOT prove its feedback is consistently accurate.'
    Write-Host ''
    Write-Host '    The pinned contract was evaluated separately, on a controlled'
    Write-Host '    held-out set of neutralised notes. It missed both of its'
    Write-Host '    preregistered validation targets.' -ForegroundColor $B
    Write-Host ''
    Write-Host '  IMPORTANT LIMITS' -ForegroundColor $H
    Write-Host '    This is a research and portfolio MVP, not a production-validated'
    Write-Host '    system. It may miss relevant issues or raise unnecessary ones, and'
    Write-Host '    in at least one recorded case it asserted an incorrect external'
    Write-Host '    fact - verify any code or typology claim before relying on it.'
    Write-Host '    It is not an AML or compliance system, not an account-review bot,'
    Write-Host '    not a scoring or approval tool, and no replacement for human'
    Write-Host '    judgement.'
    Write-Host ''
    Write-Host '    Test it only with the bundled synthetic examples. Do not enter real' -ForegroundColor Yellow
    Write-Host '    customer or case data.' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '    Full methodology, measured results, limitations and technical'
    Write-Host '    documentation: README.md (in this folder).'
    Write-Host ''
    Write-Host '  -------------------------------------------------------------------------' -ForegroundColor $D
    Write-Host '  STARTING THE LOCAL DEMO' -ForegroundColor $H
    Write-Host '    The launcher will now check this computer and prepare everything'
    Write-Host '    required to run the local application. On the first run this may'
    Write-Host '    take a few minutes; if Python is missing, Windows may ask for'
    Write-Host '    permission to install it.'
    Write-Host ''
    Write-Host '    An Anthropic API key is required to generate an analysis. You must'
    Write-Host '    use your own Anthropic Console API key and API credit. A Claude'
    Write-Host '    subscription or Max plan does NOT include Anthropic API usage.'
    Write-Host '  -------------------------------------------------------------------------' -ForegroundColor $D
    Write-Host ''
    if (-not [Console]::IsInputRedirected) {
        Read-Host 'Press Enter to continue with the setup checks'
    }
}

Write-Host ''
if ($CheckOnly) {
    Write-Host '===============================================================' -ForegroundColor White
    Write-Host '   AI Investigation Note Quality Assistant - starting up' -ForegroundColor White
    Write-Host '===============================================================' -ForegroundColor White
} else {
    Show-Introduction
}
Write-Info "Project folder: $ProjectRoot"

# ---------------------------------------------------------------------------
# 1. Structure check - the application refuses to run without the contract.
# ---------------------------------------------------------------------------
Write-Step 'Checking the project files...'
foreach ($required in @('03 Demo\app.py', 'requirements.txt',
                        '01 Contract', '02 Skill')) {
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot $required))) {
        Stop-WithMessage "Missing '$required'. This launcher must sit in the main project folder, next to 01 Contract, 02 Skill and 03 Demo."
    }
}
Write-Ok 'All required files are present.'

# ---------------------------------------------------------------------------
# 2. Locate Python.
# ---------------------------------------------------------------------------
function Test-PythonCommand {
    <# Returns $true only for a genuinely working Python 3.10 or newer -
       the pinned streamlit/pytest releases require 3.10+, so accepting an
       older Python here would only fail later with a misleading
       package-installation error. Also filters out the Microsoft Store
       stub, which is not Python. #>
    param([string]$Exe, [string[]]$Prefix = @())
    try {
        $output = & $Exe @Prefix '--version' 2>&1 | Out-String
    } catch {
        return $false
    }
    if ($LASTEXITCODE -ne 0) { return $false }
    if ($output -notmatch 'Python 3\.(\d+)') { return $false }
    if ([int]$Matches[1] -lt 10) {
        $script:TooOldPythonSeen = $output.Trim()
        return $false
    }
    return $true
}

function Find-Python {
    foreach ($candidate in @(
        @{ Exe = 'py';      Prefix = @('-3') },
        @{ Exe = 'python';  Prefix = @() },
        @{ Exe = 'python3'; Prefix = @() }
    )) {
        if (Get-Command $candidate.Exe -ErrorAction SilentlyContinue) {
            if (Test-PythonCommand -Exe $candidate.Exe -Prefix $candidate.Prefix) {
                return $candidate
            }
        }
    }
    return $null
}

Write-Step 'Looking for Python...'
$python = Find-Python

if (-not $python) {
    if ($CheckOnly) {
        # A check must never prompt, block, or install anything.
        if ($script:TooOldPythonSeen) {
            Write-Problem "Only an older Python ($script:TooOldPythonSeen) was found - this project needs Python 3.10 or newer. A normal start would offer to install a suitable version automatically. Checks stopped here: the remaining steps need Python."
        } else {
            Write-Problem 'Python is not installed - a normal start would offer to install it automatically. Checks stopped here: the remaining steps need Python.'
        }
        Write-Host ''
        Write-Problem "Checks finished with $($script:ProblemCount) note(s) - see the [!] lines above. (-CheckOnly: nothing was started or installed; exit code 2 signals the notes.)"
        exit 2
    }
    if ($script:TooOldPythonSeen) {
        Write-Problem "An older Python ($script:TooOldPythonSeen) was found, but this project needs Python 3.10 or newer."
    } else {
        Write-Problem 'Python is not installed on this computer.'
    }
    Write-Host ''
    Write-Host 'Python 3.12 can be installed automatically through the Windows'
    Write-Host 'package manager (winget). The download is about 30 MB and'
    Write-Host 'Windows may ask you to confirm.'
    Write-Host ''
    $answer = Read-Host 'Install Python now? (yes / no)'
    if (-not (Test-Affirmative $answer)) {
        Stop-WithMessage 'Installation declined. The application cannot run without Python 3.10 or newer.'
    }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Problem 'winget is not available on this version of Windows.'
        Write-Host 'Opening the download page instead - install Python from there,'
        Write-Host 'and be sure to tick "Add python.exe to PATH".'
        Start-Process 'https://www.python.org/downloads/'
        Stop-WithMessage 'Once Python is installed, run this launcher again.'
    }
    Write-Info 'Installing Python, this takes a few minutes...'
    winget install --exact --id Python.Python.3.12 --source winget `
        --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        # An unchecked winget failure would otherwise fall through to a
        # misleading "installed but not visible" diagnosis.
        Stop-WithMessage 'The Python installation did not complete - it may have been declined at the Windows permission prompt, or the download failed. Nothing was broken. Run this launcher again to retry, or install Python yourself from https://www.python.org/downloads/ (tick "Add python.exe to PATH").'
    }
    # winget does not refresh PATH for the running process - reload it.
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path', 'User')
    $python = Find-Python
    if (-not $python) {
        Stop-WithMessage 'Python was installed but is not visible yet. Close this window and run the launcher again - that usually resolves it.'
    }
}

$pythonVersion = (& $python.Exe @($python.Prefix) '--version' 2>&1 | Out-String).Trim()
Write-Ok "Found: $pythonVersion"

# ---------------------------------------------------------------------------
# 3. Isolated environment (.venv) and packages.
#    If the project folder was moved or renamed, .venv still points at the old
#    path, so the environment is tested for real rather than by mere presence.
# ---------------------------------------------------------------------------
function Test-VenvUsable {
    if (-not (Test-Path -LiteralPath $VenvPython)) { return $false }
    try {
        & $VenvPython '-c' 'import streamlit, anthropic' 2>&1 | Out-Null
    } catch {
        return $false
    }
    return ($LASTEXITCODE -eq 0)
}

Write-Step 'Checking the working environment...'
if (Test-VenvUsable) {
    Write-Ok 'Environment is ready, packages are installed.'
} elseif ($CheckOnly) {
    # A check never installs, downloads, or deletes anything.
    Write-Problem 'The working environment (.venv) is not built or not usable - a normal start would build it automatically (takes a few minutes, needs internet).'
    Write-Host ''
    Write-Problem "Checks finished with $($script:ProblemCount) note(s) - see the [!] lines above. (-CheckOnly: nothing was started or installed; exit code 2 signals the notes.)"
    exit 2
} else {
    if (Test-Path -LiteralPath (Join-Path $ProjectRoot '.venv')) {
        Write-Info 'Environment is unusable (usually after the folder was moved) - rebuilding it.'
        try {
            Remove-Item -LiteralPath (Join-Path $ProjectRoot '.venv') `
                -Recurse -Force -ErrorAction Stop
        } catch {
            Stop-WithMessage 'Could not rebuild the environment: the .venv folder is in use. Another launcher window of this project is probably open (perhaps still installing). Close every other window of this project and run the launcher again.'
        }
    } else {
        Write-Info 'Creating an isolated environment for this project...'
    }
    & $python.Exe @($python.Prefix) '-m' 'venv' '.venv'
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $VenvPython)) {
        Stop-WithMessage 'Creating the environment (.venv) failed.'
    }
    Write-Info 'Installing the required packages - this takes 1-3 minutes...'
    & $VenvPython '-m' 'pip' 'install' '--quiet' '--disable-pip-version-check' `
        '-r' 'requirements.txt'
    if ($LASTEXITCODE -ne 0 -or -not (Test-VenvUsable)) {
        Stop-WithMessage 'Installing the packages failed. Check your internet connection and run the launcher again.'
    }
    Write-Ok 'Environment is ready.'
}

# ---------------------------------------------------------------------------
# 4. API key.
#    Requested on EVERY start, by design: nothing is ever read back from
#    disk, so a shared or inherited folder can never silently run on
#    someone else's credential. Entered hidden. Never printed, never
#    logged, never written anywhere except secrets.toml (which git
#    ignores), and that file is removed again when the application stops.
#    Keys are verified against Anthropic with a FREE authenticated call
#    (models list; no tokens are billed) whenever Anthropic is reachable,
#    so a wrong or revoked key is caught here rather than as a confusing
#    failure inside the application. Deliberate exception: when Anthropic
#    is unreachable, a plausible-looking key is accepted UNVERIFIED with
#    a warning.
# ---------------------------------------------------------------------------

function Test-ApiKey {
    <# Returns 'valid', 'invalid' or 'unreachable'. Uses the models-list
       endpoint: authenticated but free - no tokens are billed. The key
       travels to the child process through an environment variable, never
       on a command line (command lines are visible in the process list).
       The child script always prints one word and exits 0. #>
    param([string]$Key)
    $checker = @'
import os
import anthropic
try:
    client = anthropic.Anthropic(
        api_key=os.environ["KEY_UNDER_TEST"], timeout=20.0, max_retries=0)
    client.models.list()
    print("valid")
except (anthropic.AuthenticationError, anthropic.PermissionDeniedError):
    print("invalid")
except Exception:
    print("unreachable")
'@
    $previousEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $env:KEY_UNDER_TEST = $Key
    try {
        $result = ($checker | & $VenvPython '-' 2>$null | Select-Object -Last 1)
    } catch {
        $result = 'unreachable'
    } finally {
        Remove-Item Env:\KEY_UNDER_TEST -ErrorAction SilentlyContinue
        $ErrorActionPreference = $previousEap
    }
    if ($result -match '^(valid|invalid|unreachable)$') { return $result }
    return 'unreachable'
}

function Save-Key {
    param([string]$Key)
    if (-not (Test-Path -LiteralPath $SecretsDir)) {
        New-Item -ItemType Directory -Path $SecretsDir -Force | Out-Null
    }
    # UTF-8 without BOM: a BOM at the start breaks TOML parsing.
    $line = 'ANTHROPIC_API_KEY = "' + $Key + '"' + [Environment]::NewLine
    [System.IO.File]::WriteAllText(
        $SecretsFile, $line, (New-Object System.Text.UTF8Encoding($false)))
}

function Remove-SavedKey {
    # The secrets file exists only so the application process can read the
    # key during this session; once the application has stopped it is
    # removed again. Best effort: if the window is closed abruptly the
    # file can remain, but it is overwritten and never reused next start.
    if (Test-Path -LiteralPath $SecretsFile) {
        Remove-Item -LiteralPath $SecretsFile -Force -ErrorAction SilentlyContinue
    }
}

function Read-SecretText {
    param([string]$Prompt)
    if ([Console]::IsInputRedirected) {
        # No real console (started automatically or through a pipe) - hidden
        # input would simply hang there, so read directly instead.
        Write-Host "${Prompt}: " -NoNewline
        return [Console]::In.ReadLine()
    }
    try {
        $secure = Read-Host -Prompt $Prompt -AsSecureString
        $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        try {
            return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
        } finally {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
        }
    } catch {
        # Some consoles do not support hidden input - fall back to plain input.
        return (Read-Host -Prompt "$Prompt (what you type will be visible)")
    }
}

Write-Step 'API key...'
if ($CheckOnly) {
    # A check must never block waiting for input. There is no saved-key
    # state to report: keys are requested fresh on every normal start.
    Write-Info 'The launcher asks for the API key on every start; keys are never reused from disk. (-CheckOnly: no prompt now.)'
} else {
        Write-Host ''
        Write-Host '  -----------------------------------------------------------------' -ForegroundColor Gray
        Write-Host '  ANTHROPIC API KEY' -ForegroundColor Cyan
        Write-Host ''
        Write-Host '    Enter your Anthropic API key and press Enter.'
        Write-Host '    Your input will be hidden.'
        Write-Host ''
        Write-Host '    The key is used for this session only: it is written to the'
        Write-Host '    local, git-ignored secrets file (03 Demo\.streamlit\secrets.toml)'
        Write-Host '    so the application can read it, and that file is removed again'
        Write-Host '    when the application stops. You will be asked again on every'
        Write-Host '    start. The key is never displayed and never written to logs.'
        Write-Host ''
        Write-Host '    Where to get one: sign in at https://console.anthropic.com ->'
        Write-Host '    API Keys -> Create Key. The account needs API credit loaded,'
        Write-Host '    otherwise analysis will not work. Keys start with "sk-ant-".'
        Write-Host ''
        Write-Host '    Treat the key like a bank card PIN - never share it.' -ForegroundColor Yellow
        Write-Host '  -----------------------------------------------------------------' -ForegroundColor Gray
        Write-Host ''
        $saved = $false
        for ($attempt = 1; $attempt -le 3; $attempt++) {
            $entered = Read-SecretText -Prompt 'Paste the key here and press Enter'
            if ($entered) { $entered = $entered.Trim() }
            if (-not $entered) {
                Write-Problem 'Nothing was entered.'
                continue
            }
            if ($entered -eq $PlaceHolder) {
                Write-Problem 'That is the example placeholder text, not a real key.'
                continue
            }
            Write-Info 'Verifying the key with Anthropic (free check, no tokens are billed)...'
            $verdict = Test-ApiKey $entered
            if ($verdict -eq 'valid') {
                Save-Key $entered
                $entered = $null
                Write-Ok 'Key verified. It is stored for this session only and removed when the application stops.'
                $saved = $true
                break
            }
            if ($verdict -eq 'invalid') {
                Write-Problem 'Anthropic REJECTED this key. Check that you copied the whole key (it starts with "sk-ant-") and that it has not been revoked. Keys come from https://console.anthropic.com -> API Keys.'
                continue
            }
            # Unreachable: cannot verify online - fall back to a format check.
            if ($entered -like 'sk-ant-*') {
                Save-Key $entered
                $entered = $null
                Write-Problem 'Could not reach Anthropic to verify the key (no internet?), but it looks like a key, so it was accepted for this session. If analysis fails later, restart and enter it again.'
                $saved = $true
                break
            }
            Write-Problem 'Could not reach Anthropic to verify the key, and it does not look like one (keys start with "sk-ant-"). It was NOT saved - check your internet connection and the key, then try again.'
        }
        if (-not $saved) {
            Stop-WithMessage 'No working key was provided. The application cannot run an analysis without one.'
        }
        [System.GC]::Collect()
}

# ---------------------------------------------------------------------------
# 5. Free port.
# ---------------------------------------------------------------------------
function Get-FreePort {
    param([int]$Start = 8501, [int]$Count = 20)
    for ($port = $Start; $port -lt ($Start + $Count); $port++) {
        $inUse = $false
        try {
            # Bind on Any, not Loopback: the server binds every interface, so
            # a loopback-only test can report a busy port as free.
            $listener = [System.Net.Sockets.TcpListener]::new(
                [System.Net.IPAddress]::Any, $port)
            $listener.Start()
            $listener.Stop()
        } catch {
            $inUse = $true
        }
        if (-not $inUse) { return $port }
    }
    return $Start
}

$port = Get-FreePort
if ($port -ne 8501) {
    Write-Info "Port 8501 is busy - using $port instead."
}

if ($CheckOnly) {
    Write-Host ''
    if ($script:ProblemCount -eq 0) {
        Write-Ok 'All checks passed. (-CheckOnly: the application was not started.)'
        exit 0
    }
    Write-Host "    Checks finished with $($script:ProblemCount) note(s) - see the [!] lines above. (-CheckOnly: the application was not started; exit code 2 signals the notes.)" -ForegroundColor Yellow
    exit 2
}

# ---------------------------------------------------------------------------
# 6. Start.
# ---------------------------------------------------------------------------
Write-Step 'Starting the application...'
Write-Host ''
Write-Host '  Your browser will open by itself in a few seconds.' -ForegroundColor White
Write-Host "  If it does not: http://localhost:$port" -ForegroundColor White
Write-Host ''
Write-Host '  IMPORTANT: leave this window open - it keeps the app running.' -ForegroundColor Yellow
Write-Host '  To stop: press Ctrl+C, or just close this window.' -ForegroundColor Yellow
Write-Host ''
Write-Host '  The interface starts in Bulgarian; there is an English switch at the top.' -ForegroundColor Gray
Write-Host '  Do NOT enter real customer data - use the bundled examples.' -ForegroundColor Gray
Write-Host ''

Set-Location -LiteralPath (Join-Path $ProjectRoot '03 Demo')

# Started headless for two reasons: on a first run Streamlit would otherwise
# ask for an email address in the terminal and stop there, and this way the
# browser only opens once the application is actually serving.
$streamlit = Start-Process -FilePath $VenvPython -PassThru -NoNewWindow `
    -ArgumentList @('-m', 'streamlit', 'run', 'app.py',
                    '--server.port', $port, '--server.headless', 'true')

$ready = $false
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Milliseconds 500
    # Our own process is checked first and again after a successful probe:
    # another program already serving this port would otherwise answer the
    # probe and make a failed start look successful.
    if ($streamlit.HasExited) { break }
    try {
        Invoke-WebRequest "http://localhost:$port" -UseBasicParsing -TimeoutSec 2 |
            Out-Null
        if (-not $streamlit.HasExited) {
            $ready = $true
            break
        }
    } catch {
        # not up yet - keep waiting
    }
}

if ($ready) {
    Write-Ok 'The application is running. Opening the browser...'
    Start-Process "http://localhost:$port"
} elseif ($streamlit.HasExited) {
    Remove-SavedKey
    Write-Problem 'The application stopped right after starting.'
    Write-Host '    The usual cause is another copy already running, holding the'
    Write-Host '    same port. Close any other launcher window and try again.'
    if (-not [Console]::IsInputRedirected) {
        Wait-CloseKey
    }
    # Propagate the startup failure so wrappers and scripts can see it.
    exit 1
} else {
    Write-Problem "The application is slow to start. Try opening it manually: http://localhost:$port"
}

$streamlit.WaitForExit()
$exitCode = $streamlit.ExitCode

# Session over: the key file has served its purpose.
Remove-SavedKey

Write-Host ''
if ($exitCode -ne 0 -and $null -ne $exitCode) {
    Write-Problem "The application ended with code $exitCode. If this was not you closing it, run the launcher again."
    if (-not [Console]::IsInputRedirected) {
        Wait-CloseKey
    }
    exit 1
}
Write-Host 'The application has stopped. (Your API key file was removed;' -ForegroundColor Gray
Write-Host 'you will be asked for the key again on the next start.)' -ForegroundColor Gray
Start-Sleep -Seconds 2
exit 0
