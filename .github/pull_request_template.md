## Summary
- **Title:** <!-- short title -->
- **Type:** Feature / Fix / Refactor / Docs
- **SCR ID(s):** <!-- e.g., SCR000001, SCR000002 -->
- **Related Issues:** Closes #<issue-id>, Relates-to #<issue-id>

## Scope / What Changed
<!-- High-level description of code changes, modules touched, and reason -->

## Test Plan
- [ ] Local build succeeds (`make` or CI build log attached)
- [ ] Added/updated testcases under `testcases/`:
  - [ ] case1/
  - [ ] case2/
- [ ] `run_testcases.(sh|bat)` produces `testcases_run_summary.md`
- [ ] All tests **PASS** locally before requesting review

### Attachments
- [ ] Snippet from `testcases_run_summary.md`
- [ ] Relevant `log.txt` excerpts (if any)
- [ ] Screenshots/plots (optional)

## Risk & Rollback
- **Risk Level:** Low / Medium / High  
- **Fallback Plan:** Revert commit / Disable feature flag / Hotfix

## Checklists
**Coding**
- [ ] Follows folder structure (`app/{calibration,h_files,c_files}`, `scr/`, `tools/`)
- [ ] Public headers documented (`app/h_files/*.h`)
- [ ] Calibrations declared in `calibration.h` and defined in `calibration.c` / `calibration.txt`
- [ ] No hardcoded constants in logic (use calibrations)

**Quality**
- [ ] Lint/format (if configured)
- [ ] PR size reasonable or split

**Process**
- [ ] Linked SCR issue moved to `in progress`
- [ ] If **any** test fails in CI → label the linked SCR `rework`
- [ ] If all tests pass on `main` post-merge → label the linked SCR `closed`

## Notes for Reviewers
<!-- Anything reviewers should focus on (edge cases, trade-offs, TODOs) -->
