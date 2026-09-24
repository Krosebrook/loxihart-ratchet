# Sources and attribution

Reviewed September 24, 2026. Article text and proprietary implementations are not included in this repository.

- [Helix: The internal tool powering our Shopify app's native migration](https://shopify.engineering/helix), Talha Naqvi, Shopify Engineering, September 21, 2026. Primary source for checkpoints, ordered gates, separate reviewers, engineer approval, and explicitly requested autonomy.
- [Migrating Shop app from React Native to native](https://shopify.engineering/shop-app-migration), Shopify Engineering, September 10, 2026. Context for parity checks, runtime observation, and keeping plan acceptance attached to the reviewed content.
- [Native is now the future of mobile at Shopify](https://shopify.engineering/back-to-native), Shopify Engineering. Context for the architectural change; this package does not recommend a specific mobile framework.
- [career-ops](https://github.com/career-ops-hq/career-ops). Product/distribution inspiration for a public, customizable project used through coding agents. No code or documentation copied.
- [Agent Skills specification](https://agentskills.io/specification). Interoperable `SKILL.md` metadata and resource layout.
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference). Claude manifest and plugin directory conventions.
- [Agent compatibility sources](compatibility.md). Official skill-discovery documentation for each supported installation target.

The user-provided Spanish editorial summary informed the initial requirements; the implementation was checked against the primary sources above. The private pasted document itself is not redistributed.

## What this repository adds

The six-skill decomposition, project installer, JSON ledger format, content fingerprinting, three-attempt default, tests, and templates are this project's implementation. Shopify's internal Helix, Tardis, private architecture, prompts, and model orchestration are not bundled. No affiliation or endorsement is implied. Provider model choices remain with the user and host.
