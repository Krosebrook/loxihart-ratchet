# Compatibility and verification

Documentation checked September 24, 2026. “Documented path” means the vendor documents discovery from that folder; it does not mean this package has passed a full session on that host.

| Installer name | Host | Project skill path | Primary source |
| --- | --- | --- | --- |
| `codex` | Codex | `.agents/skills` | [OpenAI](https://developers.openai.com/codex/skills/) |
| `claude` | Claude Code | `.claude/skills` | [Anthropic](https://code.claude.com/docs/en/skills) |
| `antigravity` | Antigravity | `.agents/skills` | [Google](https://antigravity.google/docs/skills) |
| `gemini` | Gemini CLI | `.gemini/skills` | [Gemini CLI](https://geminicli.com/docs/cli/skills/) |
| `grok` | Grok Build | `.grok/skills` | [xAI](https://docs.x.ai/build/features/skills-plugins-marketplaces) |
| `opencode` | OpenCode | `.opencode/skills` | [OpenCode](https://opencode.ai/v2/docs/skills) |
| `kimi` | Kimi Code | `.agents/skills` | [Moonshot](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html) |
| `qwen` | Qwen Code | `.qwen/skills` | [Qwen](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) |
| `copilot` | GitHub Copilot | `.github/skills` | [GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) |
| `portable` | Host with compatible discovery | `.agents/skills` | Check the host's documentation |

Older Antigravity IDE versions also document `.agent/skills`; this installer targets the current `.agents/skills` convention. Kimi uses the shared project path rather than assuming a stable vendor-specific home directory. Grok, Kimi, Qwen, and Gemini chat products are not interchangeable with their coding-agent surfaces.

## What is tested

The automated suite exercises copy destinations, repeat installation, collision refusal, and the local checkpoint ledger's success and failure paths. Static checks validate skill metadata, bundled resources, manifests, and local Markdown links. CI runs on Linux and Windows with Python 3.10 and 3.13.

Full interactive activation, subagent isolation, visual capture, human approval UX, and end-to-end project execution have not been verified on all hosts. Both plugin formats are packaged; a valid manifest does not establish marketplace acceptance or runtime execution.

## Capability fallback

| Missing capability | Honest outcome |
| --- | --- |
| Automatic skill loading | Ask the host to read `ratchet/SKILL.md` and referenced resources explicitly |
| Python or Git | Use a manual evidence packet and disclose that no fingerprint validation ran |
| Runtime/test environment | Prepare checks and report behavior blocked |
| Screenshot/vision tools | Supply a capture/review packet; keep required UI gate blocked |
| Independent subagent sessions | Obtain separate external reviewer sessions; do not simulate independence |
| Explicit approval or delegated scope | Present the concrete checkpoint and wait at the approval gate |

A Markdown skill cannot grant tools, credentials, permissions, or higher-priority instruction overrides. Native UI operations, provider API calls, and unattended scheduling belong to the host and its authorization model.
