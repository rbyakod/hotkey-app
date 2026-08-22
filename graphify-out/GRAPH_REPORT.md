# Graph Report - /Users/ravibyakod/WORK/hotkey-app  (2026-08-22)

## Corpus Check
- Corpus is ~2,261 words - fits in a single context window. You may not need a graph.

## Summary
- 38 nodes · 53 edges · 10 communities (2 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9

## God Nodes (most connected - your core abstractions)
1. `HotkeyLauncher` - 14 edges
2. `wait_for_macos_permissions()` - 4 edges
3. `run_daemon()` - 4 edges
4. `is_accessibility_trusted()` - 2 edges
5. `open_privacy_settings()` - 2 edges
6. `on_press()` - 2 edges
7. `on_release()` - 2 edges
8. `index()` - 2 edges
9. `set_mapping()` - 2 edges
10. `delete_mapping()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (10 total, 8 thin omitted)

### Community 1 - "Community 1"
Cohesion: 0.52
Nodes (6): is_accessibility_trusted(), on_press(), on_release(), open_privacy_settings(), run_daemon(), wait_for_macos_permissions()

### Community 2 - "Community 2"
Cohesion: 0.47
Nodes (4): delete_mapping(), index(), set_mapping(), route

## Knowledge Gaps
- **6 isolated node(s):** `install_launch_agent.sh script`, `start_config_gui.sh script`, `start_daemon.sh script`, `status_launch_agent.sh script`, `stop_daemon.sh script` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HotkeyLauncher` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.314) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `run_daemon()` (e.g. with `on_press()` and `on_release()`) actually correct?**
  _`run_daemon()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `install_launch_agent.sh script`, `start_config_gui.sh script`, `start_daemon.sh script` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._