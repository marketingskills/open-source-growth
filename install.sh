#!/bin/sh
set -eu

REPO="marketingskills/open-source-growth"
REF="main"
INSTALL_DIR="${HOME}/.open-source-growth"
FORCE=0

# Color support
if [ -t 1 ]; then
  BOLD=$(tput bold 2>/dev/null || printf '')
  GREEN=$(tput setaf 2 2>/dev/null || printf '')
  BLUE=$(tput setaf 4 2>/dev/null || printf '')
  DIM=$(tput dim 2>/dev/null || printf '')
  RESET=$(tput sgr0 2>/dev/null || printf '')
else
  BOLD=""; GREEN=""; BLUE=""; DIM=""; RESET=""
fi

banner() {
  cat >&2 <<EOF
${BLUE}┌────────────────────────────────────────────┐${RESET}
${BLUE}│${RESET} ${BOLD}OPEN SOURCE GROWTH OPERATOR${RESET}              ${BLUE}│${RESET}
${BLUE}├────────────────────────────────────────────┤${RESET}
${BLUE}│${RESET} ${DIM}Growth skills for open-source repos${RESET}         ${BLUE}│${RESET}
${BLUE}└────────────────────────────────────────────┘${RESET}
EOF
}

log()  { printf '%s[info]%s %s\n' "$BLUE" "$RESET" "$*" >&2; }
ok()   { printf '%s[ok]%s   %s\n' "$GREEN" "$RESET" "$*" >&2; }
die()  { printf '%s[err]%s  %s\n' "${RED:-}" "$RESET" "$*" >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }

main() {
  banner

  # Parse flags
  while [ $# -gt 0 ]; do
    case "$1" in
      --force) FORCE=1 ;;
      --ref) shift; REF="$1" ;;
      *) die "Unknown option: $1" ;;
    esac
    shift
  done

  tmp=$(mktemp -d "${TMPDIR:-/tmp}/oss-growth.XXXXXX")
  trap 'rm -rf "$tmp"' EXIT HUP INT TERM

  log "Fetching open-source-growth@$REF from GitHub..."
  url="https://codeload.github.com/$REPO/tar.gz/$REF"
  archive="$tmp/repo.tar.gz"

  if have curl; then
    curl -fsSL "$url" -o "$archive"
  elif have wget; then
    wget -qO "$archive" "$url"
  else
    die "Need curl or wget"
  fi

  tar -xzf "$archive" -C "$tmp"
  src=$(find "$tmp" -mindepth 1 -maxdepth 1 -type d | head -1)

  [ -d "$src/skills" ] || die "Archive invalid: no skills/ directory"

  rm -rf "$INSTALL_DIR"
  mkdir -p "$INSTALL_DIR"
  cp -R "$src/skills" "$INSTALL_DIR/skills"
  cp "$src/AGENTS.md" "$INSTALL_DIR/" 2>/dev/null || true
  cp "$src/README.md" "$INSTALL_DIR/" 2>/dev/null || true

  ok "Installed skills to $INSTALL_DIR/skills/"
  echo
  echo "  ${BOLD}repo-growth-operator${RESET}         — Audit, rewrite, demo, launch, monetise"
  echo "  ${BOLD}ecosystem-inclusion-operator${RESET}  — Discover targets, score, open PRs"
  echo

  if have gh; then
    log "GitHub CLI detected. Point your agent to $INSTALL_DIR/skills/ or use directly from git."
  else
    log "Install GitHub CLI (gh) for star/fork/watch actions: https://cli.github.com/"
  fi

  echo
  echo "  ${BOLD}Copy this prompt to your agent:${RESET}"
  echo "    Explore and use the skills in $INSTALL_DIR/skills/"
  echo
  echo "  ${BOLD}Or install via git:${RESET}"
  echo "    npx skills add marketingskills/open-source-growth"
  echo
}

main "$@"
