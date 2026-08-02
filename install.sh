#!/usr/bin/env bash
set -euo pipefail

PET_ID="hei-mao"
DEFAULT_BASE_URL="https://raw.githubusercontent.com/MisonL/hei-mao/main"
PET_JSON_SHA256="dafa673543839e1742fd78b766549877c249286930b3a9ae47903b9c6f2e5802"
SPRITESHEET_SHA256="dd5f50c1f34010784af94c801a5042963e8aae6031f520fdd43f2b099811453a"
STEP_INDEX=0
STEP_TOTAL=4

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  COLOR_RESET="$(printf '\033[0m')"
  COLOR_DIM="$(printf '\033[2m')"
  COLOR_CYAN="$(printf '\033[36m')"
  COLOR_GREEN="$(printf '\033[32m')"
  COLOR_RED="$(printf '\033[31m')"
  COLOR_YELLOW="$(printf '\033[33m')"
else
  COLOR_RESET=""
  COLOR_DIM=""
  COLOR_CYAN=""
  COLOR_GREEN=""
  COLOR_RED=""
  COLOR_YELLOW=""
fi

can_animate() {
  [ -t 1 ] &&
    [ "${TERM:-}" != "dumb" ] &&
    [ -z "${HEI_MAO_NO_ANIMATION:-}" ]
}

print_pig_frame() {
  frame="$1"
  eyes="o   o"
  tail="~"
  clear_prefix=""

  if can_animate; then
    clear_prefix="$(printf '\033[2K')"
  fi

  case "$frame" in
    1)
      eyes="-   -"
      tail=")"
      ;;
    2)
      eyes="o   o"
      tail="("
      ;;
  esac

  printf '%s%s\n' "$clear_prefix" '       #####'
  printf '%s%s\n' "$clear_prefix" '     .-""""-.'
  printf '%s    /  %s  \\\n' "$clear_prefix" "$eyes"
  printf '%s   |    (oo)   |%s\n' "$clear_prefix" "$tail"
  printf '%s%s\n' "$clear_prefix" '   |  /|____|\ |'
  printf '%s%s\n' "$clear_prefix" "    \\ HEI MAO/"
  printf '%s%s\n' "$clear_prefix" "     '------'"
}

show_intro() {
  printf '\n'
  printf '%s%s%s\n' "$COLOR_CYAN" '==================================================' "$COLOR_RESET"
  printf '%s%s%s\n' "$COLOR_CYAN" ' Hei Mao Codex Pet Installer' "$COLOR_RESET"
  printf '%s%s%s\n' "$COLOR_CYAN" '==================================================' "$COLOR_RESET"

  if ! can_animate; then
    print_pig_frame 0
    return
  fi

  printf '\033[s'
  for frame in 0 1 2 1 0; do
    printf '\033[u'
    print_pig_frame "$frame"
    sleep 0.12
  done
}

step() {
  STEP_INDEX=$((STEP_INDEX + 1))
  printf '\n%s[%d/%d]%s %s\n' "$COLOR_CYAN" "$STEP_INDEX" "$STEP_TOTAL" "$COLOR_RESET" "$1"
}

detail() {
  printf '      %s%s%s\n' "$COLOR_DIM" "$1" "$COLOR_RESET"
}

ok() {
  printf '%s[OK]%s %s\n' "$COLOR_GREEN" "$COLOR_RESET" "$1"
}

log() {
  printf '%s[INFO]%s %s\n' "$COLOR_YELLOW" "$COLOR_RESET" "$1"
}

die() {
  printf '\n%s[ERROR]%s %s\n' "$COLOR_RED" "$COLOR_RESET" "$1" >&2
  exit 1
}

need_home() {
  if [ -z "${CODEX_HOME:-}" ] && [ -z "${HOME:-}" ]; then
    die "HOME is not set. Set CODEX_HOME or HOME before running this installer."
  fi
}

