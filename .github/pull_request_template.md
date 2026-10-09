## Summary

<!-- Explain the problem, the user-visible result, and why this change belongs in this pull request. -->

## Related issue

<!-- Use "closes #123". If no issue applies, use "no-issue: <reason>". -->

closes #

## User-visible behavior

<!-- Describe API, configuration, lifecycle, or compatibility changes. Write "None" when behavior is unchanged. -->

## Verification

<!-- List the commands and manual scenarios that were actually run. -->

- [ ] `cargo fmt --all -- --check`
- [ ] `cargo test --workspace`
- [ ] `cargo clippy --workspace --all-targets -- -D warnings`
- [ ] `cargo doc --workspace --no-deps`

## Review checklist

- [ ] The change is self-contained and has no unused production code.
- [ ] New behavior is covered by tests that fail without the change.
- [ ] API, configuration, lifecycle, or architecture changes are documented in both languages.
- [ ] `Cargo.lock` is updated when dependencies change.
- [ ] Commit subjects follow `type: imperative description`, contain no component scope, and are at most 50 characters.
- [ ] Every commit contains a `Signed-off-by` trailer.
