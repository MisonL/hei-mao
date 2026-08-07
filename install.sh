#!/usr/bin/env bash
set -euo pipefail

DEFAULT_BASE_URL="https://raw.githubusercontent.com/MisonL/hei-mao/main"
PET_ID=""
PET_SUBDIR=""
PET_JSON_SHA256=""
SPRITESHEET_SHA256=""
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

configure_pet() {
  requested_pet_id="${1:-${HEI_MAO_PET_ID:-hei-mao}}"

  case "$requested_pet_id" in
    hei-mao)
      PET_JSON_SHA256="dafa673543839e1742fd78b766549877c249286930b3a9ae47903b9c6f2e5802"
      SPRITESHEET_SHA256="dd5f50c1f34010784af94c801a5042963e8aae6031f520fdd43f2b099811453a"
      PET_SUBDIR="pets/$requested_pet_id"
      ;;
    hei-mao-quality)
      PET_JSON_SHA256="c7539a98ae2767ab70c69e31c588f7e977e440307dc8bca791fff3bc8350eb07"
      SPRITESHEET_SHA256="1e22f95b918ab423d1b4bede9af93761e89ff39c5a961ee3728c671b0dd05f9f"
      PET_SUBDIR="pets/$requested_pet_id"
      ;;
    hei-mao-butler)
      PET_JSON_SHA256="903f3c673f510048fb3daf498976d0a99e958edc6ee969c2790b8555be89daf4"
      SPRITESHEET_SHA256="1e59bcd0024b4f381e740655e2457df490773e7038ea3f77f073f3ac5ca46304"
      PET_SUBDIR="pets/$requested_pet_id"
      ;;
    hei-mao-chef)
      PET_JSON_SHA256="d210cb46a995d378de755b3eb40815c3a114476bc25120bd184677b0ec5dd43a"
      SPRITESHEET_SHA256="32a4df73b3ecc58c0f1488025a841fb7be7c93127d3f0134f22d6c799580d957"
      PET_SUBDIR="pets/$requested_pet_id"
      ;;
    hei-mao-foodie)
      PET_JSON_SHA256="0857baacd1dbb5912ceb03a5fc4cadf121923f6d04190b9356f7588f82410a6c"
      SPRITESHEET_SHA256="fd2173bc21c5ca563cadfb1935bb037f08812559fd3d6717c1add7a40d79dc49"
      PET_SUBDIR="pets/$requested_pet_id"
      ;;
    *)
      die "Unsupported pet id: $requested_pet_id. Supported ids: hei-mao, hei-mao-quality, hei-mao-butler, hei-mao-chef, hei-mao-foodie."
      ;;
  esac

  PET_ID="$requested_pet_id"
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
    source_dir="$script_dir"
    if [ -n "$PET_SUBDIR" ]; then
      source_dir="$script_dir/$PET_SUBDIR"
    fi

    if [ -f "$source_dir/pet.json" ] &&
      [ -f "$source_dir/spritesheet.webp" ]; then
      detail "Source: local files"
      detail "Path: $source_dir"
      cp "$source_dir/pet.json" "$tmp_dir/pet.json"
      cp "$source_dir/spritesheet.webp" "$tmp_dir/spritesheet.webp"
      return
    fi
  fi

  base_url="${base_url%/}"
  if [ -n "$PET_SUBDIR" ]; then
    base_url="$base_url/$PET_SUBDIR"
  fi
  detail "Source: GitHub raw"
  detail "URL: $base_url"
  download_file "$base_url/pet.json" "$tmp_dir/pet.json"
  download_file "$base_url/spritesheet.webp" "$tmp_dir/spritesheet.webp"
}

validate_assets() {
  tmp_dir="$1"

  [ -s "$tmp_dir/pet.json" ] || die "Downloaded pet.json is missing or empty."
  [ -s "$tmp_dir/spritesheet.webp" ] || die "Downloaded spritesheet.webp is missing or empty."

  if ! grep -q "\"id\"[[:space:]]*:[[:space:]]*\"$PET_ID\"" "$tmp_dir/pet.json"; then
    die "pet.json does not describe the expected pet id: $PET_ID"
  fi

  verify_sha256 "$tmp_dir/pet.json" "$PET_JSON_SHA256"
  verify_sha256 "$tmp_dir/spritesheet.webp" "$SPRITESHEET_SHA256"
}

main() {
  configure_pet "${1:-}"
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
  ok "$PET_ID pet installed."
  detail "Install dir: $install_dir"
  detail "Next: Codex App settings -> Appearance -> Pets -> Refresh -> $PET_ID"
  printf '\n'
}

main "$@"
