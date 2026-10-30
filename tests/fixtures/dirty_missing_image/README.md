<!-- synced-with: README_CN.md @ 0de816af4a5a629504e5fb7fe9ce6d0c8161aa13 -->

# EgressAPIKEY

**Multi-port socks5/http proxy gateway between AI gateways and upstream providers — sticky exit-IP routing for AI API keys, with a topology canvas.**

[![License](https://img.shields.io/github/license/Xxx91n/EgressAPIKEY?style=flat-square)](https://github.com/Xxx91n/EgressAPIKEY/blob/main/LICENSE) [![CI](https://img.shields.io/github/actions/workflow/status/Xxx91n/EgressAPIKEY/ci.yml?style=flat-square&label=CI)](https://github.com/Xxx91n/EgressAPIKEY/actions/workflows/ci.yml)

<p align="center">
  <img src="assets/readme/missing_hero.svg" alt="EgressAPIKEY — sticky exit-IP routing for AI API keys" width="1200">
</p>

## What & why

EgressAPIKEY is a desktop application (Tauri 2 + React 19) that sits between your AI gateway.

## Limitations

Currently only loopback interfaces are supported in Mode A. Multi-node clustering is out of scope for the current release.