download_file() {
  src="$1"
  dst="$2"

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$src" -o "$dst"
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    wget -qO "$dst" "$src"
    return
  fi

  die "curl or wget is required to download assets."
}

sha256_file() {
  file_path="$1"

  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$file_path" | awk '{print $1}'
    return
  fi

  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$file_path" | awk '{print $1}'
    return
  fi

  die "sha256sum or shasum is required to verify downloaded assets."
}

verify_sha256() {
  file_path="$1"
  expected="$2"
  actual="$(sha256_file "$file_path")"

  if [ "$actual" != "$expected" ]; then
    die "SHA256 mismatch for $(basename "$file_path"). Expected $expected but got $actual."
  fi

  detail "SHA256 ok: $(basename "$file_path")"
}

copy_or_download_assets() {
  tmp_dir="$1"
  base_url="${HEI_MAO_BASE_URL:-$DEFAULT_BASE_URL}"
  script_path="${BASH_SOURCE[0]:-}"

  if [ -z "${HEI_MAO_BASE_URL:-}" ] &&
    [ -n "$script_path" ] &&
    [ -f "$script_path" ]; then
    script_dir="$(cd "$(dirname "$script_path")" >/dev/null 2>&1 && pwd -P)"

    if [ -f "$script_dir/pet.json" ] &&
      [ -f "$script_dir/spritesheet.webp" ]; then
      detail "Source: local files"
      detail "Path: $script_dir"
      cp "$script_dir/pet.json" "$tmp_dir/pet.json"
      cp "$script_dir/spritesheet.webp" "$tmp_dir/spritesheet.webp"
      return
    fi
  fi

  base_url="${base_url%/}"
  detail "Source: GitHub raw"
  detail "URL: $base_url"
  download_file "$base_url/pet.json" "$tmp_dir/pet.json"
  download_file "$base_url/spritesheet.webp" "$tmp_dir/spritesheet.webp"
}

validate_assets() {
  tmp_dir="$1"

  [ -s "$tmp_dir/pet.json" ] || die "Downloaded pet.json is missing or empty."
  [ -s "$tmp_dir/spritesheet.webp" ] || die "Downloaded spritesheet.webp is missing or empty."

  if ! grep -q '"id"[[:space:]]*:[[:space:]]*"hei-mao"' "$tmp_dir/pet.json"; then
    die "pet.json does not describe the expected pet id: $PET_ID"
  fi

  verify_sha256 "$tmp_dir/pet.json" "$PET_JSON_SHA256"
  verify_sha256 "$tmp_dir/spritesheet.webp" "$SPRITESHEET_SHA256"
}

main() {
  show_intro

  step "Prepare target"
  need_home

  codex_home="${CODEX_HOME:-$HOME/.codex}"
  install_dir="${HEI_MAO_INSTALL_DIR:-$codex_home/pets/$PET_ID}"
  tmp_parent="${TMPDIR:-/tmp}"
  tmp_parent="${tmp_parent%/}"
  tmp_dir="$(mktemp -d "$tmp_parent/hei-mao.XXXXXX")"
  trap 'rm -rf "$tmp_dir"' EXIT
  detail "Target: $install_dir"
  detail "Work dir: $tmp_dir"

  step "Fetch assets"
  copy_or_download_assets "$tmp_dir"

  step "Validate package"
  validate_assets "$tmp_dir"
  ok "Package metadata and spritesheet are valid."

  step "Install files"
  mkdir -p "$install_dir"
  cp "$tmp_dir/pet.json" "$install_dir/pet.json"
  cp "$tmp_dir/spritesheet.webp" "$install_dir/spritesheet.webp"
  detail "Wrote: pet.json"
  detail "Wrote: spritesheet.webp"

  printf '\n'
  ok "Hei Mao pet installed."
  detail "Install dir: $install_dir"
  detail "Next: Codex App settings -> Appearance -> Pets -> Refresh -> Hei Mao"
  printf '\n'
}

main "$@"
