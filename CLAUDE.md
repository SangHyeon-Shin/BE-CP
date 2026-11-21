@AGENTS.md

## Claude Code 전용
- 세팅: `/setup-be-cp`. MCP 승인 상태는 `/mcp`에서 본다.
- MCP는 `.mcp.json`에 있다(kordoc, korean-law). Windows의 kordoc 보정과 AutoCAD 등록은 `claude mcp add --scope local|user`로 한다(`SETUP.md` 부록 B).
- 스킬·명령·에이전트를 고치면 `python tools/sync_codex.py`를 실행해 Codex용 생성물(`.agents/skills/`, `.codex/agents/`)을 맞춘다.
